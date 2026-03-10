from typing import Annotated

from fastmcp import FastMCP
from pydantic import Field

mcp = FastMCP("todo-mcp")


@mcp.tool()
def list_todos() -> list[dict]:
    """List all todos."""
    return []


@mcp.tool()
def create_todo(
    title: Annotated[str, Field(description="The title of the todo item")],
    completed: Annotated[bool, Field(description="Whether the todo is completed")] = False,
) -> dict:
    """Create a new todo item."""
    return {}


def main():
    mcp.run()


if __name__ == "__main__":
    main()
