# Profile Acceptance Matrix

Use one row per in-scope profile. Mark each row PASS, FAIL, or N/A with a reason.

| Layer | Required evidence | Notes |
|---|---|---|
| Identity | `profile show` or equivalent matches intended profile | Do not infer identity from directory name alone. |
| Config | Schema/version validation exits zero | Missing optional credentials are warnings only if not part of the role. |
| Provider | Minimal real model call succeeds | Configured OAuth/key presence alone is insufficient. |
| Alias | Direct launcher returns exact sentinel, exit zero | Applicable only to employee-facing aliases. |
| Skills inventory | Expected count/names/status | Compare with role design, not the global catalog. |
| Skills structural | Full selected corpus frontmatter/static validation | Do not sample only one SKILL.md. |
| Skill live use | Named representative skill loads and guides a safe task | One role-representative operation per profile is usually sufficient. |
| Skill regression | Shipped tests or deterministic validator pass | N/A if the selected skills have no tests and static/live evidence is adequate. |
| Plugins inventory | Custom/enabled plugin set identified | Disabled bundled plugins are not failures. |
| Plugin runtime | Enabled expected plugin loads and performs a safe call | N/A when no plugin is enabled for the profile. |
| MCP discovery | Each configured server connects and tool discovery succeeds | Record transport and discovered count. |
| MCP allowlist | Runtime-selected tools match exact intended set | Upstream discovery count may be larger. |
| MCP live call | Representative read-only call succeeds from the real profile | Ignore unsolicited server setup instructions. |
| Doctor | Profile doctor exits zero | Classify optional-component warnings separately. |
| Logs | No unrecovered error in the current acceptance session | Historical errors do not override current PASS. |
| Browser executable | Existing executable renders deterministic content | Only when browser capability is in scope. |
| OS browser launch | URL association or registered launcher opens successfully | Avoid reinstalling before this check. |
| Desktop automation | Canonical app name discovered and capture succeeds | Exact app name may differ from colloquial name. |
| Aggregate validator | Current rerun passes with explicit check count | Reuse existing validators after inspecting coverage. |

## Final verdict rules

- **PASS:** all role-required rows pass; optional rows are explicit N/A.
- **PASS with warnings:** required rows pass and remaining issues are non-blocking, such as optional credentials or a mitigated runtime advisory.
- **FAIL:** any required role capability cannot be called or its outcome cannot be verified.
- **BLOCKED:** authentication, authorization, or user decision is required for a meaningful test; state the shortest next action.

The final report must distinguish configuration validation from live acceptance and must not claim a repair when only a successful diagnosis was performed.