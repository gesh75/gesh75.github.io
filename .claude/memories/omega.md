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
- Hub PR: gesh75/gesh75.github.io#1 (merged, squash `4c2bb82`).

## Maintenance playbook

When any project's headline numbers or positioning change, sync **three places**:
1. `index.html` here (card text + tags, hero lede, `<meta name="description">`, section counter),
2. `README.md` here (project table),
3. the profile README in `gesh75/gesh75`.

Source of truth for descriptions: each repo's GitHub description (search `user:gesh75`).
Private repos (trading/finance, internal MCP servers, skills library, etc.) are **deliberately
excluded** from the hub — public projects only.

## Working conventions from this session

- User prefers action over questions ("do it") and immediate merges of verified doc changes
  (draft PR → ready → squash-merge in one pass).
- Repo-settings changes (topics, homepage) can't be done from the remote session — provide
  ready-to-paste `gh repo edit` commands; the user runs them locally and confirms.
- Card style: accent color per card via `--accent`, emoji icon, 3–5 short tags, description
  mirrors the repo's GitHub description.
