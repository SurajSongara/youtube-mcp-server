# YouTube Transcript MCP Server

An MCP server that lets AI agents search YouTube, fetch video transcripts, and retrieve metadata. Bridges the gap between LLMs and video content.

## Tools

| Tool | Description |
|------|-------------|
| `search_videos` | Search YouTube for videos with filtering and pagination |
| `get_transcript` | Fetch transcript of a video by URL or ID (no API key needed) |

## Tech Stack

- **Python 3.12+**
- **[FastMCP](https://github.com/modelcontextprotocol/python-sdk)** — MCP framework
- **YouTube Data API v3** — video search
- **youtube-transcript-api** — transcript extraction (no auth required)

## Getting Started

```sh
git clone https://github.com/SurajSongara/youtube-mcp-server
cd youtube-mcp-server
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "YOUTUBE_API_KEY=your_key_here" > .env
python -m src.server
```

`search_videos` requires a YouTube Data API key (`getenv YOUTUBE_API_KEY`).  
`get_transcript` works without any API key.

## MCP Client Config

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "python",
      "args": ["-m", "src.server"],
      "env": {
        "YOUTUBE_API_KEY": "your_key_here"
      }
    }
  }
}
```

## Project Structure

```
src/
├── server.py          # FastMCP server with both tools
└── utils/
    └── youtube_api.py  # YouTube Data API client
```

## Status

MVP. Building incrementally.

## Author

[Suraj Songara](https://github.com/SurajSongara)

## License

MIT
