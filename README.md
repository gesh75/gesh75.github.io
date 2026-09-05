# gesh75.github.io

Documentation hub for open-source network automation & AI-for-NetOps projects.

**Live → https://gesh75.github.io/**

Command-center visual language shared with [Aegis](https://gesh75.github.io/aegis/): dark navy, teal / emerald / amber, glass panels, and animated architecture diagrams. Senior network engineering leader. AI tools builder. The hub lists every public lab and reference — with filters, a closed-loop map, principles, and the stack.

## Projects linked from the hub

| Project | What it is |
|---|---|
| [argus](https://github.com/gesh75/argus) | Fail-closed defensive assessment orchestrator — 7-layer guardrail, OOB HMAC signer (PR #18), 315 tests, unattended mode locked |
| [aegis](https://github.com/gesh75/aegis) | Air-gapped change validation. v0.2.0: G1–G5 promotion, HMAC approval tokens (aegis1.), fail-closed idle BGP, detached Ed25519 seals, 11 frameworks |
| [multivendor-ai-network-lab](https://github.com/gesh75/multivendor-ai-network-lab) | 26-device lab that remediates — Phase 6 Lab Ops portal, 69 MCP tools, RFC 6241 confirmed-commit, honest GAIT |
| [napalm-live-lab](https://github.com/gesh75/napalm-live-lab) | Live multivendor NAPALM coverage matrix + safe-by-default command console (Arista cEOS / Nokia SR Linux / FRR in containerlab) |
| [netlog-ai](https://github.com/gesh75/netlog-ai) | Sanitize-first AI log analyzer — v0.6.0: Grok, causal timeline, 80 patterns, 423 tests, MCP connectors |
| [multivendor-cli-configurator](https://github.com/gesh75/multivendor-cli-configurator) | 70,000+ CLI commands across 17 vendors — searchable cheatsheet **plus CLI Studio** (intent, migrate, recipes, EOS/FRR/VyOS parsers, FRR lab) |
| [network-observability-architecture](https://github.com/gesh75/network-observability-architecture) | v2.0 interactive console: OTLP/Alloy, Tempo, gNMI, freshness SLOs, dual-signal lab, read-only AI control plane |
| [claude-mastery-hub](https://github.com/gesh75/claude-mastery-hub) | Interactive single-page guide to mastering Claude — app, Claude Code, API, MCP, skills, subagents, hooks |
| [claude-skill-lint](https://github.com/gesh75/claude-skill-lint) | v0.5.0 linter — 2026 models, computer-use safety, NetOps pack. Live page: https://gesh75.github.io/claude-skill-lint/ |

Zero-dependency HTML. `python3 scripts/check_site.py` gates structure and link liveness for every `*.html` page in CI. Offline checker tests: `python3 -m unittest discover -s tests -v`.
