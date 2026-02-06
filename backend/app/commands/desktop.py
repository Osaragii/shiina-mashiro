# Desktop Automation Commands, handles desktop control, screenshots, and application management

import pyautogui
import subprocess
import platform
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional


# Takes a screenshot and saves it
def take_screenshot(filename: Optional[str] = None) -> Dict[str, Any]:
    try:
        # Create screenshots directory if it does not exist
        screenshots_dir = Path("Screenshots")
        screenshots_dir.mkdir(exist_ok=True)

        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"

        # Ensures .png extension
        if not filename.endswith(".png"):
            filename += ".png"

        filepath = screenshots_dir / filename

        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(str(filepath))

        return {
            "success": True,
            "action": "screenshot_taken",
            "filepath": str(filepath.absolute()),
            "filename": filename,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        return {"success": False, "error": str(e), "action": "screenshot_failed"}


# Opens a desktop application


def open_application(app_name: str) -> Dict[str, Any]:
    try:
        system = platform.system()

        # Common application mappings
        app_mappings = {
            "notepad": "notepad.exe" if system == "Windows" else "TextEdit",
            "chrome": "chrome.exe" if system == "Windows" else "Google Chrome",
            "firefox": "firefox.exe" if system == "Windows" else "Firefox",
            "calculator": "calc.exe" if system == "Windows" else "Calculator",
            "explorer": "explorer.exe" if system == "Windows" else "Finder",
            "paint": "mspaint.exe" if system == "Windows" else "Preview",
        }

        # Get actual app name (or use provided name)
        actual_app = app_mappings.get(app_name.lower(), app_name)

        if system == "Windows":
            subprocess.Popen([actual_app], shell=True)
        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", "-a", actual_app])
        else:  # Linux
            subprocess.Popen([actual_app])

        return {
            "success": True,
            "action": "application_opened",
            "app_name": app_name,
            "actual_command": actual_app,
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "action": "application_open_failed",
            "app_name": app_name,
        }


# Types text using keyboard automation
def type_text(text: str) -> Dict[str, Any]:
    try:
        pyautogui.write(text, interval=0.05)  # 0.05 seconds between keystrokes

        return {
            "success": True,
            "action": "text_typed",
            "text": text,
            "character_count": len(text),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        return {"success": False, "error": str(e), "action": "type_text_failed"}
