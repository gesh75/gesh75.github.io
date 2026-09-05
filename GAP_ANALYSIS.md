# Gap analysis — gesh75.github.io

Docs/Pages hub. No application backend. Ranked by blast radius, not ambition.

Scan date: 2026-09-05. Evidence gathered by reading the tree, running `python3 scripts/check_site.py`, and `curl -sI` against the live Pages host.

## P0 — fix now

### 1. Public financial book on the documentation hub (security)

- **Path:** `gesh-book-2026-08-23/index.html` (removed in this PR)
- **Evidence:**
  - Live URL returned **HTTP 200** on 2026-09-05: `https://gesh75.github.io/gesh-book-2026-08-23/`
  - Page title: “GESH Financial — Daily Report 2026-08-23”
  - Body listed **15 holdings** with share counts, dollar equity, and a **$19,521** portfolio total (e.g. “1.113 sh · avg $439.33”, “LLY at 16.7%”)
  - Banner text: “FRIEND BOOK — isolated run”
  - `noindex,nofollow` only hides search; the URL stayed world-readable
  - Not linked from `index.html` or `README.md`
  - `.claude/memories/omega.md` line 74: “Private repos (trading/finance, …) are **deliberately excluded** from the hub”
- **Why P0:** personal / friend portfolio data on a public Pages site. `noindex` is not access control.
- **Fix shipped:** delete the directory. Git history still contains the file (history rewrite is out of scope).

### 2. CI only gated `index.html` — sibling Pages were unchecked (CI / missing test)

- **Path:** `.github/workflows/ci.yml` (was line 26: `python3 scripts/check_site.py`)
- **Evidence:**
  - `scripts/check_site.py` defaults to `index.html` when given no path
  - CI invoked the script with no path, so `claude-skill-lint/index.html` and the financial book were never structure- or link-checked
  - No `test_*.py` existed — the only gate had no offline unit tests
  - Proved by running the checker against `claude-skill-lint/index.html` (30 external links, previously invisible to CI)
- **Why P0:** a broken project page or a leaked extra HTML file cannot fail the weekly cron.
- **Fix shipped:** unittest for structure + local assets; CI `find`s every `*.html`.

## P1 — next small jobs

### 3. Hub “90+ checks” contradicted the project page’s “89”

- **Path:** `index.html` (claude-skill-lint card); `claude-skill-lint/index.html` (meta / og + `<b>89</b>`)
- **Evidence:** hub card and both meta descriptions said “90+ checks”; the same project page’s stats row and “Checks” section say **89** rules. 89 is not 90+.
- **Fix shipped:** copy aligned to 89 (the page’s own count).

### 4. Architecture map says “nine labs” but draws eight project nodes

- **Path:** `index.html` (~line 277, “System context”)
- **Evidence:** hero / work heading say “Nine public labs”; `#grid` has 9 `.card` elements; the context SVG has 8 project `<a href="https://gesh75.github.io/…">` nodes and **no `claude-skill-lint` node** (`skill-lint in architecture svg` → false).
- **Skip this PR:** SVG layout rewrite is not a small safe edit.

### 5. README claimed “single HTML”

- **Path:** `README.md` last line (pre-fix)
- **Evidence:** tree also had `claude-skill-lint/index.html` and the financial book. Checker docs only mentioned `index.html`.
- **Fix shipped:** README now matches the two published pages and the all-HTML CI gate.

### 6. Session memory is stale (docs / DX)

- **Path:** `.claude/memories/omega.md`
- **Evidence:** still says “8 public projects”, “claude-skill-lint has **no Pages site**”, “68 MCP tools”, “netlog-ai **139 tests**”. Hub today: 9 cards, live `/claude-skill-lint/`, 69 MCP, 423 tests.
- **Skip this PR:** internal memory, not user-facing. Refresh in a dedicated docs pass.

## P2 — backlog, do not boil

| Gap | Path / evidence | Why not now |
|---|---|---|
| No `404.html` / `robots.txt` / `sitemap.xml` | missing from repo root | GitHub Pages defaults are fine; book is gone |
| No `.gitignore` | `ls` at repo root | Nothing to ignore yet |
| `TagBalance` accepts mis-nested tags | `scripts/check_site.py` `handle_endtag` pops from the match downward | Would need fixture-heavy parser work |
| No `og:image` | `index.html` head | Cosmetic |
| Google Fonts without `preconnect` / SRI | `index.html` line 16 | Perf only; SRI on Google CSS is brittle |
| Filter `role="tablist"` without tab panels | `index.html` `.filters` | A11y polish |
| No `SECURITY.md` / `CODEOWNERS` | missing | Empty ceremony on a static hub |
| Checker does not assert card count == “Nine” | `scripts/check_site.py` | Easy follow-up; see next job |
| Financial book remains in git history | `git log -- gesh-book-2026-08-23/` | History rewrite is out of scope |

## What this PR proved

- `python3 scripts/check_site.py` on `index.html`: structure OK, 13 external links, 0 dead (LinkedIn skipped).
- Same checker on `claude-skill-lint/index.html`: structure OK, 30 external links, 0 dead.
- Live `GET` of `/gesh-book-2026-08-23/` was **200** before deletion.
- Hub card count is 9; context SVG project nodes are 8.
- No secrets / API keys in the remaining tree (grep for key/token patterns only hit HMAC/docs copy).

## What we skipped

Large SVG redesign, dependency upgrades, CSP/Pages headers, git-filter-repo of the book, new product features, rewriting `.claude/memories/omega.md`, inventing a backend.

## Next recommended agent job

Add a `claude-skill-lint` node to the system-context SVG and a one-line assertion in `scripts/check_site.py` that `.card` count equals the “Nine” copy so the map and headline cannot drift again.
