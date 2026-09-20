#!/usr/bin/env python3
"""Offline unit tests for scripts/check_site.py. No network."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("check_site", ROOT / "check_site.py")
check_site = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(check_site)


class StructureTests(unittest.TestCase):
    def test_balanced_page_ok(self) -> None:
        html = "<!doctype html><html><head><title>t</title></head><body><p>ok</p></body></html>"
        self.assertEqual(check_site.check_structure(html), [])

    def test_unclosed_tag(self) -> None:
        # Closing an ancestor pops inner tags (documented P2). An EOF-unclosed
        # tag is the case the checker actually fails on.
        errors = check_site.check_structure("<div>hello")
        self.assertTrue(any("unclosed <div>" in e for e in errors), errors)

    def test_stray_close(self) -> None:
        errors = check_site.check_structure("<html><body></p></body></html>")
        self.assertTrue(any("stray </p>" in e for e in errors), errors)

    def test_void_tags_need_no_close(self) -> None:
        html = '<html><head><meta charset="utf-8"><link rel="icon" href="x"></head><body><br><img src="x"></body></html>'
        self.assertEqual(check_site.check_structure(html), [])


class LocalAssetTests(unittest.TestCase):
    def test_missing_relative_href(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "index.html"
            page.write_text('<html><head><link href="missing.svg"></head></html>', encoding="utf-8")
            errors = check_site.check_local_assets(page.read_text(encoding="utf-8"), page)
            self.assertEqual(errors, ["missing local asset: missing.svg"])

    def test_existing_relative_href(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "favicon.svg").write_text("<svg></svg>", encoding="utf-8")
            page = root / "index.html"
            page.write_text('<html><head><link href="favicon.svg"></head></html>', encoding="utf-8")
            self.assertEqual(check_site.check_local_assets(page.read_text(encoding="utf-8"), page), [])

    def test_hash_and_absolute_urls_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "index.html"
            page.write_text(
                '<html><body><a href="#work">w</a><a href="https://example.com">e</a></body></html>',
                encoding="utf-8",
            )
            self.assertEqual(check_site.check_local_assets(page.read_text(encoding="utf-8"), page), [])


if __name__ == "__main__":
    unittest.main()
