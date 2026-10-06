"""Things you can do on a page: open URLs, click, fill, read text, wait, reload.

Every function returns a dictionary:
    {"success": True or False, "message": "what happened", "value": extra data or None}
so the caller (a test, the demo, or later FastAPI) never has to deal with raw exceptions.

Locators used here are "reliable" ones: they find elements the way a user sees them
(by role, label or visible text) instead of by fragile CSS paths like "div > div:nth-child(3)".
They keep working when the page layout or styling changes, which matters a lot for a
self-healing tool that changes the UI.
"""

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


def _run(description, action):
    """Run action() and convert any Playwright error into a result dictionary."""
    try:
        value = action()
        return {"success": True, "message": f"OK: {description}", "value": value}
    except PlaywrightTimeoutError:
        # TimeoutError must be checked first because it is a kind of PlaywrightError.
        return {
            "success": False,
            "message": f"Timeout: {description} (element not found or not ready in time)",
            "value": None,
        }
    except PlaywrightError as error:
        first_line = str(error).splitlines()[0]
        return {"success": False, "message": f"Error: {description} - {first_line}", "value": None}


# ---------- Navigation ----------

def open_url(page, url):
    """Open a URL and wait until the page has loaded. value = page title."""

    def action():
        page.goto(url, wait_until="load")
        return page.title()

    return _run(f"open {url}", action)


def go_back(page):
    """Go to the previous page in the browser history. value = new URL."""

    def action():
        page.go_back()
        return page.url

    return _run("go back", action)


def reload_page(page):
    """Reload the current page and wait for it to load. value = page title."""

    def action():
        page.reload(wait_until="load")
        return page.title()

    return _run("reload page", action)


# ---------- Interaction ----------

def click_button(page, name):
    """Click a button by its visible name, e.g. click_button(page, "Login")."""
    return _run(
        f"click button '{name}'",
        lambda: page.get_by_role("button", name=name, exact=True).click(),
    )


def click_link(page, name):
    """Click a link by its visible text, e.g. click_link(page, "About")."""
    return _run(
        f"click link '{name}'",
        lambda: page.get_by_role("link", name=name, exact=True).click(),
    )


def fill_field(page, label, text):
    """Type text into the input that has this label, e.g. fill_field(page, "Username", "shifa")."""
    return _run(
        f"fill '{label}'",
        lambda: page.get_by_label(label, exact=True).fill(text),
    )


# ---------- Reading ----------

def read_text(page, selector):
    """Return the visible text of the first element matching a CSS selector. value = text."""
    return _run(
        f"read text of '{selector}'",
        lambda: page.locator(selector).first.inner_text(),
    )


def get_page_info(page):
    """Read basic page information. value = dictionary with title, url, heading and element counts."""

    def action():
        heading = page.locator("h1")
        return {
            "title": page.title(),
            "url": page.url,
            "heading": heading.first.inner_text() if heading.count() > 0 else "",
            "button_count": page.get_by_role("button").count(),
            "link_count": page.get_by_role("link").count(),
            "input_count": page.locator("input").count(),
        }

    return _run("read page info", action)


# ---------- Waiting ----------

def wait_for_text(page, text):
    """Wait until some text becomes visible on the page (up to the default timeout)."""
    return _run(
        f"wait for text '{text}'",
        lambda: page.get_by_text(text).wait_for(state="visible"),
    )
