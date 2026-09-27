"""Invoke the socialresearcher profile without shell interpolation."""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

MAX_PROMPT_BYTES = 1024 * 1024
DEFAULT_HERMES = Path(r"C:\Users\admin\AppData\Local\hermes\hermes-agent\bin\hermes.exe")
PROFILE_ROOT = Path(r"C:\Users\admin\AppData\Local\hermes\profiles\socialresearcher")
PROFILE_HOME = PROFILE_ROOT / "home"
PROFILE_VENV = PROFILE_ROOT / "runtime" / "agent-reach-venv" / "Scripts"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--workdir")
    parser.add_argument("--timeout", type=int, default=900)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    prompt_path = Path(args.prompt_file).resolve()
    if not prompt_path.is_file():
        print(f"prompt file not found: {prompt_path}", file=sys.stderr)
        return 2
    if prompt_path.stat().st_size > MAX_PROMPT_BYTES:
        print("prompt file exceeds 1 MiB", file=sys.stderr)
        return 2
    prompt = prompt_path.read_text(encoding="utf-8")
    if not prompt.strip():
        print("prompt file is empty", file=sys.stderr)
        return 2

    hermes = shutil.which("hermes")
    if not hermes and DEFAULT_HERMES.is_file():
        hermes = str(DEFAULT_HERMES)
    if not hermes:
        print("hermes executable not found", file=sys.stderr)
        return 127

    cmd = [hermes, "-p", "socialresearcher", "chat"]
    if args.workdir:
        workdir = Path(args.workdir).resolve()
        if not workdir.is_dir():
            print(f"workdir not found: {workdir}", file=sys.stderr)
            return 2
        cmd.extend(["--in", str(workdir)])
    cmd.extend(["--source", "tool", "--max-turns", "150", "-Q", "-q", prompt])

    env = dict(os.environ)
    # Nested Hermes invocations inherit the parent agent's bridged profile and
    # terminal variables. Remove them so `-p socialresearcher` owns its runtime.
    for key in list(env):
        if key.startswith("TERMINAL_") or key in {
            "HERMES_HOME",
            "HERMES_REAL_HOME",
            "HERMES_SESSION_ID",
            "HERMES_KANBAN_BOARD",
            "HERMES_DELEGATED_CHILD_CONTEXT",
            "HERMES_AGENT",
            "HERMES_MAX_ITERATIONS",
            "HERMES_INTERACTIVE",
            "HERMES_QUIET",
        }:
            env.pop(key, None)
    env["TERMINAL_HOME_MODE"] = "profile"
    env["HOME"] = str(PROFILE_HOME)
    env["USERPROFILE"] = str(PROFILE_HOME)
    env["XDG_CONFIG_HOME"] = str(PROFILE_HOME / ".config")
    env["MCPORTER_CONFIG"] = str(PROFILE_HOME / ".mcporter" / "mcporter.json")
    env["NPM_CONFIG_PREFIX"] = str(PROFILE_HOME / ".npm-global")
    profile_paths = [
        PROFILE_VENV,
        PROFILE_HOME / ".local" / "bin",
        PROFILE_HOME / ".npm-global",
        PROFILE_HOME / ".npm-global" / "bin",
    ]
    env["PATH"] = os.pathsep.join(
        [str(path) for path in profile_paths if path.exists()]
        + ([env.get("PATH", "")] if env.get("PATH") else [])
    )
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"
    try:
        result = subprocess.run(
            cmd,
            env=env,
            encoding="utf-8",
            errors="replace",
            timeout=max(30, args.timeout),
        )
    except subprocess.TimeoutExpired:
        print("socialresearcher invocation timed out", file=sys.stderr)
        return 124
    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
