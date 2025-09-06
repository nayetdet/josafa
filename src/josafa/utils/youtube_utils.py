from typing import Dict, Any, Tuple, Optional
from yt_dlp import YoutubeDL

class YoutubeUtils:
    __ydl_opts: Dict[str, Any] = {
        "format": "bestaudio",
        "noplaylist": True,
        "quiet": True,
        "default_search": "ytsearch"
    }

    @classmethod
    def extract_url(cls, arg: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        with YoutubeDL(cls.__ydl_opts) as ydl:
            info = ydl.extract_info(arg, download=False)
            video = info["entries"][0] if "entries" in info else info
            return video.get("title"), video.get("thumbnail"), video.get("url")
