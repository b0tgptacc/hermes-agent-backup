# Private monorepo publishing pattern

Use when the working implementation lives below a parent Git repository that also contains specifications, evidence, or deployment documentation.

## Discovery

From the implementation directory, run `git rev-parse --show-toplevel`. If it resolves to a parent, inspect `git ls-tree --name-only HEAD` from that parent. Do not run `git init` in the child merely because a repository-creation CLI rejects `--source .` there.

## Tracked-snapshot safety

Enumerate `git ls-files -z` at the real root and check only those paths for tracked `.env`, private keys, realistic token patterns, and oversized files. Record counts and filenames, never secret values. Review placeholder matches in tests rather than treating every token-shaped string as live.

## Publish

Create the private repository from the parent root and push the accepted branch. Preserve existing history and commit identity.

## Read-back verification

Confirm through the remote API and Git transport:

- repository is private;
- default branch is correct;
- `git rev-parse HEAD` equals `git ls-remote origin refs/heads/main`;
- branch tracks `origin/main`;
- recursive remote tree is not truncated;
- both specification and implementation entry points exist.

This proves a verified upload. A separate clean-clone deployment is still required before claiming reproducibility on another device.
