#!/usr/bin/env python3
"""Offline tests for scripts/check_site.py. No network."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_site import SKIP_HOSTS, check_structure, html_paths  # noqa: E402


class StructureTests(unittest.TestCase):
    def test_balanced_ok(self) -> None:
        self.assertEqual(check_structure("<div><p>hi</p></div>"), [])

    def test_void_meta_ok(self) -> None:
        self.assertEqual(
            check_structure('<html><head><meta charset="utf-8"><title>x</title></head></html>'),
            [],
        )

    def test_unclosed_tag(self) -> None:
        errors = check_structure("<div><p>hi")
        self.assertTrue(any("unclosed <p>" in e for e in errors), errors)
        self.assertTrue(any("unclosed <div>" in e for e in errors), errors)

    def test_stray_close(self) -> None:
        errors = check_structure("<div></p></div>")
        self.assertTrue(any("stray </p>" in e for e in errors), errors)

    def test_self_closing_svg_ok(self) -> None:
        self.assertEqual(check_structure('<svg><path d="M0 0"/></svg>'), [])


class PathTests(unittest.TestCase):
    def test_explicit_paths_win(self) -> None:
        self.assertEqual(html_paths(["index.html"]), [Path("index.html")])

    def test_default_discovers_hub_and_docs(self) -> None:
        found = {p.as_posix() for p in html_paths([])}
        self.assertIn("index.html", found)
        self.assertIn("claude-skill-lint/index.html", found)
        self.assertTrue(all(not str(p).startswith("gesh-book") for p in found))


class SkipHostTests(unittest.TestCase):
    def test_linkedin_still_skipped(self) -> None:
        self.assertIn("linkedin.com", SKIP_HOSTS)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
