"""Settings used by the whole automation module. Change values here, not in the other files."""

from pathlib import Path

# Project root folder (the folder that contains "automation", "tests", ...)
BASE_DIR = Path(__file__).resolve().parent.parent

# The local demo website, written as a file:// URL so Playwright can open it.
# Works on Windows, e.g. file:///C:/Users/you/OmniSight-Member1/demo_site/index.html
DEMO_SITE_URL = (BASE_DIR / "demo_site" / "index.html").as_uri()

# Where screenshots are saved
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
BEFORE_DIR = SCREENSHOTS_DIR / "before"
AFTER_DIR = SCREENSHOTS_DIR / "after"

# Browser settings
HEADLESS = True                 # True = no visible window, False = show the browser
SLOW_MO_MS = 0                  # Delay (ms) after each action; useful to watch a demo
DEFAULT_TIMEOUT_MS = 5000       # How long Playwright waits for an element
VIEWPORT = {"width": 1280, "height": 720}
