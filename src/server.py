import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from mcp.server import Server
from mcp.server.stdio import stdio_server

from src.tools import search, transcript

app = Server("youtube-transcript")


@app.list_tools()
async def list_tools():
    return [search.TOOL, transcript.TOOL]


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_videos":
        return await search.handle(arguments)
    if name == "get_transcript":
        return await transcript.handle(arguments)
    raise ValueError(f"Unknown tool: {name}")


async def main():
    async with stdio_server() as (read, write):
        await app.run(read, write, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
