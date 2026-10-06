"""Starts and stops the Chromium browser and gives you a page to work with."""

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from automation import config


class BrowserStartError(Exception):
    """Raised when Chromium cannot be started."""


class BrowserSession:
    """Owns one Chromium browser and one page.

    Recommended use (the browser is always closed, even if an error happens):

        with BrowserSession() as session:
            page = session.page
            ...
    """

    def __init__(self, headless=config.HEADLESS, slow_mo=config.SLOW_MO_MS):
        self.headless = headless
        self.slow_mo = slow_mo
        self.page = None
        self._playwright = None
        self._browser = None

    def start(self):
        """Launch Chromium and open an empty page. Returns the page."""
        try:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(
                headless=self.headless, slow_mo=self.slow_mo
            )
            self.page = self._browser.new_page(viewport=config.VIEWPORT)
            self.page.set_default_timeout(config.DEFAULT_TIMEOUT_MS)
        except PlaywrightError as error:
            self.stop()
            first_line = str(error).splitlines()[0]
            raise BrowserStartError(
                "Could not start Chromium. Did you run 'playwright install'? "
                f"Details: {first_line}"
            ) from error
        return self.page

    def stop(self):
        """Close the browser and stop Playwright."""
        try:
            if self._browser:
                self._browser.close()
        except PlaywrightError:
            pass  # the browser had already crashed or closed
        if self._playwright:
            self._playwright.stop()
        self.page = None
        self._browser = None
        self._playwright = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
