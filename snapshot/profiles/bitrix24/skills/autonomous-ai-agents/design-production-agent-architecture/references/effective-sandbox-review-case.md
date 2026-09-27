# Effective sandbox review case

## Why this case matters

A post-remediation design-agent profile looked secure in raw YAML and its validator reported PASS. Independent review of the runtime loader and Docker environment constructor found that the claimed boundary was not the effective boundary.

## Configuration/effective-state mismatch

The profile used a plausible key equivalent to `docker_persistent: false`, while the runtime consumed a canonical field equivalent to `container_persistent`. The unknown key was ignored and the effective value defaulted to true.

A host-form terminal cwd pointed at the controlled staging folder. Because automatic cwd mounting was disabled, the container backend rejected that host path and resolved its working directory to `/root`. The runtime then passed `docker run -w /root`, overriding the image's `/workspace` WORKDIR.

Durable lesson: validate canonical runtime keys and compare raw versus resolved values. Security-sensitive unknown keys must fail closed.

## Hidden mount expansion

The explicit volume list contained only the staging workspace, but the Docker constructor also added:

- a persistent home bind because persistence had defaulted on;
- the profile skill directory;
- existing document/media/web/delegation caches and attachment directories;
- any declared credential or proxy mounts when applicable.

Some mounts were read-only, but they still expanded confidentiality scope and exposed prior-task data. The correct invariant is an exact effective mount allowlist, not “one explicit volume” or a short forbidden-substring scan.

## Why acceptance gave false confidence

The acceptance script ran a manually assembled `docker run --network=none -v staging:/workspace ...` command. It proved non-root execution, blocked networking, imports, and the staging mount for that command. It bypassed the agent framework's loader, cwd guard, persistence defaults, environment factory, and automatic mounts.

A production-boundary acceptance test must either:

1. invoke the same environment factory used by terminal/file/code tools and inspect the resulting container; or
2. deterministically inspect the exact generated run arguments and resolved configuration.

Test all enabled execution toolsets, especially when file and code-execution paths construct their own container-config dictionaries.

## Stale live containers after remediation

A later review found the YAML, image manifest, Dockerfile, and hashed lock had all been corrected, and the desired minimized image passed a standalone probe. However, a still-running profile container had been created before the change and continued to use the old image, old working directory, persistent host home, and test-only packages.

This is a separate failure mode from a bad config: the desired artifact can be correct while the deployed process keeps a cached environment alive. Inventory all running and exited containers for the profile, inspect their immutable image IDs and effective HostConfig, and compare them with the current manifest. Treat a mismatched running container as current operational drift, not historical noise.

Deployment changes to image, cwd, mounts, user, network, persistence, or environment forwarding require an explicit restart/eviction gate. A validator should fail when any live profile container is stale, even if a fresh handcrafted container would pass. A working remediation pattern is:

1. add a profile-scoped switch that makes framework-added profile mounts fail closed (for example `terminal.docker_auto_mount_profile_data: false`), while preserving the historical default for ordinary profiles;
2. bridge that setting through every CLI/gateway config-to-environment path that can construct the backend;
3. make credential/skill/cache mount registries return an empty list when strict mode is active;
4. add a targeted unit test proving all three registries are empty in strict mode;
5. evict every container carrying the profile label before acceptance;
6. run terminal, file, and code-execution probes through Hermes itself;
7. parse `/proc/self/mountinfo` and require the exact host-bind destination set, not a forbidden-name heuristic;
8. assert that no profile-labeled container survives a per-session acceptance run.

In the validated case, this sequence produced UID 10001, cwd `/workspace`, blocked network, no test framework, no credential/profile-cache/host-venv visibility, exactly one host bind (`/workspace`), and no surviving profile container. A doctor or diagnostic command may itself create an exited probe container using a different construction path; put an explicit profile-container eviction step immediately before the canonical validator so diagnostic residue cannot cause false drift or remain deployable.

Useful non-secret comparison fields are:

- container ID, state, profile/task labels, and creation time;
- immutable image ID, configured image ID, and human tag;
- user, working directory, network mode, and environment-variable names only;
- every bind source/destination/mode;
- persistent-home or cross-process-reuse state;
- presence of test-only packages in the effective live image.

## Validator requirements

A robust pre-auth validator should assert:

- raw and resolved backend/image/cwd;
- canonical persistence and cross-process-reuse fields;
- network mode and effective user;
- forwarded environment-variable names without values;
- complete generated mount sources/destinations/modes;
- the actual terminal, file, and code-execution environment path;
- inventory and manifest comparison for every live profile container;
- exact MCP include allowlist and absence of mutation tools;
- exact governance status markers in operator documentation;
- a `--check` or `--no-write` mode for independent read-only review.

Do not let a report's self-declared PASS substitute for checking configured and effective state.
