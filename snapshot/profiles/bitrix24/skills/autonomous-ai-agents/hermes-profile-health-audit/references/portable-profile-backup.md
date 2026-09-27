# Portable Hermes Profile Backup and Migration

Use this procedure when a Hermes profile system must be reproducible from a private Git repository without publishing live credentials.

## Scope model

Capture the active profile plus every named profile that participates in the agent system. For each profile, preserve:

- `config.yaml` with credential-bearing fields replaced by a target-side placeholder;
- `SOUL.md`, `memories/`, `skills/`, `plugins/`, `hooks/`, `cron/`, assets, skins, widgets, and other authored extensions;
- a consistent SQLite backup of `state.db` when conversation history is requested;
- cron databases such as `cron/executions.db` when they contain scheduler state;
- installed Hermes version, source repository commit, tracked local diff, and relevant untracked source files.

Exclude `.env`, `auth.json`, OAuth/token stores, pairing material, cookies, PID/lock files, logs, caches, virtual environments, downloaded binaries, and machine-local runtime state. Generate `.env.example` with secret values replaced, preserving only safe non-secret parameters.

The built-in `hermes backup` archive includes `.env` and auth state. It is suitable for controlled local transfer, but must not be committed to Git unless separately encrypted with keys managed outside the repository.

## Consistent database capture

1. Use SQLite's online backup API instead of copying a live `state.db` byte-for-byte.
2. Run `PRAGMA integrity_check` on the copy.
3. Scan the copy for exact current credential values collected from secret stores without printing those values.
4. If a live value appears in message history, redact it in base tables. Let existing FTS triggers update search indexes.
5. Rebuild external-content FTS indexes (`messages_fts` and any trigram index), run `VACUUM`, and checkpoint/truncate WAL state. Updating rows alone can leave removed strings in FTS segments or freed pages.
6. Re-run exact-secret and credential-pattern scans on the decompressed database.
7. Compress large databases deterministically and keep every Git blob below GitHub's hard 100 MB limit.

Redaction changes only the portable snapshot, never the live source database.

## Integrity manifest

Create a machine-readable manifest containing, for every snapshot file:

- relative path;
- byte size;
- SHA-256;
- profile/database integrity status;
- source version/commit metadata.

The restore program must verify the manifest before writing anything and run SQLite integrity checks after decompression. Existing target profile data should be backed up before overwrite. Never overwrite or synthesize live credentials; require target-side setup/authentication.

## Git portability and completeness

- Add `.gitattributes` with `* -text` when the manifest is byte-exact. Otherwise Windows `core.autocrlf` can make a valid remote clone fail checksum verification.
- After staging, compare every manifest path against `git ls-files`; do not assume `git add -A` included ignored runtime databases.
- Force-add intentional database artifacts such as per-profile `cron/executions.db` when a broad `*.db` ignore rule is present.
- Exclude `.pytest_cache`, `__pycache__`, nested VCS metadata, and other generated caches before manifest generation.
- Compare each manifest SHA against the staged Git blob (`git show :path`), not only the working-tree file. A working tree can match the manifest while the Git index contains line-ending-normalized bytes.

## Required end-to-end acceptance

Do not call the migration complete after a successful push. From a fresh directory:

1. Clone the private repository from the remote provider.
2. Verify every manifest hash and count.
3. Run the secret scan against normal files and decompressed databases.
4. Restore into an isolated temporary Hermes home.
5. Run a Hermes-native read such as `hermes sessions stats` against the restored home.
6. If a source overlay is included, apply it to the pinned source commit in an isolated clone and run syntax/tests for the changed files.
7. Verify repository privacy, default branch, remote commit SHA, untruncated remote tree, total blob count, and largest blob size.
8. Confirm local HEAD, `origin/main`, and the remote API commit agree.

A clone that fails the manifest is evidence of an incomplete or non-portable publication even if `git push` succeeded.

## Report

Lead with the repository URL and privacy status, then state:

- profiles and data classes included;
- secrets and machine state intentionally excluded;
- manifest file/profile counts;
- database integrity and secret-scan results;
- exact verified remote commit;
- target-side re-authentication steps;
- the real fresh-clone restore result.
