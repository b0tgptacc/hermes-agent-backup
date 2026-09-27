# Profile-scoped capability-router deployment

Use this reference when a broad installer/router skill (social platforms, scraping backends, browser-session tools, multiple MCPs) deserves its own Hermes profile instead of being added to an existing evidence-first or developer profile.

## Architectural decision

Create a separate profile when the candidate has broad triggers, heterogeneous dependencies, login/cookie state, or a faster update/risk cadence than the existing profile. Define it as a specialist acquisition role, not a second owner of every research phase.

Keep routing explicit:

- platform-native human/community evidence -> capability-router profile;
- official, academic, document, or ordinary general-web evidence -> established researcher;
- hybrid task -> split by evidence class; MASTER/Kanban integrates;
- profiles do not recursively invoke each other.

Give the profile a precise `--description` so Kanban can route by role. Add a default-profile routing skill with positive triggers, negative triggers, hybrid rules, and at least one real invocation test.

## Profile creation and isolation

Prefer a blank profile (`hermes profile create <name> --no-skills --description ...`) and a dedicated absolute `terminal.cwd`. Do not clone a production researcher: copying its skills and MCPs recreates overlap.

Hermes profiles isolate Hermes state through `HERMES_HOME`, but local subprocesses may still share OS-user state. For credential-bearing external CLIs:

- configure `terminal.home_mode: profile`;
- keep runtime/venv, npm prefix, uv tool directories, XDG config, browser state, and tool config under the profile;
- set profile-local `HOME`, `USERPROFILE`, `XDG_CONFIG_HOME`, `NPM_CONFIG_PREFIX`, `UV_TOOL_DIR`, `UV_TOOL_BIN_DIR`, and PATH in the profile launcher/runner when the external tools use different home-resolution conventions;
- use dedicated platform accounts and browser profiles; a Hermes profile is not an OS sandbox;
- bind local MCP HTTP ports to `127.0.0.1` and pin container images by digest.

After an upstream installer, inspect and remove/migrate global spill such as user-level skill copies, MCP config, runtime config, npm globals, or cookie stores. Verify the default PATH does not expose the specialist CLIs.

## Nested Hermes invocation trap

A Hermes process launched from another Hermes terminal inherits the parent's bridged `HERMES_*` and `TERMINAL_*` variables. Merely passing `-p <target>` can load the target SOUL/skills while terminal subprocesses still observe the parent's home, cwd, or tool config.

Use a no-shell runner (`subprocess.run([...], shell=False)`) that:

1. reads the delegated prompt from a bounded UTF-8 file;
2. removes inherited `TERMINAL_*` variables;
3. removes parent-scoped `HERMES_HOME`, `HERMES_REAL_HOME`, session/kanban/delegation/profile markers, and inherited iteration/quiet flags;
4. sets the target profile's `TERMINAL_HOME_MODE=profile`, HOME/USERPROFILE/XDG paths, and profile-local PATH;
5. invokes `hermes -p <target> chat ...` as an argument list;
6. passes `--in` only for an explicit validated absolute workdir;
7. never changes `hermes project use`.

Acceptance must inspect the child terminal, not just the child prose. Require the child to print its real `HERMES_HOME`, `TERMINAL_HOME_MODE`, HOME, USERPROFILE, XDG config and `command -v` results for specialist binaries.

## Skills and MCP composition

Install one routing/execution skill, one domain methodology/evidence skill, and only complementary ingestion/citation skills. Broad skill triggers are acceptable inside the dedicated profile but must not leak into global skill roots.

For MCP:

- pin stdio package versions and container digests;
- record transport, profile-local state, tool count, and auth state;
- configure full catalogs only when explicitly required; otherwise allowlist unique tools;
- distinguish `connected/tools discovered` from `authenticated` and from a successful representative operation;
- test login/status calls without silently importing personal browser cookies.

## Credential boundaries

A fully installed channel can still be unauthenticated. Classify each channel as:

- public and outcome-verified;
- connected/configured but unauthenticated;
- authenticated and outcome-verified;
- blocked/unavailable.

Passwords, API keys, cookies, QR scans, browser-extension consent, CAPTCHA, and account login require human interaction. Never convert missing user input into a false PASS. Preserve the installed/configured state and report the shortest interactive completion path.

## Routing acceptance

Test all three cases:

1. Positive: a real named-platform task routes to the specialist and returns real evidence.
2. Negative: an official/document/academic task stays with the established researcher.
3. Hybrid: authoritative and community workstreams split cleanly, with MASTER as final owner.

The positive test must exercise the routing runner, profile identity, relevant skill load, and one real platform result. The hybrid test must state evidence classes, not merely profile names.

## Project and regression safety

Before changes, capture:

- `hermes project list`;
- profile list;
- hashes of default and existing profile config/SOUL/PROFILE files;
- global PATH presence of candidate CLIs;
- relevant global config directories.

After changes, prove:

- project list/selection is unchanged;
- existing profile hashes are unchanged;
- specialist CLIs/config exist only in the new profile scope;
- no global skill copy was left by the installer;
- profile config parses, skills load, MCPs connect, model access works;
- fresh-session real search, browser navigation/snapshot, and platform calls pass;
- citation/evidence verification passes when the profile produces reports.

Keep a profile-local acceptance record listing PASS evidence, authenticated state, residual blockers, pinned versions/digests, and non-blocking Hermes advisories.