# SOCIALRESEARCHER Profile

Purpose: full Agent Reach-backed research and interaction across social networks, online communities, video platforms, regional Chinese sources, professional networks, RSS, GitHub, and arbitrary web pages.

## Runtime

- Profile: `socialresearcher`
- Model/provider: `gpt-5.6-sol` via `openai-codex`
- Reasoning: high
- Approvals: smart
- Secret redaction: enabled
- Terminal: local, profile-scoped HOME
- Working directory: `C:/Users/admin/social-research-workspace`
- Delegation: up to 3 leaf workers, depth 1

## Primary routing triggers

Route here when the task requires one or more of:

- an explicit Agent Reach platform or URL;
- Twitter/X, Reddit, Facebook, Instagram, LinkedIn, XiaoHongShu, Bilibili, V2EX, Xueqiu, Xiaoyuzhou, YouTube comments/transcripts, GitHub community signals, or RSS;
- "what people say", reviews, user complaints, community experience, sentiment, reactions, comments, threads, engagement, virality, creators, influencers, forum research, social listening, or regional Chinese web research;
- authenticated platform content or a source ordinary Exa/Playwright research could not retrieve;
- cross-platform human-signal collection.

Do not route purely academic, document/PDF, official-fact, or ordinary general-web research here unless the requested question materially depends on human/platform-native evidence.

## Installed skills

- `agent-reach` — full upstream capability router and references.
- `human-signals-research` — evidence and workflow contract.
- `grounded-citations` — citation ledger and verification.
- `blocked-page-recovery` — bounded acquisition fallback.
- `youtube-content` — transcript and media synthesis.
- `blogwatcher` — RSS/Atom monitoring.

## MCP servers

- `playwright` — full 24-tool official Playwright MCP, pinned `0.0.79`, headless isolated Chrome.
- `xiaohongshu` — full 18-tool local Docker MCP on `127.0.0.1:18060`; container image pinned by digest.
- `linkedin` — full 19-tool `mcp-server-linkedin` pinned `4.22.0`, profile-local browser state, no automatic import from personal browsers.
- Exa is intentionally exposed only through Agent Reach's profile-scoped mcporter config, preventing duplicate Exa owners inside this profile.

## Agent Reach runtime

- Agent Reach `1.5.0`, source commit `93ae1d18c37b707dec053c7c4f9d91cd8ef8943d`.
- Isolated venv: `runtime/agent-reach-venv`.
- Profile command environment: `runtime/profile_exec.py`.
- Profile-scoped CLI config under `home/`.
- Installed backends include `mcporter`, OpenCLI, twitter-cli, bili-cli, rdt-cli, yt-dlp, ffmpeg, gh, Node.js, Docker and the profile MCP definitions.

Credentialed channels remain configured-but-unauthenticated until the Administrator completes the relevant platform login, QR scan, Chrome extension, or API-key flow. Credentials must remain under the profile home and never enter evidence artifacts.

## Cross-profile contract

MASTER/Kanban routes social-platform acquisition here. This profile returns `social-evidence/v1`; `researcher` remains the preferred final owner for hybrid evidence-grade reports combining official, academic, document, and social sources.

The profile does not edit Hermes project definitions. Its default cwd is outside all named Hermes projects, so profile execution cannot silently change project selection or repository state.