"""Tests: UI elements exist, filling fields, clicking buttons, missing elements."""

from automation.actions import click_button, fill_field, read_text, wait_for_text


def test_basic_ui_elements_exist(page):
    assert page.get_by_role("heading", name="OmniSight Demo Site").is_visible()
    assert page.get_by_role("link").count() == 3
    assert page.get_by_label("Username", exact=True).count() == 1
    assert page.get_by_label("Password", exact=True).count() == 1
    assert page.get_by_role("button", name="Login", exact=True).is_visible()
    assert page.get_by_role("button", name="Toggle Theme", exact=True).is_visible()


def test_login_fields_can_be_filled(page):
    assert fill_field(page, "Username", "shifa")["success"]
    assert fill_field(page, "Password", "secret123")["success"]

    assert page.get_by_label("Username", exact=True).input_value() == "shifa"
    assert page.get_by_label("Password", exact=True).input_value() == "secret123"


def test_login_button_shows_welcome_message(page):
    fill_field(page, "Username", "shifa")
    fill_field(page, "Password", "secret123")

    assert click_button(page, "Login")["success"]
    assert wait_for_text(page, "Welcome, shifa!")["success"]
    assert read_text(page, "#login-message")["value"] == "Welcome, shifa!"


def test_login_with_empty_fields_shows_error_message(page):
    click_button(page, "Login")
    assert read_text(page, "#login-message")["value"] == "Please enter username and password."


def test_toggle_theme_button_changes_page(page):
    click_button(page, "Toggle Theme")
    assert "dark" in page.locator("body").get_attribute("class")


def test_clicking_missing_button_returns_timeout(page):
    page.set_default_timeout(500)  # do not wait the full 5 seconds in a test

    result = click_button(page, "Does Not Exist")
    assert result["success"] is False
    assert result["message"].startswith("Timeout")
