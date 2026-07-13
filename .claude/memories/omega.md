# Session memory: omega (2026-07-11)

Snapshot of the portfolio-sync session so future Claude Code sessions can pick up where this left off.

## What this repo is

gesh75.github.io — the public documentation hub (single `index.html`, zero deps) for Georgi Gaydarov's
open-source network-automation / AI-for-NetOps projects. GitHub Pages serves `main`.

## State after this session (all merged & live)

- Hub shows **8 public projects**: argus, napalm-live-lab, multivendor-ai-network-lab,
  multivendor-cli-configurator, aegis, netlog-ai, claude-mastery-hub, claude-skill-lint.
- claude-skill-lint has **no Pages site** — its card links to the GitHub repo ("View repo →").
  All other cards link to `https://gesh75.github.io/<name>/` docs plus a `repo ↗` sublink.
- Headline numbers currently on the page: CLI configurator **70,000+ commands / 17 vendors**;
  AI lab **26 devices / 68 MCP tools**, closed-loop risk-gated auto-remediation, RFC 6241 rollback,
  vendors Juniper/Arista/Nokia SRL/FRR; napalm-live-lab **19 nodes / 2,361 commands**;
  netlog-ai **139 tests**.
- GitHub **topics** set on all public repos; **homepage** field set on all repos with live docs
  (netlog-ai's was fixed to point at its docs page, not the repo).
- Profile README (`gesh75/gesh75`) mirrors the hub's 8-project table; its stale 52K count was
  fixed to 70K (gesh75/gesh75#1, merged).
- multivendor-cli-configurator **docs landing page** (`docs/index.html`, served at
  `.../multivendor-cli-configurator/docs/`) was refreshed from the old 52,031 to the current
  **69,854** commands — every derived figure (title, meta, hero SVG, count-up chip, overview,
  feature card, 3 mermaid diagrams, components table, footer), plus role breakdown
  router/switch/firewall **43,055 / 22,656 / 4,143** and commands.json size **~18 MB**
  (gesh75/multivendor-cli-configurator#2, merged `e7d00e3`). Authoritative counts live in that
  repo's `commands.json` + `README.md`; 17 vendors / 10-node FRR lab / 870 live FRR rows /
  37 CONCEPT_SYNONYMS / 15 YANG patterns were unchanged.
- Hub PR: gesh75/gesh75.github.io#1 (merged, squash `4c2bb82`).

## CI guards added (so drift can't recur silently)

Two CI gates now enforce what this session had to fix by hand:
- **`gesh75/multivendor-cli-configurator`** — `.github/workflows/ci.yml` runs two jobs:
  1. `scripts/check_consistency.py` (stdlib) recomputes command count / per-role split /
     vendor count from `commands.json` and **fails CI** if `README.md` or `docs/index.html`
     drift. Hard-checks are the raw numbers (substring match, wording-tolerant); rounded form
     and ~MB size are advisory warnings. (PR #3, `be033b1`)
  2. `tests/stress_test.js` — the Node perf + correctness suite, now a real gate.
- **`gesh75.github.io`** (this repo) — `scripts/check_site.py` + `.github/workflows/ci.yml`
  validate `index.html` tag structure (hard gate) and card-link liveness (hard-fail only on
  404/410; transient errors warn; LinkedIn skipped). Runs on push, PR, **and weekly** cron so a
  project's Pages/repo disappearing is caught with no repo change. (PR #4, `d0cf2b3`)
- **Perf:** `lookupConcept` in the CLI configurator was re-lowercasing constant CONCEPT_SYNONYMS
  needles on every call → T6 stress test 2894ms (>1800ms target) on the grown corpus. Fixed by
  lowercasing needles once and caching on the function object (`lookupConcept._lc`); **633ms**,
  behavior-identical (concept correctness 10/10). This is why the stress suite could be gated.
  (PR #4 `cbe5de6`)
- Verified (via GitHub API) that **aegis** and **multivendor-ai-network-lab** DO serve live Pages
  from `/docs` (`docs/index.html`, plus `docs/portal.html` for the AI lab) — all 8 hub card links
  resolve; nothing dead.
- Known/deferred: none outstanding. (The T6 perf issue that was tracked is now fixed.)

## Maintenance playbook

When any project's headline numbers or positioning change, sync **these places**:
1. `index.html` here (card text + tags, hero lede, `<meta name="description">`, section counter),
2. `README.md` here (project table),
3. the profile README in `gesh75/gesh75`,
4. **that project's own docs page**, if it has one — e.g. the CLI configurator's
   `docs/index.html` in `gesh75/multivendor-cli-configurator` repeats its command count in
   ~14 spots (title/meta/hero SVG/count-up chip/overview/feature card/mermaid diagrams/table/footer)
   plus a router/switch/firewall role breakdown and a commands.json size. Grep the docs file for
   the old number before assuming it's just one edit.

Source of truth for a project's own stats: that repo's data file + `README.md` (for the CLI
configurator, `commands.json` is authoritative; the README restates the totals and role split).
Source of truth for hub descriptions: each repo's GitHub description (search `user:gesh75`).
Adding a repo to a remote session: use `add_repo` then clone (these live in separate repos, not
this one).
Private repos (trading/finance, internal MCP servers, skills library, etc.) are **deliberately
excluded** from the hub — public projects only.

## Working conventions from this session

- User prefers action over questions ("do it") and immediate merges of verified doc changes
  (draft PR → ready → squash-merge in one pass).
- Repo-settings changes (topics, homepage) can't be done from the remote session — provide
  ready-to-paste `gh repo edit` commands; the user runs them locally and confirms.
- Card style: accent color per card via `--accent`, emoji icon, 3–5 short tags, description
  mirrors the repo's GitHub description.
