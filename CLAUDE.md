# dotnet-todo-mcp

Python MCP server built with FastMCP. Uses uv for dependency management.

## Commands

```bash
uv sync                          # Install / update dependencies
uv run python server.py          # Run server (stdio mode for MCP)
uvx --from . todo-mcp            # Run via uvx (after uv sync)
```

## Architecture

Single-file FastMCP server. All tools live in `server.py`.

- `mcp = FastMCP("todo-mcp")` — server instance
- Tools use `@mcp.tool()` decorator with `Annotated[T, Field(...)]` for parameter descriptions

## Gotchas

- `hatchling` requires `[tool.hatch.build.targets.wheel] include = ["server.py"]` because the project is a flat module (not a package directory)
- `uv sync` must run before `uvx --from . todo-mcp` to populate `.venv`
