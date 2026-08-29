# gesh75.github.io

Documentation hub for open-source network automation & AI-for-NetOps projects.

**Live → https://gesh75.github.io/**

Senior network engineering leader. AI tools builder. The hub lists every public
lab and reference — with filters, principles, and the stack — not just a card
grid.

## Projects linked from the hub

| Project | What it is |
|---|---|
| [argus](https://github.com/gesh75/argus) | Fail-closed defensive assessment orchestrator. Supervised V1 RC; experimental V2 with an out-of-band HMAC signer and operator-gated evidence graph |
| [aegis](https://github.com/gesh75/aegis) | Air-gapped pre-deployment change validation. v0.2.0: G1–G5 promotion, fail-closed idle BGP, detached Ed25519 seals, 11 frameworks |
| [multivendor-ai-network-lab](https://github.com/gesh75/multivendor-ai-network-lab) | 26-device lab that remediates — Phase 6 Lab Ops portal, 69 MCP tools, RFC 6241 confirmed-commit rollback, immutable GAIT |
| [napalm-live-lab](https://github.com/gesh75/napalm-live-lab) | Live multivendor NAPALM coverage matrix + safe-by-default command console (Arista cEOS / Nokia SR Linux / FRR in containerlab) |
| [netlog-ai](https://github.com/gesh75/netlog-ai) | Sanitize-first AI log analyzer — 0.6 in flight: Grok, causal timeline, 80 patterns, 423 tests, MCP connectors (Kibana/Splunk/Loki/syslog/LibreNMS) |
| [multivendor-cli-configurator](https://github.com/gesh75/multivendor-cli-configurator) | 70,000+ CLI commands across 17 vendors — searchable cheatsheet **plus CLI Studio** (intent, migrate, recipes, EOS/FRR/VyOS parsers, FRR lab) |
| [network-observability-architecture](https://github.com/gesh75/network-observability-architecture) | v2.0 interactive console: OTLP/Alloy, Tempo, gNMI, freshness SLOs, dual-signal lab, read-only AI control plane |
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
