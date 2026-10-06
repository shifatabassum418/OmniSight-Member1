"""Demo of the Member 1 module. Run from the project root:   python run_demo.py

Opens the local demo site in a visible Chromium window, fills the login form,
clicks buttons, and saves a "before" and an "after" screenshot.
"""

from automation import config
from automation.actions import (
    click_button,
    click_link,
    fill_field,
    get_page_info,
    open_url,
    read_text,
    reload_page,
    wait_for_text,
)
from automation.browser import BrowserSession, BrowserStartError
from automation.screenshots import capture_screenshot


def show(result):
    """Print the result message and stop the demo if the step failed."""
    print(result["message"])
    if not result["success"]:
        raise SystemExit(1)
    return result


def main():
    # slow_mo adds a small delay after every action so you can watch the demo.
    with BrowserSession(headless=False, slow_mo=600) as session:
        page = session.page

        show(open_url(page, config.DEMO_SITE_URL))
        print("Page info:", show(get_page_info(page))["value"])

        # Screenshot of the page as it is at the start
        show(capture_screenshot(page, "demo_site", "before"))

        # Navigation
        show(click_link(page, "About"))
        show(click_link(page, "Home"))

        # Fill the login form and click Login
        show(fill_field(page, "Username", "shifa"))
        show(fill_field(page, "Password", "secret123"))
        show(click_button(page, "Login"))
        show(wait_for_text(page, "Welcome, shifa!"))
        print("Login message:", show(read_text(page, "#login-message"))["value"])

        # Change the page, then take the second screenshot
        show(click_button(page, "Toggle Theme"))
        show(capture_screenshot(page, "demo_site", "after"))

        # Reload: the page goes back to its original state
        show(reload_page(page))
        print("Login message after reload:", repr(show(read_text(page, "#login-message"))["value"]))

        page.wait_for_timeout(2000)  # keep the window open briefly at the end


if __name__ == "__main__":
    try:
        main()
    except BrowserStartError as error:
        print(error)
        raise SystemExit(1)
