"""Single MCP server for MIKE+. Exposes auto-discovered tools over stdio.

Run:  python -m mikeplus_mcp.server        (cwd = repo root, venv python)

The server itself imports neither mikeplus nor mikeio — every tool runs its work
in an isolated worker subprocess (see runtime/worker.py).
"""
from __future__ import annotations

import asyncio
import json

from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

from .registry import discover_tools

_TOOLS = {t.name: t for t in discover_tools()}

server = Server("mike-plus")


@server.list_tools()
async def _list_tools() -> list[types.Tool]:
    return [
        types.Tool(name=t.name, description=t.description, inputSchema=t.input_schema)
        for t in _TOOLS.values()
    ]


@server.call_tool()
async def _call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    tool = _TOOLS.get(name)
    if tool is None:
        raise ValueError(f"Unknown tool: {name}")
    # handlers spawn a subprocess (blocking) — run off the event loop
    result = await asyncio.to_thread(tool.handler, arguments or {})
    text = json.dumps(result, ensure_ascii=False, default=str, indent=2)
    return [types.TextContent(type="text", text=text)]


async def _main() -> None:
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())


def run() -> None:
    asyncio.run(_main())


if __name__ == "__main__":
    run()
