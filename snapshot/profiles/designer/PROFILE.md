# DESIGNER Profile

Purpose: a dedicated employee-facing specialist for creating and editing Figma Design pages and Figma Slides, using authorized PDFs and common office files as source material.

## Why this is a separate profile

DESIGNER is intentionally separate from DEVELOPER and RESEARCHER:

- Figma OAuth is a per-user external identity and `use_figma` can modify shared design files.
- Slide/page creation is a creative production workflow, not software implementation or evidence-first web research.
- Keeping Figma in one profile avoids giving production-code and research workers a broad canvas-mutation tool.
- The separate profile has its own minimal skills, exact MCP allowlist, approval policy, and audit boundary.

MASTER/Hermes Kanban remains the only cross-profile orchestrator. DESIGNER does not call DEVELOPER or RESEARCHER directly.

## Runtime

- Model: `gpt-5.6-sol` via existing `openai-codex` OAuth
- Reasoning: high
- Maximum turns: 200
- Approvals: smart
- Secret redaction: enabled
- Native delegation and cross-profile orchestration: unavailable in the CLI tool surface
- Enabled native tools: clarification, code execution, files, skills, terminal/processes, todo, vision
- Local code/file/terminal operations execute as UID 10001 in the immutable image ID recorded by `runtime/image-manifest.json` (human alias `hermes-designer-docs:20260818`), with Docker networking disabled, a per-session container, no environment forwarding, and only `C:/Users/admin/designer-workspace` mounted at `/workspace`. Profile strict mode disables Hermes automatic skills/cache/media/attachment/credential mounts. MASTER stages authorized inputs there and removes them after the task's retention review; arbitrary `--in` paths are not mounted.
- The former profile-local Windows virtualenv remains a maintenance/test artifact; it is not the agent security boundary and is not used by the configured tool backend.
- Disabled by default: native web/browser, computer control, memory writes, cron, messaging, media generation, Git/PR-specific surfaces

## Figma MCP

Official remote endpoint:

`https://mcp.figma.com/mcp`

Authentication: Figma OAuth to one centrally managed dedicated Figma account. Administrator OAuth completed successfully. `whoami` confirmed the approved masked identity, but the account currently has only a `View` seat; live mutations remain blocked until a Full seat and least-privilege edit access are confirmed.

Exact configured tools for full creative production (11):

1. `whoami`
2. `create_new_file`
3. `use_figma`
4. `get_screenshot`
5. `get_metadata`
6. `get_design_context`
7. `get_variable_defs`
8. `get_libraries`
9. `search_design_system`
10. `download_assets`
11. `upload_assets`

Mutation tools are exposed because high-quality Design/Slides production requires real canvas creation, iterative layout, typography, imagery, components, and asset placement. Governance is enforced around the creative work rather than by disabling it: the approved dispatcher requires requester/task/target fields, writes a hash-chained audit ledger, and holds a conservative global lock for the entire task. Destructive deletion/overwrite remains separately approval-gated and every mutation batch requires structural and screenshot verification.

Excluded: Code Connect mutation/suggestion tools, shaders, Weave paid-credit tools, FigJam diagram generation, live-UI capture, and every future tool not explicitly allowlisted. MCP prompts, resources, and sampling are disabled.

`use_figma` is necessarily broad: it can create, edit, delete, or inspect Figma Design, FigJam, and Slides objects through the Plugin API. `SOUL.md` therefore requires explicit targets, inspect-before-write, no deletion by default, per-batch verification, and explicit authorization for uploads or cross-file transfer.

## Curated skills

Figma (official upstream repository):

- `figma-create-new-file`
- `figma-use`
- `figma-use-slides`
- `figma-generate-design`

Documents (Hermes productivity skills):

- `ocr-and-documents`
- `pdf`
- `docx`
- `powerpoint`
- `xlsx`

No broad research, coding-process, GitHub, monitoring, or browser skills are installed.

## Employee routing

Employees must not invoke raw `hermes --profile designer` or complete OAuth directly. They submit the brief, exact workspace, and target through MASTER/the approved dispatcher. The supported launcher is `C:/Users/admin/.local/bin/designer.bat`, which requires requester, task ID, and target and serializes all Figma jobs.

Examples:

```text
Read C:/Work/brief.pdf, create a new Figma Slides deck named "Q4 Review",
use our brand file <Figma URL> as the visual reference, and show me the plan
before writing to Figma.
```

```text
Using <exact Figma Design URL>, add a new page for a product landing page.
Preserve existing pages, reuse the linked design-system components, and verify
the result with a screenshot.
```

```text
Read C:/Work/source.docx and C:/Work/data.xlsx. Summarize the content and
propose a 10-slide narrative. Do not create or edit Figma until I approve the
outline.
```

## First-time OAuth (administrator only; intentionally deferred)

Run:

```bash
hermes --profile designer mcp login figma
```

An administrator signs in to the approved dedicated Figma account and completes the official browser authorization. Restart the DESIGNER session after successful login, then verify:

```bash
hermes --profile designer mcp test figma
```

Figma currently allows only catalog-listed MCP clients. Hermes uses its curated Figma catalog compatibility setting for the OAuth client name. This is a compatibility dependency and should be revalidated after Hermes or Figma MCP changes.

## Seat and rate-limit constraints

- Canvas writes require a Full seat and edit permission to the target file.
- Dev seats support read-only design context.
- View/Collab and Starter plans have materially lower read-tool limits.
- Write-to-canvas is beta, currently free during beta, and expected to become usage-based paid functionality.
- Custom fonts and some image workflows remain limited; generated output requires human review.

## Health checks

```bash
hermes --profile designer config check
hermes --profile designer doctor
hermes --profile designer prompt-size
hermes --profile designer mcp test figma
```

The MCP health test requires completed Figma OAuth. Config/document checks do not.
