"""Tests: screenshots are saved in the before/after folders.

monkeypatch points the screenshot folders to a temporary folder so test runs
do not fill your real screenshots/ folder.
"""

from pathlib import Path

from automation import config
from automation.screenshots import capture_screenshot


def test_screenshot_is_captured_and_saved(page, monkeypatch, tmp_path):
    monkeypatch.setattr(config, "BEFORE_DIR", tmp_path / "before")

    result = capture_screenshot(page, "demo_page", "before")

    assert result["success"]
    saved_file = Path(result["path"])
    assert saved_file.exists()
    assert saved_file.stat().st_size > 0
    assert saved_file.parent == tmp_path / "before"


def test_before_and_after_use_different_folders(page, monkeypatch, tmp_path):
    monkeypatch.setattr(config, "BEFORE_DIR", tmp_path / "before")
    monkeypatch.setattr(config, "AFTER_DIR", tmp_path / "after")

    before = capture_screenshot(page, "demo_page", "before")
    after = capture_screenshot(page, "demo_page", "after")

    assert Path(before["path"]).parent.name == "before"
    assert Path(after["path"]).parent.name == "after"


def test_unknown_stage_returns_error(page):
    result = capture_screenshot(page, "demo_page", "middle")
    assert result["success"] is False
    assert result["path"] is None
