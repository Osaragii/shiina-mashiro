# Browser Automation Commands, handles browser control, navigation, and web interactions

import subprocess
import platform
from typing import Dict, Any
from ..config import (
    config,
)  # It is in the app directory not in the backend directory so we cannot import directly, either app.config or ..config


# Opens default browser and navigates to URL.
def open_browser(url: str = None) -> Dict[str, Any]:
    try:
        # Add https:// if not present
        if url is None:
            url = config.DEFAULT_BROWSER_URL

        # Platform-specific browser opening
        system = platform.system()

        if system == "Windows":
            subprocess.Popen(["start", url], shell=True)
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", url])
        else:  # Linux
            subprocess.Popen(["xdg-open", url])

        return {"success": False, "action": "browser_opened", "url": url}

    except Exception as e:
        return {"success": False, "error": str(e), "action": "browser_open_failed"}


# Opens Google search with the given query.
def search_google(query: str) -> Dict[str, Any]:
    try:
        # URL encode the query
        import urllib.parse

        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"

        # Use open_browser to navigate
        result = open_browser(search_url)
        result["action"] = "google_search"
        result["query"] = query

        return result

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "action": "google_search_failed",
            "query": query,
        }


# Opens Youtube, optionally with a search query
def open_youtube(search: str = None) -> Dict[str, Any]:
    try:
        if search:
            import urllib.parse

            encoded_search = urllib.parse.quote(search)
            url = f"https://www.youtube.com/results?search_query={encoded_search}"
        else:
            url = "https://www.youtube.com"

        result = open_browser(url)
        result["action"] = "youtube_opened"

        if search:
            result["search"] = search

        return result

    except Exception as e:
        return {"success": False, "error": str(e), "action": "youtube_open_failed"}
