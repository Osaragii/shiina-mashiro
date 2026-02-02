# Command Executor - Central Router, Routes commands to appropriate command modules

from typing import Dict, Any
from commands import browser, desktop

# Routes command to the appropriate handler function
def execute_command(command: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    # Default empty dict if no parameters
    if parameters is None:
        parameters = {}

    # Commaqnd mapping - routes command names to handler functions
    command_map = {
        # Browser commands (from browser.py)
        "open_browser": lambda p: browser.open_browser(p.get("url", "https://google.com")),
        "search_google": lambda p: browser.search_google(p.get("query", "")),
        "open_youtube": lambda p: browser.open_youtube(p.get("search")),

        # Desktop commands (from desktop.py)
        "screenshot": lambda p: desktop.take_screenshot(p.get("filename")),
        "open_app": lambda p: desktop.open_application(p.get("app", "notepad")),
        "type_text": lambda p: desktop.type_text(p.get("text", "")),
    }

    # Execute command if it exists
    if command in command_map:
        try:
            result = command_map[command](parameters)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution error: {str(e)}",
                "command": command
            }
    else:
        #Command not found
        return {
            "success": False,
            "error": f"Unknown Command: {command}",
            "available_commands": list(command_map.keys())
        }

# Returns list of all available commands organized by category
def get_available_commands() -> Dict[str, list]:
    return {
        "browser": [
            "open_browser",
            "search_google",
            "open_youtube",
        ],
        "desktop": [
            "screenshot",
            "open_app",
            "type_text",
        ]
    }