"""Captures screenshots and saves them in screenshots/before or screenshots/after.

The "before" and "after" folders are what the AI/VLM team will read later.
"""

from datetime import datetime

from playwright.sync_api import Error as PlaywrightError

from automation import config


def capture_screenshot(page, filename, stage="before"):
    """Take a full-page screenshot.

    filename: a short name such as "login_page" (no extension needed)
    stage:    "before" or "after"

    Returns {"success": bool, "path": saved file path or None, "message": text}.
    The file is saved as <folder>/<filename>_<YYYYMMDD_HHMMSS>.png
    """
    folders = {"before": config.BEFORE_DIR, "after": config.AFTER_DIR}
    if stage not in folders:
        return {"success": False, "path": None, "message": f"Error: stage must be 'before' or 'after', got '{stage}'"}

    folder = folders[stage]
    folder.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = folder / f"{filename}_{timestamp}.png"

    try:
        page.screenshot(path=str(path), full_page=True)
    except PlaywrightError as error:
        first_line = str(error).splitlines()[0]
        return {"success": False, "path": None, "message": f"Error: screenshot failed - {first_line}"}

    return {"success": True, "path": str(path), "message": f"OK: screenshot saved to {path}"}
