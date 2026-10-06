"""Shared pytest setup. Because this file is in the project root, pytest can import "automation"
and every test can ask for the `page` fixture: a headless Chromium page with the demo site open."""

import pytest

from automation import config
from automation.actions import open_url
from automation.browser import BrowserSession


@pytest.fixture
def page():
    with BrowserSession(headless=True) as session:
        result = open_url(session.page, config.DEMO_SITE_URL)
        assert result["success"], result["message"]
        yield session.page
