import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

load_dotenv()

from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound
from src.utils.youtube_api import YouTubeAPI

VIDEO_ID_RE = re.compile(r"(?:v=|youtu\.be/|/shorts/)([a-zA-Z0-9_-]{11})")

app = FastMCP("youtube-transcript")


def _extract_video_id(value: str) -> str:
    match = VIDEO_ID_RE.search(value)
    return match.group(1) if match else value


@app.tool()
async def search_videos(
    query: str,
    max_results: int = 10,
    order: str = "relevance",
    page_token: str | None = None,
) -> str:
    """Search YouTube for videos by query string with filtering and pagination.

    Args:
        query: Search query for YouTube videos
        max_results: Maximum number of results (1-50)
        order: Sort order (relevance, date, rating, viewCount)
        page_token: Token for pagination from previous response
    """
    try:
        yt = YouTubeAPI()
        result = yt.search_videos(
            query=query,
            max_results=max_results,
            order=order,
            page_token=page_token,
        )
        return str(result)
    except Exception as e:
        return f"Error searching videos: {e}"


@app.tool()
async def get_transcript(
    video_id: str,
    languages: list[str] | None = None,
) -> str:
    """Fetch the transcript of a YouTube video by URL or video ID.

    Args:
        video_id: YouTube video URL or video ID (e.g. 'dQw4w9WgXcQ' or 'https://youtube.com/watch?v=dQw4w9WgXcQ')
        languages: Language codes to try (e.g. ['en', 'hi']). Defaults to ['en']
    """
    raw = video_id
    video_id = _extract_video_id(video_id)
    languages = languages or ["en"]

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

        return str(result)
    except NoTranscriptFound:
        api = YouTubeTranscriptApi()
        available = api.list(raw if not VIDEO_ID_RE.search(raw) else video_id)
        langs = "\n".join(
            f"  - {t.language_code} ({t.language}){' [auto-generated]' if t.is_generated else ''}"
            for t in available
        )
        return f"No transcript found for languages: {languages}\nAvailable transcripts:\n{langs}"
    except Exception as e:
        return f"Error fetching transcript: {e}"


@app.tool()
async def search_transcript(
    video_id: str,
    query: str,
    languages: list[str] | None = None,
    context_seconds: float = 5.0,
) -> str:
    """Search within a video's transcript for specific terms or phrases, returning matching segments with timestamps.

    Args:
        video_id: YouTube video URL or video ID
        query: Text to search for within the transcript (case-insensitive)
        languages: Language codes to try (e.g. ['en', 'hi']). Defaults to ['en']
        context_seconds: Include surrounding context in seconds. Defaults to 5.0
    """
    video_id = _extract_video_id(video_id)
    languages = languages or ["en"]

    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id, languages=languages)

        query_lower = query.lower()
        matches = []
        for i, seg in enumerate(transcript):
            if query_lower in seg.text.lower():
                match = {
                    "text": seg.text.strip(),
                    "start": seg.start,
                    "duration": seg.duration,
                }
                if context_seconds > 0:
                    before = [
                        {"text": t.text.strip(), "start": t.start}
                        for t in transcript
                        if 0 <= seg.start - t.start <= context_seconds and t is not seg
                    ]
                    after = [
                        {"text": t.text.strip(), "start": t.start}
                        for t in transcript
                        if 0 <= t.start - (seg.start + seg.duration) <= context_seconds
                    ]
                    if before:
                        match["before"] = before
                    if after:
                        match["after"] = after
                matches.append(match)

        if not matches:
            return f"No matches found for '{query}' in the transcript."

        result = {
            "video_id": video_id,
            "query": query,
            "match_count": len(matches),
            "language": transcript.language,
            "language_code": transcript.language_code,
            "matches": matches[:50],
            "truncated": len(matches) > 50,
        }
        return str(result)
    except NoTranscriptFound:
        return f"No transcript available for this video in languages: {languages}"
    except Exception as e:
        return f"Error searching transcript: {e}"


if __name__ == "__main__":
    app.run(transport="stdio")
