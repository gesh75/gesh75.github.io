# Gap analysis — gesh75.github.io

Ranked scan of this docs/Pages hub. Method: read every file, run `scripts/check_site.py`, `curl -sI` live URLs, and compare hub copy to CI coverage. No product features invented.

## P0

### P0-1 — Personal portfolio HTML was a live Pages URL

- **Area:** security
- **File:** `gesh-book-2026-08-23/index.html` (removed in this PR)
- **Evidence:**
  - `curl -sI https://gesh75.github.io/gesh-book-2026-08-23/` → **HTTP 200** (GitHub Pages, 2026-09-05).
  - Page title: “GESH Financial — Daily Report 2026-08-23”. Body lists **$19,521** portfolio total, 15 tickers with **share counts** (e.g. `1.113 sh` AMGN, `7.229 sh` GOOG, `2.594 sh` LLY).
  - Commit `fa45cfd` called it “share-by-link” + `noindex`. `noindex` does not hide a public user-Pages path or a file in a public git tree.
  - Hub copy says “Private work stays private.” `.claude/memories/omega.md` says trading/finance is deliberately excluded. CI never opened this file (see P0-2).
- **Fix shipped:** delete the page. Git history still has it (history rewrite out of scope).

### P0-2 — CI only gated `index.html`

- **Area:** CI
- **Files:** `.github/workflows/ci.yml`, `scripts/check_site.py` (old default `Path("index.html")`)
- **Evidence:**
  - Workflow ran `python3 scripts/check_site.py` with no args; the script defaulted to **only** `index.html`.
  - `claude-skill-lint/index.html` is a live public page (`https://gesh75.github.io/claude-skill-lint/` → 200) with **30** external links. Those links were never a CI hard gate.
  - Manual run on that page (this scan) passed — the hole is **missing coverage**, not a current 404.
- **Fix shipped:** default to every `*.html`; add offline unit tests; CI runs both.

## P1

| ID | Area | Gap | Evidence |
|---|---|---|---|
| P1-1 | docs / DX | Stale agent memory will “correct” live facts | `.claude/memories/omega.md`: “8 public projects”, “claude-skill-lint has **no Pages site**”, AI lab **68** MCP tools, netlog-ai **139 tests**. Hub today: 9 labs, live skill-lint page, 69 MCP, 423 tests (`index.html`, `README.md`). |
| P1-2 | DX | No branded 404 | `curl -sI https://gesh75.github.io/this-does-not-exist-gap-scan` → 404, GitHub default page (`content-security-policy: default-src 'none'`). No `404.html` in repo. |
| P1-3 | docs / CI | Checker ignores relative links and `README.md` | `scripts/check_site.py` regex is `(?:href\|src)="(https?://[^"]+)"`. `favicon.svg` and README table URLs are not gated. |
| P1-4 | security | Finance page remains in git history | `git log -- gesh-book-2026-08-23/` still shows `fa45cfd`. Deletion stops Pages after the next `main` deploy; clones of old SHAs still have holdings. |
| P1-5 | CI | `scripts/check_site.py` itself is published | `curl -sI https://gesh75.github.io/scripts/check_site.py` → **200**. Low risk (stdlib), but the site has no allow-list of publishable paths. |

## P2

| ID | Area | Gap | Evidence |
|---|---|---|---|
| P2-1 | correctness | “90+ checks” vs “89” | Hub card `index.html` + skill-lint meta: “90+ checks”. Same page hero: `<b>89</b> lint checks` and “89 rules”. |
| P2-2 | docs | System-context SVG omits skill-lint as its own node | `index.html` architecture map has 8 lab nodes; Claude hub text is “skills · lint”. Nine cards exist. |
| P2-3 | DX | Missing site chrome | No `robots.txt` (live 404), no `sitemap.xml`, no `.gitignore`, no `CODEOWNERS`, no `SECURITY.md`, no `og:image`. |
| P2-4 | correctness | Tag balancer accepts crossed nesting | `check_structure("<div><span></div></span>")` returns `[]` because `handle_endtag` pops back to the matching name. Documented, not “fixed” (would be a parser rewrite). |
| P2-5 | CI | Actions unpinned | `.github/workflows/ci.yml` uses `actions/checkout@v4` and `actions/setup-python@v5` (moving tags). Stdlib site; upgrade skipped unless broken. |
| P2-6 | DX | No `.nojekyll` | User Pages defaults to Jekyll. Site works today; a later `_assets/` folder would silently not publish. |

## Dead / leftover

- **`gesh-book-2026-08-23/`** — leftover finance snapshot on a NetOps hub. Deleted.
- **`.claude/memories/omega.md`** — leftover session notes, factually wrong. Left in place (not one of the three code fixes). Safe to delete in a follow-up.

## What this PR changed (3 fixes, no more)

1. Delete `gesh-book-2026-08-23/`.
2. `check_site.py` + CI walk every HTML page.
3. Offline `tests/test_check_site.py` (structure, path discovery, LinkedIn skip).

## Skipped

Large rewrites, dependency upgrades, new 404/robots chrome, history rewrite, pinning Actions by SHA, inventing backend features, syncing project stats across other repos.

## Next recommended agent job

Delete or rewrite `.claude/memories/omega.md` so agents stop treating the July 2026 hub snapshot as source of truth, then add a one-file `404.html` that links back to the nine lab cards.
