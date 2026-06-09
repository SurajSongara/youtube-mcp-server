from mcp.types import Tool, TextContent
from src.utils.youtube_api import YouTubeAPI

yt = YouTubeAPI()

TOOL = Tool(
    name="search_videos",
    description="Search YouTube for videos by query string with filtering and pagination",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query for YouTube videos",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results (1-50)",
                "minimum": 1,
                "maximum": 50,
                "default": 10,
            },
            "order": {
                "type": "string",
                "description": "Sort order (relevance, date, rating, viewCount)",
                "enum": ["relevance", "date", "rating", "viewCount"],
                "default": "relevance",
            },
            "page_token": {
                "type": "string",
                "description": "Token for pagination from previous response",
            },
        },
        "required": ["query"],
    },
)


async def handle(arguments: dict) -> list[TextContent]:
    query = arguments["query"]
    max_results = arguments.get("max_results", 10)
    order = arguments.get("order", "relevance")
    page_token = arguments.get("page_token")

    try:
        result = yt.search_videos(
            query=query,
            max_results=max_results,
            order=order,
            page_token=page_token,
        )
        return [TextContent(type="text", text=str(result))]
    except Exception as e:
        return [TextContent(type="text", text=f"Error searching videos: {e}")]
