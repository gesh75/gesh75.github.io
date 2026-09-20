#!/usr/bin/env python3
"""Validate a Pages HTML file: structure (offline) + local assets + link liveness.

Three checks:
  1. The file parses with balanced tags. Pure offline, a hard gate.
  2. Relative href/src targets exist on disk (also offline).
  3. Every external http(s) link resolves. A 404/410 is a hard failure
     (a card pointing at a renamed repo / taken-down Pages site). Transient
     problems (timeouts, 403, 5xx, rate limits) are warnings, not failures.

LinkedIn is skipped outright — it serves 999/403 to automated clients.

Stdlib only. `python3 scripts/check_site.py [path-to-html]` (defaults to index.html).
CI should invoke this once per published HTML file.
Exit 0 = ok, 1 = structural / missing-asset / dead-link error, 2 = usage/IO error.
"""
from __future__ import annotations

import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
# Hosts that reject automated requests; checking them only yields false alarms.
SKIP_HOSTS = ("linkedin.com",)
UA = "Mozilla/5.0 (compatible; hub-link-check/1.0)"
TIMEOUT = 12


class TagBalance(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[tuple[str, int]] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        pass  # self-closing, nothing to balance

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                del self.stack[i:]
                return
        self.errors.append(f"line {self.getpos()[0]}: stray </{tag}>")


def check_structure(html: str) -> list[str]:
    p = TagBalance()
    p.feed(html)
    errors = list(p.errors)
    for tag, line in p.stack:
        errors.append(f"line {line}: unclosed <{tag}>")
    return errors


_LOCAL_REF = re.compile(r'(?:href|src)="(?!https?://|//|#|mailto:|data:)([^"]+)"')


def check_local_assets(html: str, page: Path) -> list[str]:
    """Fail if a relative href/src does not exist next to the page."""
    errors: list[str] = []
    root = page.resolve().parent
    for raw in _LOCAL_REF.findall(html):
        rel = raw.split("#", 1)[0].split("?", 1)[0]
        if not rel:
            continue
        target = (root / rel).resolve()
        if not target.exists():
            errors.append(f"missing local asset: {raw}")
    return errors


def link_status(url: str) -> tuple[str, int | None, str]:
    """Return (verdict, http_status, detail). verdict in dead|ok|warn."""
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return "ok", resp.status, ""
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return "dead", e.code, "not found"
            if e.code in (403, 405) and method == "HEAD":
                continue  # some servers refuse HEAD — retry as GET
            return "warn", e.code, f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            return "warn", None, str(getattr(e, "reason", e))
    return "warn", None, "HEAD/GET both refused"


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("index.html")
    if not path.exists():
        print(f"ERROR: {path} not found", file=sys.stderr)
        return 2
    html = path.read_text(encoding="utf-8")

    print(f"Checking {path}\n")
    struct_errors = check_structure(html)
    if struct_errors:
        print("HTML STRUCTURE ERRORS:")
        for e in struct_errors:
            print(f"  ✗ {e}")
        print()
    else:
        print("HTML structure: OK (tags balanced)\n")

    asset_errors = check_local_assets(html, path)
    if asset_errors:
        print("LOCAL ASSET ERRORS:")
        for e in asset_errors:
            print(f"  ✗ {e}")
        print()
    else:
        print("Local assets: OK\n")

    links = sorted(set(re.findall(r'(?:href|src)="(https?://[^"]+)"', html)))
    dead: list[str] = []
    print(f"Checking {len(links)} external link(s):")
    for url in links:
        if any(h in url for h in SKIP_HOSTS):
            print(f"  ⤳ skip  {url}")
            continue
        verdict, status, detail = link_status(url)
        if verdict == "dead":
            print(f"  ✗ DEAD  {url}  ({detail})")
            dead.append(url)
        elif verdict == "ok":
            print(f"  ✓ {status}   {url}")
        else:
            print(f"  ⚠ warn  {url}  ({detail})")

    print()
    if struct_errors or asset_errors or dead:
        print("FAIL:", end=" ")
        parts = []
        if struct_errors:
            parts.append(f"{len(struct_errors)} HTML structure error(s)")
        if asset_errors:
            parts.append(f"{len(asset_errors)} missing local asset(s)")
        if dead:
            parts.append(f"{len(dead)} dead link(s)")
        print(", ".join(parts))
        return 1
    print("OK — page is well-formed, local assets exist, and no dead links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
