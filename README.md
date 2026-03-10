# dotnet-todo-mcp

A FastMCP server that exposes the [`dotnet-todo`](https://github.com/rprouse/dotnet-todo) CLI (a Todo.txt port) as MCP tools, making your todo list accessible to AI assistants via the Model Context Protocol.

## Prerequisites

Install the `todo` CLI (.NET global tool):

```bash
dotnet tool install -g dotnet-todo
```

## Running the Server

**Via uvx** (from PyPI):

```bash
uvx dotnet-todo-mcp
```

**Local development** (from the project directory):

```bash
uv sync
uv run python server.py
```

## Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_todos` | List pending todos, optionally filtered | `terms: list[str] \| None` — filter terms (AND logic, prefix `-` to exclude) |
| `create_todo` | Create a new todo item | `title: str`, `priority: str \| None` — letter A–Z |
| `complete_todo` | Mark a todo as done | `item_number: int` |
| `delete_todo` | Delete a todo | `item_number: int` |
| `set_priority` | Set or remove priority | `item_number: int`, `priority: str \| None` |
| `list_todos_by_priority` | List todos sorted by priority | `priorities: str \| None` (e.g. `"A"` or `"A-C"`), `terms: list[str] \| None` |
| `list_all_todos` | List all todos including completed | `terms: list[str] \| None` |
| `list_contexts` | List all `@context` tags | _(none)_ |
| `list_projects` | List all `+project` tags | _(none)_ |

**Todo item format:** `02 (D) 2023-07-30 Task description @context +project`

## MCP Client Configuration

Add to your MCP client config (e.g. Claude Desktop `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "todo": {
      "command": "uvx",
      "args": [
        "--from",
        "dotnet-todo-mcp",
        "todo-mcp"
      ]
    }
  }
}
```

**Local development** — point at your local clone:

```json
{
  "mcpServers": {
    "todo": {
      "command": "uv",
      "args": ["run", "--project", "/path/to/dotnet-todo-mcp", "todo-mcp"]
    }
  }
}
```

This requires that you run `uv sync` first.
