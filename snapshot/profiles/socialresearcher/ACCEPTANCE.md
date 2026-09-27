# SOCIALRESEARCHER Acceptance Record

Verified: 2026-08-20T07:30:03Z on Windows 11, Hermes Agent 0.20.4.

## PASS

- Profile identity/model: fresh call returned `SOCIALRESEARCHER_MODEL_OK`; OpenAI Codex auth healthy.
- Config schema: v38, `hermes config check` passed.
- Profile inventory: six enabled local skills.
- MCP connection/discovery:
  - Playwright: 24/24 tools, connected.
  - XiaoHongShu: 18/18 tools, connected through local Docker MCP.
  - LinkedIn: 19/19 tools, connected.
  - Exa is intentionally configured once through profile-scoped mcporter, not duplicated as native Hermes MCP.
- Real backend/MCP calls:
  - Agent Reach mcporter Exa search returned `https://hermes-agent.nousresearch.com/` from the absolute profile config.
  - Playwright navigated `https://example.com` and captured heading `Example Domain`.
  - XiaoHongShu `check_login_status` executed and correctly reported unauthenticated.
- Agent Reach 1.5.0 loaded from pinned commit `93ae1d18c37b707dec053c7c4f9d91cd8ef8943d`.
- Public backend calls:
  - Bilibili `bili-cli`: real result `BV13YRjBTEPb`.
  - V2EX public API: non-empty current response.
  - RSS/feedparser: 20-item feed response.
  - Jina Reader: retrieved Example Domain.
  - YouTube/yt-dlp: real metadata call with Node JS runtime configured.
- End-to-end routing:
  - MASTER routed a Bilibili task to `socialresearcher` and returned real evidence.
  - An official Python release task stayed with `researcher`.
  - A hybrid official + Reddit/X/Bilibili task split between `researcher` and `socialresearcher`, final owner MASTER.
- End-to-end social research loaded `human-signals-research` and `agent-reach`, returned a real Bilibili evidence item and a correctly bounded V2EX `no_match`.
- Grounded-citations deterministic smoke: strict evidence verification passed with 100% declared provenance coverage.
- Isolation:
  - Nested routing runner strips inherited Hermes/terminal profile variables.
  - Routed child observed the correct profile `HERMES_HOME` and profile-scoped HOME.
  - Profile runtime CLIs resolve only inside the routed profile environment.
  - `MCPORTER_CONFIG` is pinned to an absolute profile-owned file, so project-level mcporter config cannot override Agent Reach routing.
  - Native Exa MCP was removed to prevent duplicate Exa ownership; Agent Reach mcporter is the sole Exa route in this profile.
  - Resolved npm/uv/Python/MCP/container versions are recorded in `runtime/LOCK.json`; automatic updates are disabled by policy.
  - Rollback dry-run completed through `runtime/rollback_socialresearcher.py` without changing state.
  - No global Agent Reach, mcporter, OpenCLI, twitter, bili, or rdt commands remain on the default PATH.
  - Global spill directories `.agent-reach`, `.mcporter`, and `.agents/skills/agent-reach` were removed after migration.
- Existing-state protection:
  - 11/11 captured config/SOUL/PROFILE hashes for default, designer, developer, and researcher remained unchanged.
  - `hermes project list` remained `No projects yet` before and after all tests.

## INSTALLED BUT REQUIRES ADMINISTRATOR LOGIN/SECRET

These capabilities are present but cannot be truthfully accepted as authenticated without human account interaction:

- OpenCLI Chrome/Edge extension and platform sessions: Reddit, Facebook, Instagram, XiaoHongShu browser route, Bilibili subtitles, and Xueqiu browser route.
- Twitter/X: explicit account cookies or dedicated browser session.
- LinkedIn: interactive login into the profile-local browser state.
- XiaoHongShu: QR/login into the profile-local Docker MCP state.
- Xiaoyuzhou/Whisper fallback: Groq or OpenAI transcription key.
- GitHub private/authenticated operations: profile-specific `gh auth login`.

The Administrator did not respond to the interactive authorization decision before timeout. No credentials were guessed, copied, printed, or imported from personal browsers.

## Non-blocking Hermes advisories

- Hermes uses SQLite 3.45.1 but this profile's state DB is in rollback journal mode and is not exposed to the WAL-reset bug.
- Hermes doctor reports build-time npm advisories in shared Hermes web/ui workspaces; these were pre-existing and are unrelated to the new profile.
- Built-in browser/search providers lack their optional API credentials; the verified Exa and Playwright MCP paths are operational.
