# rhinomcp C# Plugin — Port Fix

Two files need modification in the upstream [jingcheng-chen/rhinomcp](https://github.com/jingcheng-chen/rhinomcp) plugin to support multiple instances.

## File 1: RhinoMCPServerController.cs

```diff
  public static class RhinoMCPServerController
  {
      private static RhinoMCPServer server;

-     public static void StartServer()
+     public static void StartServer(int port = 1999)
      {
          if (server == null)
          {
-             server = new RhinoMCPServer();
+             server = new RhinoMCPServer("127.0.0.1", port);
          }
          server.Start();
      }
```

## File 2: MCPStartCommand.cs

```diff
  [CommandStyle(Style.ScriptRunner)]
  public class MCPStartCommand : Command
  {
      public override string EnglishName => "mcpstart";

      protected override Result RunCommand(RhinoDoc doc, RunMode mode)
      {
+         var gi = new Rhino.Input.Custom.GetInteger();
+         gi.SetCommandPrompt("Port number (default 1999)");
+         gi.SetDefaultInteger(1999);
+         gi.SetLowerLimit(1024, false);
+         gi.SetUpperLimit(65535, false);
+         gi.AcceptNothing(true);
+         var result = gi.Get();
+         int port = (result == Rhino.Input.GetResult.Number) ? gi.Number() : 1999;
+
-         RhinoMCPServerController.StartServer();
+         RhinoMCPServerController.StartServer(port);
+         RhinoApp.WriteLine($"MCP server started on port {port}");
          return Result.Success;
      }
  }
```

## Usage after fix

```
Rhino window 1:  mcpstart 9001
Rhino window 2:  mcpstart 9002
Rhino window 3:  mcpstart 9003
```

Default `mcpstart` (no argument) still uses port 1999 for backward compatibility.

## Build steps

1. Fork `jingcheng-chen/rhinomcp`
2. Apply the two diffs above
3. Open the solution in Visual Studio / Rider
4. Build the RhinoPlugin project
5. Install the resulting .rhp in Rhino (drag-drop or `_PlugInManager`)
6. Test: open two Rhino windows, `mcpstart 9001` in one, `mcpstart 9002` in the other
7. Verify with two Claude Code sessions, each with different `RHINO_MCP_PORT` env var

## Optional: upstream PR

The changes are backward-compatible (default port unchanged). Clean PR candidate.
