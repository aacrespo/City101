# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp[cli]>=1.0", "pydantic>=2.0"]
# ///
"""
Rhino Router MCP — Multi-instance TCP proxy for parallel Rhino modeling.

Routes MCP tool calls to multiple Rhino instances via raw TCP sockets,
matching the rhinomcp plugin's wire protocol exactly:
  Request:  {"type": "command_name", "params": {...}}
  Response: {"status": "success|error", "result": {...}}

Architecture:
    Claude Code ──[stdio/MCP]──> Router ──[TCP:9001]──> Rhino 1 (shell.3dm)
                                        ──[TCP:9002]──> Rhino 2 (mep.3dm)
                                        ──[TCP:9003]──> Rhino 3 (bridge.3dm)

Every tool includes a `target` parameter that selects which Rhino instance
receives the command. Agent teams share this single MCP server but each
agent routes to its own Rhino instance.

Setup:
    1. Start Rhino instances with MCP plugin on different ports
       (requires the port fix: `mcpstart 9001`, `mcpstart 9002`, etc.)
    2. Set env var: RHINO_INSTANCES='{"shell": 9001, "mep": 9002}'
    3. Run: uv run experiments/rhino\\ mcp\\ server/rhino_router_mcp.py

.mcp.json config:
    {
      "mcpServers": {
        "rhino_router": {
          "command": "uv",
          "args": ["run", "experiments/rhino mcp server/rhino_router_mcp.py"],
          "env": {
            "RHINO_INSTANCES": "{\"shell\": 9001, \"mep\": 9002}"
          }
        }
      }
    }
"""

import json
import logging
import os
import socket
import tempfile
import threading
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP, Context, Image

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

ROUTER_TIMEOUT = float(os.getenv("RHINO_ROUTER_TIMEOUT", "30.0"))
ROUTER_LOG_LEVEL = os.getenv("RHINO_ROUTER_LOG_LEVEL", "INFO")

logging.basicConfig(
    level=getattr(logging, ROUTER_LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
logger = logging.getLogger("rhino_router")


# ---------------------------------------------------------------------------
# TCP Connection — based on rhinomcp's RhinoConnection
# ---------------------------------------------------------------------------

class RhinoInstanceConnection:
    """TCP socket connection to a single Rhino MCP plugin instance.

    Thread-safe: a per-instance lock serializes commands to the same Rhino
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

        Matches rhinomcp's receive_full_response — reads chunks until a
        valid JSON object is detected via json.JSONDecoder.raw_decode().
        """
        accumulated = ""
        decoder = json.JSONDecoder()
        assert self._sock is not None
        self._sock.settimeout(ROUTER_TIMEOUT)

        while True:
            try:
                chunk = self._sock.recv(8192)
            except socket.timeout:
                break
            except (ConnectionError, BrokenPipeError, ConnectionResetError) as e:
                raise ConnectionError(f"Socket error during receive: {e}")

            if not chunk:
                break

            accumulated += chunk.decode("utf-8")

            # Optimization: only attempt JSON parse when we see a closing brace
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
        """Send a command to this Rhino instance and return the result.

        Thread-safe — acquires per-instance lock. Reconnects on failure.
        """
        with self._lock:
            # Connect on demand
            if self._sock is None and not self.connect():
                raise ConnectionError(
                    f"Cannot connect to Rhino instance '{self.name}' "
                    f"at {self.host}:{self.port}. Is Rhino running with "
                    f"'mcpstart {self.port}'?"
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
                    raise Exception(response.get("message", "Unknown error from Rhino"))

                return response.get("result", {})

            except socket.timeout:
                self._sock = None
                raise Exception(
                    f"[{self.name}] Timeout ({ROUTER_TIMEOUT}s) waiting for Rhino. "
                    f"Try simplifying the operation or increasing RHINO_ROUTER_TIMEOUT."
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
        self._instances: Dict[str, RhinoInstanceConnection] = {}
        self._lock = threading.Lock()

    def register(self, name: str, port: int, host: str = "127.0.0.1"):
        with self._lock:
            if name in self._instances:
                self._instances[name].disconnect()
            self._instances[name] = RhinoInstanceConnection(name, host, port)
            logger.info(f"Registered instance '{name}' -> {host}:{port}")

    def get(self, name: str) -> RhinoInstanceConnection:
        with self._lock:
            if name not in self._instances:
                available = ", ".join(sorted(self._instances.keys())) or "(none)"
                raise KeyError(
                    f"Unknown instance '{name}'. Available: {available}. "
                    f"Use rhino_register_instance to add it."
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
    """Load instances from RHINO_INSTANCES env var.

    Format: JSON object mapping names to port numbers.
    Example: {"shell": 9001, "mep": 9002, "bridge": 9003}
    """
    raw = os.environ.get("RHINO_INSTANCES", "")
    if not raw:
        logger.warning("RHINO_INSTANCES not set — no instances registered. "
                       "Use rhino_register_instance to add them at runtime.")
        return

    try:
        mapping = json.loads(raw)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid RHINO_INSTANCES JSON: {e}")
        return

    for name, port in mapping.items():
        try:
            registry.register(name, int(port))
        except (ValueError, TypeError) as e:
            logger.error(f"Invalid port for '{name}': {port} ({e})")


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp_server = FastMCP("rhino_router")

# Load instances at import time (before server starts)
_load_instances_from_env()


# ---------------------------------------------------------------------------
# Routing helper
# ---------------------------------------------------------------------------

def _route(target: str, command_type: str, params: Dict[str, Any] | None = None) -> str:
    """Route a command to a Rhino instance, return JSON string result."""
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
def rhino_list_instances() -> str:
    """List all registered Rhino instances and their connection status.

    Use this first to discover available targets before routing commands.
    Instances are registered via RHINO_INSTANCES env var or rhino_register_instance.
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
def rhino_register_instance(
    name: str,
    port: int,
    host: str = "127.0.0.1",
) -> str:
    """Register a new Rhino instance at runtime.

    Use when starting additional Rhino windows mid-session.
    Start Rhino, run `mcpstart <port>`, then register it here.

    Args:
        name: Instance name (e.g. 'landscape', 'structure')
        port: TCP port the Rhino MCP plugin is listening on
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
def rhino_unregister_instance(name: str) -> str:
    """Remove a Rhino instance from the registry.

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
# TOOLS — Document & Object Queries (read-only)
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def rhino_get_document_summary(target: str) -> str:
    """Get a summary of the Rhino document in the target instance.

    Returns layer info, object counts, file name, units, etc.

    Args:
        target: Instance name (e.g. 'shell', 'mep')
    """
    return _route(target, "get_document_summary")


@mcp_server.tool()
def rhino_get_objects(
    target: str,
    layer_filter: Optional[str] = None,
    type_filter: Optional[str] = None,
    bbox_filter: Optional[List[List[float]]] = None,
    include_geometry: bool = True,
    offset: int = 0,
    limit: int = 50,
) -> str:
    """Get objects from a Rhino instance with optional filters.

    Args:
        target: Instance name
        layer_filter: Filter by layer name
        type_filter: Filter by type (e.g. 'BREP', 'CURVE', 'MESH')
        bbox_filter: Bounding box filter [[min_x, min_y, min_z], [max_x, max_y, max_z]]
        include_geometry: Include geometry data in response
        offset: Pagination offset
        limit: Max objects to return (default 50)
    """
    params: Dict[str, Any] = {
        "offset": offset,
        "limit": limit,
        "include_geometry": include_geometry,
    }
    if layer_filter:
        params["layer_filter"] = layer_filter
    if type_filter:
        params["type_filter"] = type_filter.upper()
    if bbox_filter:
        params["bbox_filter"] = bbox_filter

    return _route(target, "get_objects", params)


@mcp_server.tool()
def rhino_get_object_info(
    target: str,
    id: Optional[str] = None,
    name: Optional[str] = None,
) -> str:
    """Get detailed info about a specific object by ID or name.

    Args:
        target: Instance name
        id: Object GUID
        name: Object name (id takes precedence if both provided)
    """
    params: Dict[str, Any] = {}
    if id:
        params["id"] = id
    if name:
        params["name"] = name
    return _route(target, "get_object_info", params)


@mcp_server.tool()
def rhino_get_selected_objects_info(
    target: str,
    include_attributes: bool = False,
) -> str:
    """Get info about currently selected objects in the target instance.

    Args:
        target: Instance name
        include_attributes: Include detailed attribute data
    """
    return _route(target, "get_selected_objects_info", {"include_attributes": include_attributes})


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Object Creation & Modification
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def rhino_create_object(
    target: str,
    type: str,
    params: Optional[Dict[str, Any]] = None,
    name: Optional[str] = None,
    layer: Optional[str] = None,
    color: Optional[List[int]] = None,
    translation: Optional[List[float]] = None,
    rotation: Optional[List[float]] = None,
    scale: Optional[List[float]] = None,
) -> str:
    """Create a geometric object in a Rhino instance.

    Args:
        target: Instance name
        type: Object type — POINT, LINE, POLYLINE, CIRCLE, ARC, ELLIPSE,
              RECTANGLE, POLYGON, SPHERE, BOX, CYLINDER, CONE, TORUS,
              TEXT, TEXTDOT, SURFACE, CURVE, MESH
        params: Type-specific parameters (e.g. {"center": [0,0,0], "radius": 5} for CIRCLE)
        name: Optional object name
        layer: Optional layer name (will set as current layer)
        color: Optional RGB color [r, g, b]
        translation: Optional translation [x, y, z]
        rotation: Optional rotation [rx, ry, rz] in degrees
        scale: Optional scale [sx, sy, sz]
    """
    cmd_params: Dict[str, Any] = {"type": type}
    if params:
        cmd_params["params"] = params
    if name:
        cmd_params["name"] = name
    if color:
        cmd_params["color"] = color
    if translation:
        cmd_params["translation"] = translation
    if rotation:
        cmd_params["rotation"] = rotation
    if scale:
        cmd_params["scale"] = scale

    # Set layer before creating if specified
    if layer:
        _route(target, "get_or_set_current_layer", {"name": layer})

    return _route(target, "create_object", cmd_params)


@mcp_server.tool()
def rhino_create_objects(
    target: str,
    objects: List[Dict[str, Any]],
    layer: Optional[str] = None,
) -> str:
    """Create multiple objects in a single batch call.

    Args:
        target: Instance name
        objects: List of object dicts, each with 'type', 'params', optional 'name', 'color', etc.
        layer: Optional layer — sets current layer before creating
    """
    # rhinomcp expects {key: object_dict} format
    cmd_params: Dict[str, Any] = {}
    for i, obj in enumerate(objects):
        key = obj.get("name", f"object_{i}")
        cmd_params[key] = obj

    if layer:
        _route(target, "get_or_set_current_layer", {"name": layer})

    return _route(target, "create_objects", cmd_params)


@mcp_server.tool()
def rhino_modify_object(
    target: str,
    id: Optional[str] = None,
    name: Optional[str] = None,
    new_name: Optional[str] = None,
    new_color: Optional[List[int]] = None,
    translation: Optional[List[float]] = None,
    rotation: Optional[List[float]] = None,
    scale: Optional[List[float]] = None,
    visible: Optional[bool] = None,
) -> str:
    """Modify an existing object's properties.

    Args:
        target: Instance name
        id: Object GUID to modify
        name: Object name to modify (id takes precedence)
        new_name: New name for the object
        new_color: New RGB color [r, g, b]
        translation: Translation to apply [x, y, z]
        rotation: Rotation to apply [rx, ry, rz] in degrees
        scale: Scale to apply [sx, sy, sz]
        visible: Set visibility
    """
    params: Dict[str, Any] = {}
    if id:
        params["id"] = id
    if name:
        params["name"] = name
    if new_name:
        params["new_name"] = new_name
    if new_color:
        params["new_color"] = new_color
    if translation:
        params["translation"] = translation
    if rotation:
        params["rotation"] = rotation
    if scale:
        params["scale"] = scale
    if visible is not None:
        params["visible"] = visible

    return _route(target, "modify_object", params)


@mcp_server.tool()
def rhino_modify_objects(
    target: str,
    objects: List[Dict[str, Any]],
    all: bool = False,
) -> str:
    """Modify multiple objects in a batch call.

    Args:
        target: Instance name
        objects: List of modification dicts, each with 'id' and optional
                 'new_color', 'translation', 'rotation', 'scale', 'visible'
        all: If True, apply modifications to all objects in the document
    """
    params: Dict[str, Any] = {"objects": objects}
    if all:
        params["all"] = True
    return _route(target, "modify_objects", params)


@mcp_server.tool()
def rhino_delete_object(
    target: str,
    id: Optional[str] = None,
    name: Optional[str] = None,
    all: bool = False,
) -> str:
    """Delete an object from a Rhino instance.

    Args:
        target: Instance name
        id: Object GUID to delete
        name: Object name to delete
        all: Delete all objects (use with caution)
    """
    params: Dict[str, Any] = {}
    if id:
        params["id"] = id
    if name:
        params["name"] = name
    if all:
        params["all"] = True
    return _route(target, "delete_object", params)


@mcp_server.tool()
def rhino_select_objects(
    target: str,
    filters: Optional[Dict[str, List[Any]]] = None,
    filters_type: str = "and",
) -> str:
    """Select objects in a Rhino instance by filters.

    Args:
        target: Instance name
        filters: Filter dict (e.g. {"layer": ["Default"], "type": ["BREP"]})
        filters_type: How to combine filters — 'and' or 'or'
    """
    params: Dict[str, Any] = {
        "filters": filters or {},
        "filters_type": filters_type,
    }
    return _route(target, "select_objects", params)


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Code Execution
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def rhino_execute_python_code(
    target: str,
    code: str,
) -> str:
    """Execute RhinoScript Python code on a Rhino instance.

    This is the most versatile tool — any Rhino operation can be done
    via rhinoscriptsyntax (rs) or RhinoCommon. The code runs in Rhino's
    Python environment with access to:
      - rhinoscriptsyntax as rs
      - Rhino.Geometry, Rhino.RhinoDoc, etc.
      - scriptcontext

    Args:
        target: Instance name
        code: Python code to execute (can use 'import rhinoscriptsyntax as rs')
    """
    return _route(target, "execute_rhinoscript_python_code", {"code": code})


@mcp_server.tool()
def rhino_execute_csharp_code(
    target: str,
    code: str,
) -> str:
    """Execute RhinoCommon C# code on a Rhino instance.

    Runs C# code with access to the full RhinoCommon API.

    Args:
        target: Instance name
        code: C# code to execute
    """
    return _route(target, "execute_rhinocommon_csharp_code", {"code": code})


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Layers
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def rhino_create_layer(
    target: str,
    name: str,
    color: Optional[List[int]] = None,
    parent: Optional[str] = None,
) -> str:
    """Create a new layer in a Rhino instance.

    Args:
        target: Instance name
        name: Layer name (use :: for sublayers, e.g. 'Building::Shell')
        color: Optional RGB color [r, g, b]
        parent: Optional parent layer name
    """
    params: Dict[str, Any] = {"name": name}
    if color:
        params["color"] = color
    if parent:
        params["parent"] = parent
    return _route(target, "create_layer", params)


@mcp_server.tool()
def rhino_get_or_set_current_layer(
    target: str,
    name: Optional[str] = None,
    guid: Optional[str] = None,
) -> str:
    """Get or set the current (active) layer.

    Call with no args to get the current layer. Pass name or guid to set it.

    Args:
        target: Instance name
        name: Layer name to set as current
        guid: Layer GUID to set as current
    """
    params: Dict[str, Any] = {}
    if name:
        params["name"] = name
    if guid:
        params["guid"] = guid
    return _route(target, "get_or_set_current_layer", params)


@mcp_server.tool()
def rhino_delete_layer(
    target: str,
    name: Optional[str] = None,
    guid: Optional[str] = None,
) -> str:
    """Delete a layer from a Rhino instance.

    Args:
        target: Instance name
        name: Layer name to delete
        guid: Layer GUID to delete
    """
    params: Dict[str, Any] = {}
    if name:
        params["name"] = name
    if guid:
        params["guid"] = guid
    return _route(target, "delete_layer", params)


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Viewport
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def rhino_capture_viewport(
    target: str,
    viewport: str = "active",
    width: int = 800,
    height: int = 600,
    show_grid: bool = True,
    show_axes: bool = True,
    show_cplane_axes: bool = False,
    zoom_to_fit: bool = False,
) -> str:
    """Capture the viewport of a Rhino instance as an image.

    Args:
        target: Instance name
        viewport: Viewport name or 'active' (default)
        width: Image width in pixels
        height: Image height in pixels
        show_grid: Show the grid
        show_axes: Show the world axes
        show_cplane_axes: Show construction plane axes
        zoom_to_fit: Zoom to fit all objects before capture
    """
    return _route(target, "capture_viewport", {
        "viewport": viewport,
        "width": width,
        "height": height,
        "show_grid": show_grid,
        "show_axes": show_axes,
        "show_cplane_axes": show_cplane_axes,
        "zoom_to_fit": zoom_to_fit,
    })


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Boolean Operations
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def rhino_boolean_union(
    target: str,
    object_ids: List[str],
    delete_sources: bool = True,
    name: Optional[str] = None,
) -> str:
    """Boolean union of multiple objects.

    Args:
        target: Instance name
        object_ids: List of object GUIDs to union
        delete_sources: Delete source objects after union (default True)
        name: Optional name for the result
    """
    params: Dict[str, Any] = {
        "object_ids": object_ids,
        "delete_sources": delete_sources,
    }
    if name:
        params["name"] = name
    return _route(target, "boolean_union", params)


@mcp_server.tool()
def rhino_boolean_difference(
    target: str,
    base_id: str,
    subtract_ids: List[str],
    delete_sources: bool = True,
    name: Optional[str] = None,
) -> str:
    """Boolean difference — subtract objects from a base.

    Args:
        target: Instance name
        base_id: GUID of the base object
        subtract_ids: GUIDs of objects to subtract
        delete_sources: Delete source objects (default True)
        name: Optional name for the result
    """
    params: Dict[str, Any] = {
        "base_id": base_id,
        "subtract_ids": subtract_ids,
        "delete_sources": delete_sources,
    }
    if name:
        params["name"] = name
    return _route(target, "boolean_difference", params)


@mcp_server.tool()
def rhino_boolean_intersection(
    target: str,
    object_ids: List[str],
    delete_sources: bool = True,
    name: Optional[str] = None,
) -> str:
    """Boolean intersection of multiple objects.

    Args:
        target: Instance name
        object_ids: List of object GUIDs to intersect
        delete_sources: Delete source objects (default True)
        name: Optional name for the result
    """
    params: Dict[str, Any] = {
        "object_ids": object_ids,
        "delete_sources": delete_sources,
    }
    if name:
        params["name"] = name
    return _route(target, "boolean_intersection", params)


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Advanced Geometry
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def rhino_loft(
    target: str,
    curve_ids: List[str],
    name: Optional[str] = None,
    closed: bool = False,
    loft_type: int = 0,
) -> str:
    """Create a loft surface through multiple curves.

    Args:
        target: Instance name
        curve_ids: List of curve GUIDs to loft through (minimum 2)
        name: Optional name for the result
        closed: Create a closed loft
        loft_type: 0=Normal, 1=Loose, 2=Tight, 3=Straight, 4=Developable
    """
    params: Dict[str, Any] = {
        "curve_ids": curve_ids,
        "closed": closed,
        "loft_type": loft_type,
    }
    if name:
        params["name"] = name
    return _route(target, "loft", params)


@mcp_server.tool()
def rhino_extrude_curve(
    target: str,
    curve_id: str,
    direction: List[float],
    name: Optional[str] = None,
    cap: bool = True,
) -> str:
    """Extrude a curve along a direction vector.

    Args:
        target: Instance name
        curve_id: Curve GUID to extrude
        direction: Extrusion direction [x, y, z] (e.g. [0, 0, 10] for 10 units up)
        name: Optional name for the result
        cap: Cap the ends if curve is closed (default True)
    """
    params: Dict[str, Any] = {
        "curve_id": curve_id,
        "direction": direction,
        "cap": cap,
    }
    if name:
        params["name"] = name
    return _route(target, "extrude_curve", params)


@mcp_server.tool()
def rhino_sweep1(
    target: str,
    rail_id: str,
    profile_ids: List[str],
    name: Optional[str] = None,
    closed: bool = False,
) -> str:
    """Sweep profile curves along a rail curve.

    Args:
        target: Instance name
        rail_id: Rail curve GUID
        profile_ids: Profile curve GUIDs to sweep
        name: Optional name for the result
        closed: Create a closed sweep
    """
    params: Dict[str, Any] = {
        "rail_id": rail_id,
        "profile_ids": profile_ids,
        "closed": closed,
    }
    if name:
        params["name"] = name
    return _route(target, "sweep1", params)


@mcp_server.tool()
def rhino_offset_curve(
    target: str,
    curve_id: str,
    distance: float,
    name: Optional[str] = None,
    plane: Optional[List[float]] = None,
    corner_style: int = 1,
) -> str:
    """Offset a curve by a distance.

    Args:
        target: Instance name
        curve_id: Curve GUID to offset
        distance: Offset distance (positive = one side, negative = other)
        name: Optional name for the result
        plane: Optional plane normal [x, y, z] for offset direction
        corner_style: 0=None, 1=Sharp, 2=Round, 3=Smooth, 4=Chamfer
    """
    params: Dict[str, Any] = {
        "curve_id": curve_id,
        "distance": distance,
        "corner_style": corner_style,
    }
    if name:
        params["name"] = name
    if plane:
        params["plane"] = plane
    return _route(target, "offset_curve", params)


@mcp_server.tool()
def rhino_pipe(
    target: str,
    curve_id: str,
    radius: float,
    name: Optional[str] = None,
    cap: bool = True,
    fit_rail: bool = False,
) -> str:
    """Create a pipe (tube) along a curve.

    Args:
        target: Instance name
        curve_id: Curve GUID to pipe along
        radius: Pipe radius
        name: Optional name for the result
        cap: Cap the pipe ends (default True)
        fit_rail: Fit pipe more closely to rail
    """
    params: Dict[str, Any] = {
        "curve_id": curve_id,
        "radius": radius,
        "cap": cap,
        "fit_rail": fit_rail,
    }
    if name:
        params["name"] = name
    return _route(target, "pipe", params)


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Undo / Redo
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def rhino_undo(target: str, steps: int = 1) -> str:
    """Undo recent operations on a Rhino instance.

    Args:
        target: Instance name
        steps: Number of steps to undo (default 1)
    """
    return _route(target, "undo", {"steps": steps})


@mcp_server.tool()
def rhino_redo(target: str, steps: int = 1) -> str:
    """Redo recently undone operations.

    Args:
        target: Instance name
        steps: Number of steps to redo (default 1)
    """
    return _route(target, "redo", {"steps": steps})


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Generic Passthrough
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def rhino_command(
    target: str,
    command_type: str,
    params: Optional[Dict[str, Any]] = None,
) -> str:
    """Send any command to a Rhino instance (generic passthrough).

    Use this for commands that don't have dedicated router tools,
    or when you need full control over the command parameters.

    Supported command types:
        get_document_summary, get_objects, get_object_info,
        get_selected_objects_info, create_object, create_objects,
        delete_object, modify_object, modify_objects,
        execute_rhinoscript_python_code, execute_rhinocommon_csharp_code,
        select_objects, create_layer, get_or_set_current_layer, delete_layer,
        undo, redo, capture_viewport,
        boolean_union, boolean_difference, boolean_intersection,
        loft, extrude_curve, sweep1, offset_curve, pipe,
        project_curve, intersect_curves, split_curve

    Args:
        target: Instance name
        command_type: The command type string (see list above)
        params: Command parameters as a dict
    """
    return _route(target, command_type, params)


# ═══════════════════════════════════════════════════════════════════════════
# TOOLS — Cross-Instance Geometry Transfer
# ═══════════════════════════════════════════════════════════════════════════

@mcp_server.tool()
def rhino_transfer_geometry(
    source: str,
    destination: str,
    source_layer: Optional[str] = None,
    destination_layer: Optional[str] = None,
) -> str:
    """Transfer geometry from one Rhino instance to another.

    Exports objects from the source instance to a temp .3dm file,
    then imports them into the destination instance. This is the key
    tool for agent team coordination — when one specialist finishes
    geometry that another needs.

    Example: Shell modeler finishes the building envelope, transfers
    it to the MEP agent's instance for pipe routing.

    Args:
        source: Source instance name
        destination: Destination instance name
        source_layer: Layer to export from source (None = all visible)
        destination_layer: Layer to import into on destination (None = keep original layers)
    """
    tmp_path = tempfile.mktemp(suffix=".3dm", prefix="rhino_transfer_")

    # Step 1: Export from source using RhinoScript
    if source_layer:
        export_code = f"""
import rhinoscriptsyntax as rs
objs = rs.ObjectsByLayer("{source_layer}")
if objs:
    rs.UnselectAllObjects()
    rs.SelectObjects(objs)
    rs.Command('-_Export "{tmp_path}" _Enter', False)
    rs.UnselectAllObjects()
    print(f"Exported {{len(objs)}} objects from layer '{source_layer}'")
else:
    print("No objects found on layer '{source_layer}'")
"""
    else:
        export_code = f"""
import rhinoscriptsyntax as rs
objs = rs.AllObjects()
if objs:
    rs.UnselectAllObjects()
    rs.SelectObjects(objs)
    rs.Command('-_Export "{tmp_path}" _Enter', False)
    rs.UnselectAllObjects()
    print(f"Exported {{len(objs)}} objects")
else:
    print("No objects in document")
"""

    export_result = _route(source, "execute_rhinoscript_python_code", {"code": export_code})

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

    # Step 2: Import into destination using RhinoScript
    if destination_layer:
        import_code = f"""
import rhinoscriptsyntax as rs
# Create destination layer if needed
if not rs.IsLayer("{destination_layer}"):
    rs.AddLayer("{destination_layer}")
rs.CurrentLayer("{destination_layer}")
rs.Command('-_Import "{tmp_path}" _Enter', False)
print(f"Imported geometry to layer '{destination_layer}'")
"""
    else:
        import_code = f"""
import rhinoscriptsyntax as rs
rs.Command('-_Import "{tmp_path}" _Enter', False)
print("Imported geometry (original layers preserved)")
"""

    import_result = _route(destination, "execute_rhinoscript_python_code", {"code": import_code})

    # Clean up temp file
    try:
        os.unlink(tmp_path)
    except OSError:
        pass

    return json.dumps({
        "status": "success",
        "source": source,
        "destination": destination,
        "source_layer": source_layer,
        "destination_layer": destination_layer,
        "tmp_file": tmp_path,
        "export_result": export_result,
        "import_result": import_result,
    }, indent=2)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp_server.run()
