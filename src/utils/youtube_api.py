import os
import re

from googleapiclient.discovery import build


class YouTubeAPI:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY", "")
        self.service = build("youtube", "v3", developerKey=self.api_key)

    def search_videos(
        self,
        query: str,
        max_results: int = 10,
        order: str = "relevance",
        page_token: str | None = None,
    ) -> dict:
        request = self.service.search().list(
            q=query,
            part="snippet",
            type="video",
            maxResults=min(max_results, 50),
            order=order,
            pageToken=page_token or "",
        )
        response = request.execute()

        items = []
        for item in response.get("items", []):
            snippet = item["snippet"]
            items.append({
                "id": item["id"]["videoId"],
                "title": snippet["title"],
                "description": snippet["description"],
                "channel": snippet["channelTitle"],
                "published_at": snippet["publishedAt"],
                "thumbnail": snippet["thumbnails"]["high"]["url"]
                if "high" in snippet["thumbnails"]
                else snippet["thumbnails"]["default"]["url"],
            })

        return {
            "items": items,
            "total_results": response.get("pageInfo", {}).get("totalResults", 0),
            "next_page_token": response.get("nextPageToken"),
            "prev_page_token": response.get("prevPageToken"),
        }

    def get_video_metadata(self, video_id: str) -> dict:
        request = self.service.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id,
        )
        response = request.execute()
        if not response.get("items"):
            return {"error": "Video not found"}

        item = response["items"][0]
        snippet = item["snippet"]
        stats = item.get("statistics", {})

        duration = item.get("contentDetails", {}).get("duration", "")
        duration_seconds = self._parse_duration(duration)

        return {
            "id": video_id,
            "title": snippet["title"],
            "description": snippet["description"],
            "channel": snippet["channelTitle"],
            "published_at": snippet["publishedAt"],
            "duration": duration,
            "duration_seconds": duration_seconds,
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0)),
            "tags": snippet.get("tags", []),
            "category": snippet.get("categoryId", ""),
            "thumbnail": snippet["thumbnails"]["high"]["url"]
            if "high" in snippet["thumbnails"]
            else snippet["thumbnails"]["default"]["url"],
        }

    @staticmethod
    def _parse_duration(duration_iso: str) -> int:
        match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_iso)
        if not match:
            return 0
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        return hours * 3600 + minutes * 60 + seconds
