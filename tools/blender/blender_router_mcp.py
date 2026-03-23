# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp[cli]>=1.0", "pydantic>=2.0"]
# ///
"""
Blender Router MCP — Multi-instance TCP proxy for parallel Blender modeling.

Routes MCP tool calls to multiple Blender instances via raw TCP sockets,
matching the BlenderMCP addon's wire protocol exactly:
  Request:  {"type": "command_name", "params": {...}}
  Response: {"status": "success|error", "result": {...}}

Architecture:
    Claude Code ──[stdio/MCP]──> Router ──[TCP:9876]──> Blender 1 (terrain.blend)
                                        ──[TCP:9877]──> Blender 2 (buildings.blend)
                                        ──[TCP:9878]──> Blender 3 (landscape.blend)

Every tool includes a `target` parameter that selects which Blender instance
receives the command. Agent teams share this single MCP server but each
agent routes to its own Blender instance.

Setup:
    1. Open multiple Blender instances
    2. In each: press N → BlenderMCP tab → set port (9876, 9877, etc.) → Connect
    3. Set env var: BLENDER_INSTANCES='{"terrain": 9876, "buildings": 9877}'
    4. Run: uv run tools/blender/blender_router_mcp.py

.mcp.json config:
    {
      "mcpServers": {
        "blender": {
          "command": "uv",
          "args": ["run", "tools/blender/blender_router_mcp.py"],
          "env": {
            "BLENDER_INSTANCES": "{\"terrain\": 9876, \"buildings\": 9877}"
          }
        }
      }
    }
"""

import json
import logging
import os
import socket
import threading
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROUTER_TIMEOUT = float(os.getenv("BLENDER_ROUTER_TIMEOUT", "30.0"))
ROUTER_LOG_LEVEL = os.getenv("BLENDER_ROUTER_LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, ROUTER_LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
logger = logging.getLogger("blender_router")


# ---------------------------------------------------------------------------
# TCP Connection — matches BlenderMCP addon's wire protocol
# ---------------------------------------------------------------------------

class BlenderInstanceConnection:
    """TCP socket connection to a single Blender MCP addon instance.

    Thread-safe: a per-instance lock serializes commands to the same Blender
    window while allowing concurrent commands to different instances.
    Connects on first command (not at registration time).
    """

    def __init__(self, name: str, host: str, port: int):
        self.name = name
        self.host = host
        self.port = port
        self._sock: socket.socket | None = None
        self._lock = threading.Lock()

    # -- connection lifecycle --

    def connect(self) -> bool:
        if self._sock is not None:
            return True
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((self.host, self.port))
            logger.info(f"[{self.name}] Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            logger.error(f"[{self.name}] Connection failed: {e}")
            self._sock = None
            return False

    def disconnect(self):
        if self._sock is not None:
            try:
                self._sock.close()
            except Exception:
                pass
            finally:
                self._sock = None

    @property
    def is_connected(self) -> bool:
        return self._sock is not None

    # -- protocol --

    def _receive_full_response(self) -> bytes:
        """Receive a complete JSON response using incremental parsing.

        Reads chunks until a valid JSON object is detected via
        json.JSONDecoder.raw_decode().
        """
        accumulated = ""
        decoder = json.JSONDecoder()
        assert self._sock is not None
        self._sock.settimeout(ROUTER_TIMEOUT)

        while True:
            try:
                chunk = self._sock.recv(65536)
            except socket.timeout:
                break
            except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
                raise ConnectionError(f"Socket error during receive: {e}")

            if not chunk:
                break

            accumulated += chunk.decode("utf-8")

            # Attempt JSON parse when we see a closing brace
            if accumulated.rstrip().endswith("}"):
                try:
                    decoder.raw_decode(accumulated)
                    return accumulated.encode("utf-8")
                except json.JSONDecodeError:
                    continue

        # Try to use what we have
        if accumulated:
            try:
                decoder.raw_decode(accumulated)
                return accumulated.encode("utf-8")
            except json.JSONDecodeError:
                raise Exception(f"[{self.name}] Incomplete JSON response ({len(accumulated)} bytes)")
        raise Exception(f"[{self.name}] No data received")

    def send_command(self, command_type: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
        """Send a command to this Blender instance and return the result.

        Thread-safe — acquires per-instance lock. Reconnects on failure.
        """
        with self._lock:
            # Connect on demand
            if self._sock is None and not self.connect():
                raise ConnectionError(
                    f"Cannot connect to Blender instance '{self.name}' "
                    f"at {self.host}:{self.port}. Is Blender running with "
                    f"the MCP addon on port {self.port}?"
                )

            command = {"type": command_type, "params": params or {}}

            try:
                command_json = json.dumps(command)
                logger.debug(f"[{self.name}] >> {command_type} ({len(command_json)} bytes)")
                assert self._sock is not None
                self._sock.sendall(command_json.encode("utf-8"))

                response_data = self._receive_full_response()
                response = json.loads(response_data.decode("utf-8"))
                logger.debug(f"[{self.name}] << status={response.get('status')}")

                if response.get("status") == "error":
                    raise Exception(response.get("message", "Unknown error from Blender"))

                return response.get("result", {})

            except socket.timeout:
                self._sock = None
                raise Exception(
                    f"[{self.name}] Timeout ({ROUTER_TIMEOUT}s) waiting for Blender. "
                    f"Try simplifying the operation or increasing BLENDER_ROUTER_TIMEOUT."
                )
            except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
                self._sock = None
                raise ConnectionError(f"[{self.name}] Connection lost: {e}")
            except json.JSONDecodeError as e:
                self._sock = None
                raise Exception(f"[{self.name}] Invalid JSON response: {e}")
            except Exception:
                self._sock = None
                raise


# ---------------------------------------------------------------------------
# Instance Registry
# ---------------------------------------------------------------------------

class InstanceRegistry:
    """Maps instance names to TCP connections. Thread-safe."""

    def __init__(self):
        self._instances: Dict[str, BlenderInstanceConnection] = {}
        self._lock = threading.Lock()

    def register(self, name: str, port: int, host: str = "127.0.0.1"):
        with self._lock:
            if name in self._instances:
                self._instances[name].disconnect()
            self._instances[name] = BlenderInstanceConnection(name, host, port)
            logger.info(f"Registered instance '{name}' -> {host}:{port}")

    def get(self, name: str) -> BlenderInstanceConnection:
        with self._lock:
            if name not in self._instances:
                available = ", ".join(sorted(self._instances.keys())) or "(none)"
                raise KeyError(
                    f"Unknown instance '{name}'. Available: {available}. "
                    f"Use blender_register_instance to add it."
                )
            return self._instances[name]

    def unregister(self, name: str):
        with self._lock:
            if name in self._instances:
                self._instances[name].disconnect()
                del self._instances[name]
                logger.info(f"Unregistered instance '{name}'")

    def list_all(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [
                {
                    "name": name,
                    "host": conn.host,
                    "port": conn.port,
                    "connected": conn.is_connected,
                }
                for name, conn in sorted(self._instances.items())
            ]

    def shutdown(self):
        with self._lock:
            for conn in self._instances.values():
                conn.disconnect()
            self._instances.clear()


# Global registry — loaded once at startup
registry = InstanceRegistry()


def _load_instances_from_env():
    """Load instances from BLENDER_INSTANCES env var.

    Format: JSON object mapping names to port numbers.
    Example: {"terrain": 9876, "buildings": 9877, "landscape": 9878}
    """
    raw = os.environ.get("BLENDER_INSTANCES", "")
    if not raw:
        logger.warning("BLENDER_INSTANCES not set — no instances registered. "
                       "Use blender_register_instance to add them at runtime.")
        return

    try:
        mapping = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid BLENDER_INSTANCES JSON: {e}")
        return

    for name, port in mapping.items():
        try:
            registry.register(name, int(port))
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid port for '{name}': {port} ({e})")


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp_server = FastMCP("blender_router")

# Load instances at import time (before server starts)
_load_instances_from_env()


# ---------------------------------------------------------------------------
# Routing helper
# ---------------------------------------------------------------------------

def _route(target: str, command_type: str, params: Dict[str, Any] | None = None) -> str:
    """Route a command to a Blender instance, return JSON string result."""
    try:
        conn = registry.get(target)
        result = conn.send_command(command_type, params)
        return json.dumps(result, indent=2)
    except KeyError as e:
        return json.dumps({"error": str(e)})
    except Exception as e:
        return json.dumps({"error": f"[{target}] {type(e).__name__}: {e}"})


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Instance Management
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def blender_list_instances() -> str:
    """List all registered Blender instances and their connection status.

    Use this first to discover available targets before routing commands.
    Instances are registered via BLENDER_INSTANCES env var or blender_register_instance.
    """
    instances = registry.list_all()

    # Probe connectivity for each instance
    for inst in instances:
        if not inst["connected"]:
            try:
                conn = registry.get(inst["name"])
                conn.connect()
                inst["connected"] = conn.is_connected
            except Exception:
                inst["connected"] = False

    return json.dumps({"instances": instances, "count": len(instances)}, indent=2)


@mcp_server.tool()
def blender_register_instance(
    name: str,
    port: int,
    host: str = "127.0.0.1",
) -> str:
    """Register a new Blender instance at runtime.

    Use when starting additional Blender windows mid-session.
    Open Blender, set the MCP port in the sidebar panel, click Connect,
    then register it here.

    Args:
        name: Instance name (e.g. 'terrain', 'buildings', 'landscape')
        port: TCP port the Blender MCP addon is listening on
        host: Hostname (default 127.0.0.1)
    """
    registry.register(name, port, host)
    return json.dumps({
        "status": "registered",
        "name": name,
        "host": host,
        "port": port,
        "all_instances": [i["name"] for i in registry.list_all()],
    }, indent=2)


@mcp_server.tool()
def blender_unregister_instance(name: str) -> str:
    """Remove a Blender instance from the registry.

    Disconnects the TCP socket and removes the instance.

    Args:
        name: Instance name to remove
    """
    try:
        registry.unregister(name)
        return json.dumps({
            "status": "unregistered",
            "name": name,
            "remaining": [i["name"] for i in registry.list_all()],
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Scene & Object Queries (read-only)
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def blender_get_scene_info(target: str) -> str:
    """Get detailed information about the current Blender scene.

    Returns object count, object list with types/locations, and material count.

    Args:
        target: Instance name (e.g. 'terrain', 'buildings')
    """
    return _route(target, "get_scene_info")


@mcp_server.tool()
def blender_get_object_info(
    target: str,
    object_name: str,
) -> str:
    """Get detailed info about a specific object by name.

    Returns mesh data, transforms, modifiers, materials, etc.

    Args:
        target: Instance name
        object_name: Name of the Blender object
    """
    return _route(target, "get_object_info", {"object_name": object_name})


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Viewport
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def blender_get_viewport_screenshot(target: str) -> str:
    """Capture the current 3D viewport as a screenshot.

    Returns base64-encoded image data.

    Args:
        target: Instance name
    """
    return _route(target, "get_viewport_screenshot")


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Code Execution (the power tool)
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def blender_execute_code(
    target: str,
    code: str,
) -> str:
    """Execute Python code in a Blender instance.

    This is the most versatile tool — any Blender operation can be done
    via bpy. The code runs in Blender's Python environment with full
    access to the bpy API.

    Use this for:
    - Creating/modifying geometry
    - Setting up materials and shaders
    - Configuring the scene (camera, lighting, render)
    - Importing/exporting files
    - Any operation not covered by other tools

    Args:
        target: Instance name
        code: Python code to execute (has access to bpy and all Blender modules)
    """
    return _route(target, "execute_code", {"code": code})


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — PolyHaven Assets
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def blender_get_polyhaven_status(target: str) -> str:
    """Check if PolyHaven integration is enabled in the target Blender instance.

    Args:
        target: Instance name
    """
    return _route(target, "get_polyhaven_status")


@mcp_server.tool()
def blender_get_polyhaven_categories(target: str) -> str:
    """Get available PolyHaven asset categories.

    Requires PolyHaven to be enabled in Blender's MCP panel.

    Args:
        target: Instance name
    """
    return _route(target, "get_polyhaven_categories")


@mcp_server.tool()
def blender_search_polyhaven_assets(
    target: str,
    asset_type: str,
    categories: Optional[str] = None,
    search_query: Optional[str] = None,
) -> str:
    """Search for assets on PolyHaven (HDRIs, textures, models).

    Args:
        target: Instance name
        asset_type: Type of asset — 'hdris', 'textures', or 'models'
        categories: Comma-separated category filter
        search_query: Search term
    """
    params: Dict[str, Any] = {"asset_type": asset_type}
    if categories:
        params["categories"] = categories
    if search_query:
        params["search_query"] = search_query
    return _route(target, "search_polyhaven_assets", params)


@mcp_server.tool()
def blender_download_polyhaven_asset(
    target: str,
    asset_name: str,
    asset_type: str,
    resolution: str = "1k",
) -> str:
    """Download and apply a PolyHaven asset.

    Args:
        target: Instance name
        asset_name: Name of the asset on PolyHaven
        asset_type: Type — 'hdris', 'textures', or 'models'
        resolution: Resolution (e.g. '1k', '2k', '4k')
    """
    return _route(target, "download_polyhaven_asset", {
        "asset_name": asset_name,
        "asset_type": asset_type,
        "resolution": resolution,
    })


@mcp_server.tool()
def blender_set_texture(
    target: str,
    object_name: str,
    texture_path: str,
) -> str:
    """Apply a texture to an object.

    Args:
        target: Instance name
        object_name: Name of the object to texture
        texture_path: Path to texture file or PolyHaven texture name
    """
    return _route(target, "set_texture", {
        "object_name": object_name,
        "texture_path": texture_path,
    })


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Sketchfab
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def blender_get_sketchfab_status(target: str) -> str:
    """Check if Sketchfab integration is enabled.

    Args:
        target: Instance name
    """
    return _route(target, "get_sketchfab_status")


@mcp_server.tool()
def blender_search_sketchfab_models(
    target: str,
    query: str,
    downloadable: bool = True,
) -> str:
    """Search for 3D models on Sketchfab.

    Args:
        target: Instance name
        query: Search term
        downloadable: Only show downloadable models (default True)
    """
    return _route(target, "search_sketchfab_models", {
        "query": query,
        "downloadable": downloadable,
    })


@mcp_server.tool()
def blender_get_sketchfab_model_preview(
    target: str,
    model_uid: str,
) -> str:
    """Get preview/details for a Sketchfab model.

    Args:
        target: Instance name
        model_uid: Sketchfab model UID
    """
    return _route(target, "get_sketchfab_model_preview", {"model_uid": model_uid})


@mcp_server.tool()
def blender_download_sketchfab_model(
    target: str,
    model_uid: str,
) -> str:
    """Download and import a Sketchfab model into Blender.

    Args:
        target: Instance name
        model_uid: Sketchfab model UID
    """
    return _route(target, "download_sketchfab_model", {"model_uid": model_uid})


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Hyper3D / Rodin (AI model generation)
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def blender_get_hyper3d_status(target: str) -> str:
    """Check if Hyper3D/Rodin integration is enabled.

    Args:
        target: Instance name
    """
    return _route(target, "get_hyper3d_status")


@mcp_server.tool()
def blender_generate_hyper3d_model_via_text(
    target: str,
    prompt: str,
) -> str:
    """Generate a 3D model from a text prompt using Hyper3D/Rodin.

    Args:
        target: Instance name
        prompt: Text description of the 3D model to generate
    """
    return _route(target, "create_rodin_job", {"prompt": prompt})


@mcp_server.tool()
def blender_generate_hyper3d_model_via_images(
    target: str,
    image_paths: List[str],
    prompt: Optional[str] = None,
) -> str:
    """Generate a 3D model from images using Hyper3D/Rodin.

    Args:
        target: Instance name
        image_paths: List of image file paths
        prompt: Optional text prompt to guide generation
    """
    params: Dict[str, Any] = {"image_paths": image_paths}
    if prompt:
        params["prompt"] = prompt
    return _route(target, "create_rodin_job", params)


@mcp_server.tool()
def blender_poll_rodin_job_status(
    target: str,
    job_id: str,
) -> str:
    """Check the status of a Rodin/Hyper3D generation job.

    Args:
        target: Instance name
        job_id: The job ID returned from generate commands
    """
    return _route(target, "poll_rodin_job_status", {"job_id": job_id})


@mcp_server.tool()
def blender_import_generated_asset(
    target: str,
    job_id: str,
) -> str:
    """Import a completed Hyper3D/Rodin generated model into Blender.

    Args:
        target: Instance name
        job_id: The completed job ID
    """
    return _route(target, "import_generated_asset", {"job_id": job_id})


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Hunyuan3D (AI model generation)
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def blender_get_hunyuan3d_status(target: str) -> str:
    """Check if Hunyuan3D integration is enabled.

    Args:
        target: Instance name
    """
    return _route(target, "get_hunyuan3d_status")


@mcp_server.tool()
def blender_generate_hunyuan3d_model(
    target: str,
    prompt: str,
    image_path: Optional[str] = None,
) -> str:
    """Generate a 3D model using Hunyuan3D.

    Args:
        target: Instance name
        prompt: Text description
        image_path: Optional reference image path
    """
    params: Dict[str, Any] = {"prompt": prompt}
    if image_path:
        params["image_path"] = image_path
    return _route(target, "create_hunyuan_job", params)


@mcp_server.tool()
def blender_poll_hunyuan_job_status(
    target: str,
    job_id: str,
) -> str:
    """Check the status of a Hunyuan3D generation job.

    Args:
        target: Instance name
        job_id: The job ID
    """
    return _route(target, "poll_hunyuan_job_status", {"job_id": job_id})


@mcp_server.tool()
def blender_import_generated_asset_hunyuan(
    target: str,
    job_id: str,
) -> str:
    """Import a completed Hunyuan3D model into Blender.

    Args:
        target: Instance name
        job_id: The completed job ID
    """
    return _route(target, "import_generated_asset_hunyuan", {"job_id": job_id})


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Generic Passthrough
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def blender_command(
    target: str,
    command_type: str,
    params: Optional[Dict[str, Any]] = None,
) -> str:
    """Send any command to a Blender instance (generic passthrough).

    Use this for commands that don't have dedicated router tools,
    or when you need full control over the command parameters.

    Supported command types:
        get_scene_info, get_object_info, get_viewport_screenshot,
        execute_code, get_polyhaven_categories, search_polyhaven_assets,
        download_polyhaven_asset, set_texture, search_sketchfab_models,
        get_sketchfab_model_preview, download_sketchfab_model,
        create_rodin_job, poll_rodin_job_status, import_generated_asset,
        create_hunyuan_job, poll_hunyuan_job_status, import_generated_asset_hunyuan

    Args:
        target: Instance name
        command_type: The command type string (see list above)
        params: Command parameters as a dict
    """
    return _route(target, command_type, params)


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Cross-Instance Transfer
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def blender_transfer_geometry(
    source: str,
    destination: str,
    source_collection: Optional[str] = None,
    destination_collection: Optional[str] = None,
    file_format: str = "fbx",
) -> str:
    """Transfer geometry from one Blender instance to another.

    Exports objects from the source instance to a temp file,
    then imports them into the destination instance. This is the key
    tool for agent team coordination — when one specialist finishes
    geometry that another needs.

    Args:
        source: Source instance name
        destination: Destination instance name
        source_collection: Collection to export from source (None = all visible)
        destination_collection: Collection to import into (None = Scene Collection)
        file_format: Export format — 'fbx' (default), 'obj', or 'glb'
    """
    import tempfile as _tempfile
    suffix_map = {"fbx": ".fbx", "obj": ".obj", "glb": ".glb"}
    suffix = suffix_map.get(file_format, ".fbx")
    tmp_path = _tempfile.mktemp(suffix=suffix, prefix="blender_transfer_")

    # Step 1: Export from source
    if source_collection:
        export_code = f"""
import bpy

# Select objects in the collection
col = bpy.data.collections.get("{source_collection}")
if col:
    bpy.ops.object.select_all(action='DESELECT')
    for obj in col.objects:
        obj.select_set(True)
    count = len(col.objects)
    bpy.ops.export_scene.{file_format}(filepath="{tmp_path}", use_selection=True)
    print(f"Exported {{count}} objects from collection '{source_collection}'")
else:
    print("Collection '{source_collection}' not found")
"""
    else:
        export_code = f"""
import bpy
bpy.ops.object.select_all(action='SELECT')
count = len(bpy.context.selected_objects)
bpy.ops.export_scene.{file_format}(filepath="{tmp_path}", use_selection=True)
print(f"Exported {{count}} objects")
"""

    export_result = _route(source, "execute_code", {"code": export_code})

    # Check for export errors
    try:
        export_data = json.loads(export_result)
        if "error" in export_data:
            return json.dumps({
                "status": "error",
                "step": "export",
                "detail": export_data["error"],
            }, indent=2)
    except json.JSONDecodeError:
        pass

    # Step 2: Import into destination
    if destination_collection:
        import_code = f"""
import bpy

# Create collection if needed
if "{destination_collection}" not in bpy.data.collections:
    col = bpy.data.collections.new("{destination_collection}")
    bpy.context.scene.collection.children.link(col)

# Import
before = set(bpy.data.objects.keys())
bpy.ops.import_scene.{file_format}(filepath="{tmp_path}")
after = set(bpy.data.objects.keys())
new_objects = after - before

# Move new objects to destination collection
col = bpy.data.collections["{destination_collection}"]
for name in new_objects:
    obj = bpy.data.objects[name]
    for c in obj.users_collection:
        c.objects.unlink(obj)
    col.objects.link(obj)

print(f"Imported {{len(new_objects)}} objects into '{destination_collection}'")
"""
    else:
        import_code = f"""
import bpy
before = set(bpy.data.objects.keys())
bpy.ops.import_scene.{file_format}(filepath="{tmp_path}")
after = set(bpy.data.objects.keys())
print(f"Imported {{len(after - before)}} objects")
"""

    import_result = _route(destination, "execute_code", {"code": import_code})

    # Clean up temp file
    try:
        os.unlink(tmp_path)
    except OSError:
        pass

    return json.dumps({
        "status": "success",
        "source": source,
        "destination": destination,
        "source_collection": source_collection,
        "destination_collection": destination_collection,
        "format": file_format,
        "export_result": export_result,
        "import_result": import_result,
    }, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp_server.run()
