"""Tests: opening the site, page title, links, going back, reloading, bad URLs."""

from automation import config
from automation.actions import (
    click_link,
    fill_field,
    click_button,
    get_page_info,
    go_back,
    open_url,
    read_text,
    reload_page,
    wait_for_text,
)


def test_website_opens_successfully(page):
    info = get_page_info(page)
    assert info["success"]
    assert info["value"]["url"] == config.DEMO_SITE_URL


def test_page_title_is_correct(page):
    assert page.title() == "OmniSight Demo Site"


def test_navigation_link_changes_url_and_back_returns(page):
    assert click_link(page, "About")["success"]
    assert page.url.endswith("#about")

    assert go_back(page)["success"]
    assert not page.url.endswith("#about")


def test_page_can_be_reloaded(page):
    fill_field(page, "Username", "shifa")
    fill_field(page, "Password", "secret123")
    click_button(page, "Login")
    assert wait_for_text(page, "Welcome, shifa!")["success"]

    assert reload_page(page)["success"]
    assert read_text(page, "#login-message")["value"] == ""


def test_opening_a_missing_page_returns_error(page):
    result = open_url(page, "file:///this/page/does/not/exist.html")
    assert result["success"] is False
    assert result["message"].startswith("Error")
