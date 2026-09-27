# Read-only CLI inventory discipline

Use explicit non-interactive subcommands during health audits. A bare CLI noun may open a configuration UI and persist selections even when the operator intended only to inspect state.

## Safe pattern

1. Read `<command> --help` before inventorying an unfamiliar surface.
2. Prefer `list`, `show`, `status`, `check`, `--summary`, `--plain`, or `--json` forms.
3. For Hermes tool inventory use `hermes tools list` or `hermes tools --summary`; do not use bare `hermes tools` in a read-only audit.
4. Prefer `hermes plugins list --enabled --plain` when only active plugins matter; avoid treating the full bundled catalog as active runtime state.
5. If an interactive UI opens unexpectedly, exit without confirming and re-check the resulting configuration before continuing.

This rule applies to any setup, model, tool, plugin, profile, or provider command whose no-argument form may be a wizard or editor.
