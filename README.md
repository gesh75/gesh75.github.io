# gesh75.github.io

Documentation hub for open-source network automation & AI-for-NetOps projects.

**Live → https://gesh75.github.io/**

Senior network engineering leader. AI tools builder. The hub lists every public
lab and reference — with filters, principles, and the stack — not just a card
grid.

## Projects linked from the hub

| Project | What it is |
|---|---|
| [argus](https://github.com/gesh75/argus) | Agentic AI penetration tester — network/host/AD/web, read-only by default behind a fail-closed 7-layer guardrail, HMAC-audited |
| [aegis](https://github.com/gesh75/aegis) | Air-gapped pre-deployment change validation against a containerlab digital twin, with sealed PCI/SOC2/NIST evidence |
| [multivendor-ai-network-lab](https://github.com/gesh75/multivendor-ai-network-lab) | 26-device multivendor AI network lab with closed-loop, risk-gated auto-remediation and RFC 6241 confirmed-commit rollback |
| [napalm-live-lab](https://github.com/gesh75/napalm-live-lab) | Live multivendor NAPALM coverage matrix + safe-by-default command console (Arista cEOS / Nokia SR Linux / FRR in containerlab) |
| [netlog-ai](https://github.com/gesh75/netlog-ai) | Sanitize-first AI network log analyzer (Junos / EOS / FRR) with LLM-assisted root-cause playbooks |
| [multivendor-cli-configurator](https://github.com/gesh75/multivendor-cli-configurator) | 70,000+ CLI commands across 17 vendors & tools — searchable, comparable, zero-dependency single-HTML cheatsheet |
| [network-observability-architecture](https://github.com/gesh75/network-observability-architecture) | Vendor-neutral reference architecture for observability and source-of-truth management (NetBox, dual-signal alerts) |
| [claude-mastery-hub](https://github.com/gesh75/claude-mastery-hub) | Interactive single-page guide to mastering Claude — app, Claude Code, API, MCP, skills, subagents, hooks |
| [claude-skill-lint](https://github.com/gesh75/claude-skill-lint) | Zero-dependency linter for Claude Code skills — frontmatter, progressive disclosure, dead refs, stale model IDs |

## What this redesign fixed

- Missing project: `network-observability-architecture`
- Nested `<a>` inside project cards (invalid HTML)
- No about, principles, stack, or search
- Emoji-as-icons and aurora-blob background
- Stale “8 projects” count
- No skip-to-content or keyboard search (`/` focuses the filter)

Zero-dependency single HTML. `python3 scripts/check_site.py` still gates structure and link liveness in CI.
