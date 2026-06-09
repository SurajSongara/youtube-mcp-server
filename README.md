# YouTube Transcript MCP Server

An MCP (Model Context Protocol) server that lets AI agents interact with YouTube content. Search videos, fetch transcripts, search within transcript text, and retrieve video metadata — bridging the gap between LLMs and video content.

## Tools

| Tool | Description |
|------|-------------|
| `search_videos` | Search YouTube for videos by query, with filtering and pagination |
| `get_transcript` | Fetch the full transcript of a video by URL or ID |
| `search_transcript` | Search within a video's transcript for specific terms or phrases |
| `get_metadata` | Retrieve video metadata (title, description, views, duration, etc.) |

## Why an MCP Server?

MCP is the emerging standard for giving AI agents access to external tools and data sources. This server follows the [MCP specification](https://modelcontextprotocol.io), making it compatible with any MCP client — including Claude Desktop, VS Code via `opencode.json`, and custom MCP hosts.

## Tech Stack

- **Python 3.12+** — core language
- **[MCP SDK](https://github.com/modelcontextprotocol/python-sdk)** — MCP protocol implementation
- **YouTube Data API v3** — video search and metadata
- **yt-dlp / youtube-transcript-api** — transcript extraction
- **FastAPI** — async server (optional, for HTTP transport)

## Getting Started

### Prerequisites

- Python 3.12+
- YouTube Data API key ([get one here](https://console.cloud.google.com/apis/credentials))

### Installation

```sh
git clone https://github.com/SurajSongara/youtube-mcp-server
cd youtube-mcp-server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Create a `.env` file:

```
YOUTUBE_API_KEY=your_api_key_here
```

### Usage with MCP Client

Add to your `opencode.json` or Claude Desktop config:

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "python",
      "args": ["-m", "src.server"],
      "env": {
        "YOUTUBE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## Project Structure

```
youtube-mcp-server/
├── src/
│   ├── __init__.py
│   ├── server.py              # MCP server entry point
│   └── tools/
│       ├── __init__.py
│       ├── search.py           # search_videos tool
│       ├── transcript.py       # get_transcript tool
│       ├── search_transcript.py # search_transcript tool
│       └── metadata.py         # get_metadata tool
├── pyproject.toml
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md
```

## Development Status

MVP in progress. Building incrementally with each tool added and tested.

## Author

[Suraj Songara](https://github.com/SurajSongara)

## License

MIT
