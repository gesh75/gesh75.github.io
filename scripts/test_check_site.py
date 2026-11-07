#!/usr/bin/env python3
"""Offline unit tests for scripts/check_site.py. No network."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from html.parser import HTMLParser
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


class HubCardParser(HTMLParser):
    """Collect each .card title and the <a href, text> pairs on that card."""

    def __init__(self) -> None:
        super().__init__()
        self.cards: list[dict] = []
        self._card: dict | None = None
        self._card_depth = 0
        self._depth = 0
        self._in_h3 = False
        self._h3: list[str] = []
        self._link: dict | None = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        classes = (d.get("class") or "").split()
        if tag in check_site.VOID:
            return
        self._depth += 1
        if self._card is None and "card" in classes:
            self._card = {"title": "", "links": []}
            self._card_depth = self._depth
            href = d.get("href")
            if tag == "a" and href:
                self._link = {"href": href, "parts": [], "depth": self._depth}
            return
        if self._card is None:
            return
        if tag == "h3" and not self._card["title"]:
            self._in_h3 = True
            self._h3 = []
        if tag == "a" and d.get("href") and self._link is None:
            self._link = {"href": d["href"], "parts": [], "depth": self._depth}

    def handle_endtag(self, tag):
        if tag in check_site.VOID:
            return
        if self._in_h3 and tag == "h3" and self._card is not None:
            self._card["title"] = "".join(self._h3).strip()
            self._in_h3 = False
        if self._link is not None and tag == "a" and self._depth == self._link["depth"]:
            self._flush_link()
        if self._card is not None and self._depth == self._card_depth:
            if self._link is not None:
                self._flush_link()
            self.cards.append(self._card)
            self._card = None
        self._depth -= 1

    def handle_data(self, data):
        if self._in_h3:
            self._h3.append(data)
        if self._link is not None:
            self._link["parts"].append(data)

    def _flush_link(self) -> None:
        assert self._card is not None and self._link is not None
        text = " ".join("".join(self._link["parts"]).split())
        self._card["links"].append((self._link["href"], text))
        self._link = None


class AllAnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self._link: dict | None = None
        self._depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in check_site.VOID:
            return
        self._depth += 1
        if tag != "a" or self._link is not None:
            return
        href = dict(attrs).get("href")
        if href:
            self._link = {"href": href, "parts": [], "depth": self._depth}

    def handle_endtag(self, tag):
        if tag in check_site.VOID:
            return
        if self._link is not None and tag == "a" and self._depth == self._link["depth"]:
            text = " ".join("".join(self._link["parts"]).split())
            self.links.append((self._link["href"], text))
            self._link = None
        self._depth -= 1

    def handle_data(self, data):
        if self._link is not None:
            self._link["parts"].append(data)


class HubHuggingFaceTests(unittest.TestCase):
    EXPECTED_CARD_LINKS = (
        (
            "netlog-ai",
            "https://huggingface.co/spaces/gesh75/netlog-ai",
            "Live demo on Hugging Face",
        ),
        (
            "multivendor-cli-configurator",
            "https://huggingface.co/spaces/gesh75/multivendor-cli-configurator",
            "Live demo on Hugging Face",
        ),
        (
            "multivendor-cli-commands",
            "https://huggingface.co/datasets/gesh75/multivendor-cli-commands",
            "Dataset on Hugging Face",
        ),
    )

    def test_huggingface_urls_are_anchors_on_intended_cards(self) -> None:
        html = (ROOT.parent / "index.html").read_text(encoding="utf-8")
        cards = HubCardParser()
        cards.feed(html)
        by_title = {card["title"]: card for card in cards.cards}
        for title, url, label in self.EXPECTED_CARD_LINKS:
            with self.subTest(card=title):
                self.assertIn(title, by_title, f"missing project card {title!r}")
                matches = [
                    (href, text)
                    for href, text in by_title[title]["links"]
                    if href == url and label in text
                ]
                self.assertTrue(
                    matches,
                    f"{title}: no <a href={url!r}> containing {label!r}; "
                    f"links={by_title[title]['links']}",
                )

        anchors = AllAnchorParser()
        anchors.feed(html)
        profile = [
            (href, text)
            for href, text in anchors.links
            if href == "https://huggingface.co/gesh75"
        ]
        self.assertTrue(
            profile,
            "no <a> with href https://huggingface.co/gesh75",
        )


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
