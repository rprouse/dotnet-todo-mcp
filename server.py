import shutil
import subprocess
from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("todo-mcp")


def _run_todo(*args: str) -> str:
    if shutil.which("todo") is None:
        return "Error: todo is not installed. Install with: dotnet tool install -g dotnet-todo"
    result = subprocess.run(["todo", "-p", *args], capture_output=True, text=True)
    return (result.stdout + result.stderr).strip()


@mcp.tool()
def list_todos(
    terms: Annotated[
        list[str] | None,
        Field(description="Filter terms (AND logic). Prefix with - to exclude, e.g. '-home'"),
    ] = None,
) -> str:
    """List pending todos, optionally filtered by terms."""
    args = ["ls"]
    if terms:
        args.extend(terms)
    return _run_todo(*args)


@mcp.tool()
def create_todo(
    title: Annotated[str, Field(description="Task text, including @context tags e.g. 'Fix bug @work'")],
    priority: Annotated[str | None, Field(description="Priority letter A-Z (A=highest). Optional.")] = None,
) -> str:
    """Create a new todo item, optionally with a priority."""
    task = f"({priority.upper()}) {title}" if priority else title
    return _run_todo("add", "-t", task)


@mcp.tool()
def complete_todo(
    item_number: Annotated[int, Field(description="Line number of the task to mark as done")],
) -> str:
    """Mark a todo item as completed."""
    return _run_todo("do", str(item_number))


@mcp.tool()
def delete_todo(
    item_number: Annotated[int, Field(description="Line number of the task to delete")],
) -> str:
    """Delete a todo item."""
    return _run_todo("rm", str(item_number))


@mcp.tool()
def set_priority(
    item_number: Annotated[int, Field(description="Line number of the task")],
    priority: Annotated[str | None, Field(description="Priority letter A-Z, or None to remove priority")],
) -> str:
    """Set or remove the priority of a todo item."""
    if priority is None:
        return _run_todo("dp", str(item_number))
    return _run_todo("pri", str(item_number), priority.upper())


@mcp.tool()
def list_todos_by_priority(
    priorities: Annotated[
        str | None,
        Field(description="Priority or range, e.g. 'A' or 'A-C'"),
    ] = None,
    terms: Annotated[list[str] | None, Field(description="Filter terms")] = None,
) -> str:
    """List todos sorted by priority, optionally filtered."""
    args = ["lsp"]
    if priorities:
        args.append(priorities)
    if terms:
        args.extend(terms)
    return _run_todo(*args)


@mcp.tool()
def list_all_todos(
    terms: Annotated[list[str] | None, Field(description="Filter terms (AND logic)")] = None,
) -> str:
    """List all todos including completed ones."""
    args = ["lsa"]
    if terms:
        args.extend(terms)
    return _run_todo(*args)


@mcp.tool()
def list_contexts() -> str:
    """List all @context tags used across todos."""
    return _run_todo("lsc")


@mcp.tool()
def list_projects() -> str:
    """List all +project tags used across todos."""
    return _run_todo("lspj")


def main():
    mcp.run()


if __name__ == "__main__":
    main()
