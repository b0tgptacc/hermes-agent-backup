# Code Knowledge-Graph Tool Evaluation

Use this reference when evaluating AST/call-graph/GraphRAG tools proposed for coding agents. The decision question is not whether the tool can generate a graph; it is whether the graph improves verified engineering outcomes enough to justify indexing, prompt, dependency, and maintenance cost.

## 1. Establish source identity

- Verify the canonical project domain from repository metadata, package metadata, and maintainer-controlled documentation.
- Treat similarly named domains and packages as unaffiliated until provenance is confirmed.
- Pin the reviewed repository commit, package version, release, license, and timestamp.
- Separate adoption signals (stars, forks, downloads) from engineering quality.
- Treat pre-1.0 status and unusually rapid release cadence as change-risk signals, not automatic rejection.

## 2. Inspect every integration surface

Evaluate the CLI/library, vendor skill, MCP server, hooks/watch mode, hosted service, and database exporters separately. A sound core library does not make every integration appropriate.

For agent stacks, prefer this order unless evidence supports escalation:

1. isolated, pinned local CLI;
2. short curator-managed wrapper skill;
3. MCP only when persistent typed query tools outperform terminal invocation enough to justify schema/context overhead;
4. hooks, watchers, global indexes, remote databases, and hosted services only after explicit operational and security approval.

Never run a vendor installer against a production profile before probing it in a redirected temporary home and writable scratch project. Test each documented install spelling: commands that appear equivalent may write different artifacts (for example, a skill-only install versus a platform subcommand that also modifies project instruction files).

Verify profile safety. An installer that writes a global default path rather than the active profile home is not suitable for profile-scoped deployment without adaptation.

## 3. Audit the vendor skill as executable policy

Read the full installed skill, references, and injected project instructions. Measure:

- SKILL.md bytes and lines;
- total bundle bytes/files;
- trigger breadth;
- auto-install or auto-upgrade behavior;
- project-file mutations;
- assumed shell, Python command, agent tool names, and concurrency model;
- mandatory fan-out or instructions that prohibit native inspection;
- overlap with native search, structural search, codebase inspection, debugging, and review.

Do not install a broad vendor skill merely because it supports the runtime by name. Prefer an adapted wrapper when the vendor skill owns too many phases, assumes another host's tools, or imposes large always-loaded context.

## 4. Run an evidence-producing smoke ladder

Use an isolated environment and test progressively:

### A. Synthetic known-answer fixture

Create a tiny multi-file project containing known imports, inheritance, direct calls, member calls, and one expected impact chain. Build the graph and exercise:

- explain a symbol;
- path between two symbols;
- reverse/affected traversal;
- exact-symbol query;
- natural-language query.

Compare returned edges to source truth programmatically or by a fixed checklist. Record both false positives and false negatives. A provenance label such as `EXTRACTED` proves how a present edge was produced; it does not prove completeness or the absence of missing edges.

### B. Representative repository

Run a code-only build on a medium/large real repository. Record:

- files scanned and skipped;
- unsupported-language/dependency warnings;
- raw node/edge counts;
- wall time;
- output size;
- no-change incremental time and re-queued files;
- clustering/final graph counts.

Run two clean builds and compare a canonicalized graph hash that excludes timestamps and non-semantic ordering. Then run a no-change incremental build. Count changes between raw extraction and final clustered/exported forms rather than assuming the displayed totals represent the same schema.

### C. Owning-platform installation

Redirect all global/profile paths to a temporary root. Verify exact created files, version stamp, sidecars, instruction-file edits, and uninstall behavior. Then load the skill through the target profile/runtime if a safe isolated profile is available.

### D. Tests on the target OS

Run the relevant upstream tests on the deployment OS. Inspect CI matrices directly: a green Linux CI run is not Windows acceptance. Distinguish a test portability failure from a runtime defect, but record both as evidence of coverage gaps. Check whether security scans are blocking or `continue-on-error`.

## 5. Security and data-flow review

Classify modes independently:

- local deterministic code parsing;
- semantic processing of docs/media;
- explicit URL ingest;
- local query logs;
- remote LLM backends;
- workspace/cloud connectors;
- live database introspection;
- graph database push;
- hosted platform synchronization.

Verify behavior from source, not only privacy prose. Query logs deserve special attention: determine whether they are opt-in, where plaintext is stored, whether corpus paths/questions/responses are included, and which environment variable disables them.

For the first pilot, default to code-only, no outbound network, no hooks/watch, no global graph, no remote push, and no semantic/media modes. Require an explicit later decision for each expansion.

## 6. Architecture ownership

Default classification is `project-specific/optional`, owned by the software-development profile. The parent orchestrator routes work but does not load the graph tool globally. Do not create a separate agent unless durable graph maintenance becomes a distinct operational service with its own queue and lifecycle.

Use the graph for large or unfamiliar repositories, repeated architecture/dependency/impact questions, cross-language tracing, and subsystem navigation. Skip it for exact identifiers, small repositories, single-file defects, runtime behavior, or one-off searches that native text/structural search answers cheaply.

Source files, tests, runtime traces, and project-native analyzers remain authoritative. Critical security, correctness, migration, and impact conclusions must be verified against them.

## 7. Pilot acceptance gate

Before approving the capability, require:

- pinned version and artifact hash;
- installation only in the owning profile/tool environment;
- short wrapper skill with no auto-install, auto-upgrade, hidden project mutations, or mandatory fan-out;
- zero outbound network in code-only mode;
- writes confined to an approved output directory;
- secrets/sensitive paths excluded and artifacts inspected;
- stable canonical hash across two clean builds;
- stable no-change incremental behavior;
- target-OS acceptance;
- a known-answer benchmark (for example, 20 architecture/impact questions) against source truth and a native-search baseline;
- independent review of claimed gains and residual false-negative risk.

Approve only if the graph measurably improves completeness or time without lowering answer correctness. Otherwise keep it off by default or exclude it.

## Pitfalls

- Equating a green graph build with useful retrieval.
- Treating edge provenance as a recall/completeness guarantee.
- Trusting natural-language query quality after testing only exact symbol lookup.
- Accepting self-authored benchmark claims without a local known-answer evaluation.
- Installing the MCP and skill simultaneously before assigning one owner.
- Ignoring prompt footprint because the CLI itself is local.
- Testing only the command advertised in the README when alternate subcommands have different side effects.
- Calling Linux CI proof of Windows compatibility.
- Committing generated graphs before reviewing paths, rationale text, and sensitive content.
