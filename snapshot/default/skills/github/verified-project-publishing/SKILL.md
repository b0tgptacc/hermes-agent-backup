---
name: verified-project-publishing
description: "Use when publishing verified projects to remote Git."
version: 1.0.0
author: Hermes Curator
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [github, publishing, release, verification, secrets, reproducibility]
    category: github
---

# Verified Project Publishing

Publish an existing, verified local project to a private or public Git remote without losing history, leaking credentials, pushing the wrong subtree, or mistaking a successful push message for a verified remote release.

Use this after implementation acceptance when the deliverable is the complete project: code, specifications, deployment files, tests, and restore instructions.

## Core Standard

Publishing is complete only when:

1. The actual Git root and intended repository scope are confirmed.
2. The working tree is clean or every pending change is intentionally committed.
3. The tracked snapshot—not arbitrary filesystem contents—passes secret and size checks.
4. Repository visibility is explicit.
5. The remote default branch points to the exact local commit.
6. Critical project paths are visible through the remote API.
7. Reproducible deployment is distinguished from upload-only completion.

## 1. Discover the Repository Boundary

Always start with:

```bash
git rev-parse --show-toplevel
git status --short --branch
git log -1 --oneline --decorate
git remote -v
```

Do not assume the current directory is the Git root. Plain `git` commands search parent directories, while repository-creation tools may require `--source` to be the exact root. A project implementation may be a subdirectory of a larger repository that also contains specifications and validation evidence.

Inspect the top-level tree from the resolved root:

```bash
git ls-tree --name-only HEAD
```

Confirm whether the intended deliverable is the implementation subtree or the complete parent repository before creating the remote.

## 2. Verify Before Publishing

Run the project's accepted verification gates before push:

- full regression suite;
- runtime/container health when applicable;
- smoke/E2E acceptance;
- independent review status;
- clean Git state.

Report each scope separately. A healthy container does not replace regression or acceptance evidence.

## 3. Scan the Tracked Snapshot

Scan `git ls-files`, not the entire working directory. This avoids reading ignored live credentials while proving what will actually be pushed.

At minimum verify:

- no tracked `.env` files;
- no private-key headers;
- no GitHub/access-token patterns;
- no credential assignments with realistic values;
- no files near the hosting provider's hard size limit;
- total tracked size and file count are reasonable.

Review every match. Test fixtures such as `ACxxxxxxxx`, `example_token`, or assertions about `.env.example` are not secrets, but they must be classified rather than silently ignored.

Never print credential values in logs or normal responses. Report filenames and counts only.

## 4. Create the Remote Explicitly

Default to the user's previously established visibility preference; otherwise clarify private versus public because that changes disclosure risk.

From the exact Git root:

```bash
gh repo create OWNER/REPO \
  --private \
  --source . \
  --remote origin \
  --push \
  --description "..."
```

If creation from a subdirectory says it is not a Git repository even though `git status` worked, do not run `git init`. Resolve the parent root and retry there, preserving the original history.

## 5. Verify the External State

After push, read the remote back:

```bash
gh repo view OWNER/REPO --json nameWithOwner,isPrivate,url,defaultBranchRef
git rev-parse HEAD
git ls-remote origin refs/heads/main
git status --short --branch
gh api 'repos/OWNER/REPO/git/trees/main?recursive=1'
```

Require:

- expected visibility;
- expected default branch;
- local SHA equals remote branch SHA exactly;
- local branch tracks the remote;
- remote tree is not truncated;
- critical implementation, specification, deployment, and restore files exist.

A command returning exit code zero is not enough; verify these resulting properties.

## 6. Upload Versus Reproducibility

State the achieved level precisely:

- **Uploaded:** remote exists and exact commit is present.
- **Repository verified:** visibility, SHA, tree, and critical paths are confirmed.
- **Reproducible:** a clean clone was deployed and acceptance tests passed.

Do not claim reproducibility merely because Docker or setup instructions are present. If the user requested a cross-device restore guarantee, clone into a clean location/environment and execute the documented deployment and acceptance flow.

## Pitfalls

- Running repository creation from a nested folder and then incorrectly reinitializing Git.
- Scanning only the implementation subtree when the parent repository will be pushed.
- Scanning ignored live `.env` values instead of the tracked snapshot.
- Treating placeholder credentials in tests as live secrets without review.
- Declaring success from `git push` without comparing remote SHA.
- Publishing publicly when the user's established preference is private.
- Saying “fully reproducible” before a clean-clone deployment.

## Verification Checklist

- [ ] Actual Git root resolved.
- [ ] Intended repository scope confirmed.
- [ ] Working tree clean and accepted commit identified.
- [ ] Tracked snapshot scanned for secrets and oversized files.
- [ ] Visibility explicit.
- [ ] Remote created from the exact root.
- [ ] Local and remote SHA match.
- [ ] Default branch and tracking confirmed.
- [ ] Remote tree contains critical project assets and is not truncated.
- [ ] Upload versus clean-clone reproducibility reported accurately.

## References

- `references/private-monorepo-publish.md` — concise worked pattern for a parent repository containing specifications plus an implementation subtree.
