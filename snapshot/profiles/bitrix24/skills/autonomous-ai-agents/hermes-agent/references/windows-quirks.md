# Windows-Specific Quirks

Hermes runs natively on Windows (PowerShell, cmd, Windows Terminal, git-bash
mintty, VS Code integrated terminal). Most of it just works, but a handful
of differences between Win32 and POSIX have bitten us — document new ones
here as you hit them so the next person (or the next session) doesn't
rediscover them from scratch.

### Input / Keybindings

**Alt+Enter doesn't insert a newline** — Windows Terminal (and mintty) grab it
for fullscreen before prompt_toolkit sees it. Use **Ctrl+Enter** instead (the
CLI binds it to newline on Windows; raw Ctrl+J does the same, harmlessly).
To inspect how your terminal reports a keystroke, run
`python scripts/keystroke_diagnostic.py` from the repo root.

### Config / Files

**HTTP 400 "No models provided" on first run** — `config.yaml` was saved with
a UTF-8 BOM (Notepad does this). Re-save as UTF-8 without BOM;
`hermes config edit` writes correctly.

### `execute_code` / Sandbox

**WinError 10106** from the sandbox child process — it can't create an
`AF_INET` socket. Root cause is usually Hermes's env scrubber dropping
`SYSTEMROOT`/`WINDIR`/`COMSPEC` (Python's `socket` needs `SYSTEMROOT` to find
`mswsock.dll`), not a broken Winsock LSP. The `_WINDOWS_ESSENTIAL_ENV_VARS`
allowlist in `tools/code_execution_tool.py` covers it; if you still hit it,
echo `os.environ` inside an `execute_code` block to confirm `SYSTEMROOT` is set.

### Desktop bootstrap fails with npm `EBADENGINE`

If `bootstrap-installer.log` reports that Hermes requires npm
`<11.10.0 || >=11.17.0` while the installed npm is in the rejected range
(for example `11.12.1`), the Desktop stage stops before dependency install.
Node itself may still satisfy the requirement. Verify live versions, install a
known-compatible npm, and rerun the failed Desktop stage:

```powershell
node --version
npm --version
npm install --global npm@11.17.0
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:LOCALAPPDATA\hermes\hermes-agent\scripts\install.ps1" -Stage desktop -IncludeDesktop -NonInteractive -Json
```

Then run the remaining non-interactive finalization stages (`config-templates`,
`platform-sdks`, and `bootstrap-marker`). The `path` stage can fail if
`bin\hermes.exe` is in use by the current Hermes session; if `hermes --version`
already works, close all Hermes CLI processes before retrying that stage, or
skip it because PATH is already functional. Verify both the bootstrap marker
and `apps\desktop\release\win-unpacked\Hermes.exe` before reporting success.

### Testing on Windows

`scripts/run_tests.sh` is POSIX-only (expects `.venv/bin/activate`); the
Hermes-installed `venv/Scripts/` has no pip/pytest (stripped for size).
Install pytest into a system Python and run directly (the repo no longer
uses pytest-xdist; the canonical runner does per-file subprocess isolation,
which the POSIX-only wrapper handles):

```bash
"/c/Program Files/Python311/python" -m pip install --user pytest pyyaml
export PYTHONPATH="$(pwd)"
"/c/Program Files/Python311/python" -m pytest tests/foo/test_bar.py -v --tb=short
```

(POSIX-only tests need skip guards — see the cross-platform guard list in
`references/contributor-guide.md`.)

### Repository-scoped one-shot delegation

**Top-level `-z/--oneshot` may ignore `--in` for terminal initialization on
Windows.** This was reproduced on Hermes v0.20.0 (2026.8.3):
`hermes --profile <name> --in C:/repo -z "..."` left terminal tools in
`C:\WINDOWS\system32`, even when `terminal.cwd: "."` was configured. When the
working directory matters, use the chat subcommand path instead:

```bash
hermes --profile <name> chat --in C:/repo -Q -q "<task>"
```

Verify with `pwd` plus `git rev-parse --show-toplevel` before destructive or
repository-specific work. The chat-subcommand form correctly anchored both
commands in the requested repository in the same environment. Re-test after a
Hermes update because this is a version-specific runtime defect, not intended
CLI semantics.

### Path / Filesystem

**Line endings.** Git may warn `LF will be replaced by CRLF`. Cosmetic — the
repo's `.gitattributes` normalizes. Don't let editors auto-convert committed
POSIX-newline files to CRLF.

**Forward slashes work almost everywhere.** `C:/Users/...` is accepted by
every Hermes tool and most Windows APIs. Prefer forward slashes in code
and logs — avoids shell-escaping backslashes in bash.

