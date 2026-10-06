# OmniSight - Member 1: Python + Playwright Browser Automation

## 1. Project purpose
OmniSight is a multimodal UI self-healing and RPA agent. The full workflow is:

```
Website -> Playwright automation -> Screenshot -> AI/VLM analyses it -> Detect UI problem
        -> Generate fix -> Apply fix -> Playwright tests again -> Verify the problem is fixed
```

## 2. Member 1 responsibility
This repository contains only the browser automation part (Member 1). It opens websites, interacts with them, runs UI tests and saves before/after screenshots.

| Member | Responsibility |
|---|---|
| 1 (this module) | Python + Playwright browser automation |
| 2 | AI/VLM setup and prompt testing |
| 3 | FastAPI backend |
| 4 | Frontend/dashboard and GitHub setup |

## 3. Technology used
Python 3, Playwright (sync API, Chromium), pytest. Target OS: Windows.

## 4. Folder structure
```
OmniSight-Member1/
├── automation/
│   ├── __init__.py       Makes "automation" an importable package
│   ├── config.py         URLs, folders, timeout and browser settings
│   ├── browser.py        Starts and stops Chromium, gives you a page
│   ├── actions.py        Open URL, click, fill, read text, wait, reload
│   └── screenshots.py    Captures and saves screenshots (before/after)
├── tests/
│   ├── test_navigation.py    Site opens, title, links, back, reload, bad URL
│   ├── test_interaction.py   Elements exist, fill, click, errors
│   └── test_screenshot.py    Screenshot saving and before/after folders
├── screenshots/
│   ├── before/
│   └── after/
├── demo_site/
│   └── index.html        Local website used for practice and testing
├── conftest.py           Shared pytest fixture: a browser page with the demo site open
├── run_demo.py           The demo: run this to show the module working
├── requirements.txt
├── .gitignore
└── README.md
```

How the pieces connect: `config.py` holds the settings. `browser.py` gives you a `page`. `actions.py` and `screenshots.py` do things with that `page`. `run_demo.py` and the files in `tests/` use all of them.

`conftest.py` is a pytest file. It creates the `page` fixture (a headless browser with the demo site already open) used by every test, and it lets pytest find the `automation` package.

## 5. Windows installation
Open Command Prompt or the VS Code terminal. Every command below is run from the project root folder, the folder that contains `requirements.txt` (the `OmniSight-Member1` folder).

```
cd path\to\OmniSight-Member1
```

### Virtual environment
```
python -m venv venv
venv\Scripts\activate
```
Your prompt will start with `(venv)`. If PowerShell blocks the activation script, run this once and try again:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Playwright and browser installation
```
pip install -r requirements.txt
playwright install
```
`pip install` installs the Playwright Python package and pytest. `playwright install` downloads the browsers (Chromium is the one used here).

## 6. Run the demo
From the project root, with `(venv)` active:
```
python run_demo.py
```
A Chromium window opens the demo site, goes to About and back to Home, fills the login form, clicks Login, clicks Toggle Theme, reloads the page, and saves two screenshots.

## 7. Run the tests
From the project root, with `(venv)` active:
```
pytest
```
For more detail: `pytest -v`

## 8. Where screenshots are saved
```
screenshots/before/<name>_<YYYYMMDD_HHMMSS>.png
screenshots/after/<name>_<YYYYMMDD_HHMMSS>.png
```
Example: `screenshots/before/demo_site_20261006_101936.png`. In code:
```python
from automation.screenshots import capture_screenshot
result = capture_screenshot(page, "login_page", "before")   # or "after"
print(result["path"])
```
The tests save their screenshots to a temporary folder, so `screenshots/` only contains what the demo (or your own code) creates.

## 9. Why reliable selectors
A fragile selector such as `div > div:nth-child(3) > button` breaks when the layout, order or styling changes. A reliable selector describes the element the way a user sees it:

```python
page.get_by_role("button", name="Login")   # a button named Login
page.get_by_label("Username")              # the input with the label Username
page.get_by_text("Welcome, shifa!")        # visible text
page.locator("#login-message")             # a CSS selector for a stable id
```
OmniSight changes the UI to fix problems, so tests that depend on visible meaning keep working after a fix, while tests that depend on page structure would break.

## 10. Error handling
Every function in `actions.py` and `screenshots.py` returns a dictionary instead of crashing:
```python
{"success": False, "message": "Timeout: click button 'Login' (element not found or not ready in time)", "value": None}
```
Covered cases: URL cannot be opened, element not found or timeout, screenshot failure. If Chromium cannot start (for example `playwright install` was not run), `BrowserSession` raises `BrowserStartError` with a clear message.

## 11. What this module provides to the team
| | |
|---|---|
| Input | A URL and automation instructions (open, fill, click, read, screenshot) |
| Output | Result dictionary (`success`, `message`, `value`), screenshot file path, page info (title, URL, heading, element counts), pytest pass/fail results |

## 12. How this connects to the VLM (Member 2)
`capture_screenshot()` returns the file path of a PNG in `screenshots/before/`. Member 2 reads that file, sends it to the VLM, and gets the detected UI problem. After a fix is applied, this module captures a new screenshot in `screenshots/after/` for the VLM to compare. This module does not call the VLM.

```python
result = capture_screenshot(page, "checkout", "before")
image_path = result["path"]        # Member 2 sends this image to the VLM
```

## 13. How this connects to FastAPI (Member 3)
The functions are plain Python and return plain dictionaries, so a FastAPI endpoint can import and call them directly:

```python
from automation.browser import BrowserSession
from automation.actions import open_url
from automation.screenshots import capture_screenshot

with BrowserSession() as session:
    open_url(session.page, "https://example.com")
    shot = capture_screenshot(session.page, "home", "before")
    # return shot["path"] in the API response
```
Member 3 can also run `pytest` (for example with `subprocess`) to verify a fix and return the result. This integration is not implemented here.

## Playwright browsers and GitHub
Do not commit Playwright browser binaries. `playwright install` stores them outside the project (on Windows: `%USERPROFILE%\AppData\Local\ms-playwright`), so they are never inside this folder. Each teammate runs `playwright install` once. `.gitignore` also ignores `venv/`, `__pycache__/`, `*.pyc`, `.env` and generated screenshots (the empty `before/` and `after/` folders are kept with `.gitkeep` files).
