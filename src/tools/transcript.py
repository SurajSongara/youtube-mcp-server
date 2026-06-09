import re

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from mcp.types import Tool, TextContent


VIDEO_ID_RE = re.compile(r"(?:v=|youtu\.be/|/shorts/)([a-zA-Z0-9_-]{11})")

TOOL = Tool(
    name="get_transcript",
    description="Fetch the transcript of a YouTube video by URL or video ID",
    inputSchema={
        "type": "object",
        "properties": {
            "video_id": {
                "type": "string",
                "description": "YouTube video URL or video ID (e.g. 'dQw4w9WgXcQ' or 'https://youtube.com/watch?v=dQw4w9WgXcQ')",
            },
            "languages": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Language codes to try (e.g. ['en', 'hi']). Defaults to ['en'].",
            },
        },
        "required": ["video_id"],
    },
)


def extract_video_id(value: str) -> str:
    match = VIDEO_ID_RE.search(value)
    return match.group(1) if match else value


async def handle(arguments: dict) -> list[TextContent]:
    raw = arguments["video_id"]
    languages = arguments.get("languages", ["en"])

    video_id = extract_video_id(raw)

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=languages)

        segments = [
            {"text": s.text, "start": s.start, "duration": s.duration}
            for s in transcript
        ]

        result = {
            "video_id": video_id,
            "language": transcript.language,
            "language_code": transcript.language_code,
            "is_generated": transcript.is_generated,
            "segments": segments,
            "full_text": " ".join(s["text"] for s in segments),
        }

        return [TextContent(type="text", text=str(result))]
    except NoTranscriptFound:
        api = YouTubeTranscriptApi()
        available = api.list(raw if not VIDEO_ID_RE.search(raw) else video_id)
        langs = "\n".join(
            f"  - {t.language_code} ({t.language}){' [auto-generated]' if t.is_generated else ''}"
            for t in available
        )
        return [
            TextContent(
                type="text",
                text=f"No transcript found for languages: {languages}. Available transcripts:\n{langs}",
            )
        ]
    except Exception as e:
        return [TextContent(type="text", text=f"Error fetching transcript: {e}")]
