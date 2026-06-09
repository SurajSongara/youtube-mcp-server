# YouTube Transcript MCP Server

An MCP server that lets AI agents search YouTube, fetch video transcripts, search within transcript text, and retrieve video metadata. Bridges the gap between LLMs and video content.

## Tools

| Tool | Description | API Key |
|------|-------------|---------|
| `search_videos` | Search YouTube for videos with filtering and pagination | Required |
| `get_metadata` | Retrieve video metadata: title, description, duration, view count, like count, tags | Required |
| `get_transcript` | Fetch full transcript of a video by URL or ID | None needed |
| `search_transcript` | Search within a video's transcript for specific terms or phrases | None needed |

`search_transcript` supports fuzzy + stem-aware matching (no external dependencies) — catches typos and variant word forms like "coding" matching "code", "codes", "coder".

## Tech Stack

- **Python 3.12+**
- **[FastMCP](https://github.com/modelcontextprotocol/python-sdk)** — MCP framework (auto-schema from type hints)
- **[YouTube Data API v3](https://developers.google.com/youtube/v3)** — video search and metadata
- **[youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)** — transcript extraction

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

A YouTube Data API key is free from [Google Cloud Console](https://console.cloud.google.com/apis/credentials) (enable YouTube Data API v3). Only `search_videos` and `get_metadata` require it; transcript tools work without any key.

## MCP Client Config

Add to `~/.config/opencode/opencode.jsonc` or `opencode.json`:

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
├── server.py           # FastMCP server (all 4 tools)
└── utils/
    └── youtube_api.py  # YouTube Data API v3 client
```

## Author

[Suraj Songara](https://github.com/SurajSongara)

## License

MIT
