# Isolated enterprise profile build and acceptance

Use this reference when creating a Hermes profile for a local/self-hosted model and credentialed enterprise APIs. The objective is a genuinely separate runtime with a minimal capability surface, not a clone that silently inherits unrelated keys, skills, or fallback providers.

## Build sequence

1. **Create from blank state.** Use `hermes profile create <name> --no-skills --description "..."`; do not clone another profile when isolation is a requirement. Confirm the new profile path with `hermes -p <name> profile show <name>`.
2. **Configure the self-hosted model as a named custom provider.** Set `providers.<id>.api`, `key_env`, `transport`, `default_model`, and `model.provider=custom:<id>` with `hermes -p <name> config set ...`. Keep the key slot in that profile's `.env`; do not place the value in `config.yaml` or inherit a generic shell key.
3. **Pin conservative model limits.** Set context/output caps from the serving configuration, not only model-family marketing limits. Preserve the exact model ID supplied by the operator.
4. **Minimize toolsets.** Disable cloud media, public search, delegation, or browser surfaces that the role does not own. Retain only tools with a defined operational use. Set secret redaction, PII policy, approvals, and a profile-local working directory explicitly.
5. **Install domain skills by ownership phase.** Prefer one owner for API contract lookup, one for service operations, and one change-control workflow. Pin external skill/toolkit sources to a commit and run their deterministic tests before installation.
6. **Pin MCP dependencies.** Install a fixed package/version into the profile or a controlled vendor directory rather than resolving `latest`/unversioned `npx` on every start. Run the package-manager production audit and retain the lockfile.
7. **Keep service credentials out of MCP config.** Use the profile `.env`, environment interpolation, or a small audited launcher that reads the profile secret file without printing it. A placeholder may be used only when it cannot reach a real service and its purpose is explicit.
8. **Apply runtime tool allowlists.** Upstream discovery count and registered runtime count are different facts. Configure `mcp_servers.<name>.tools.include` to the exact intended tools, disable server sampling for untrusted/community servers, and disable optional prompts/resources unless required.

## Acceptance gates

Record each layer independently:

- `hermes -p <name> config check` exits zero;
- profile show reports the intended model/provider and skill count;
- every selected skill passes structural validation; upstream tests pass when supplied;
- `hermes -p <name> mcp test <server>` proves transport/discovery;
- runtime registration proves the configured allowlist is what the agent sees, not all upstream tools;
- one representative read-only tool call succeeds for every configured MCP;
- launcher invokes the intended profile and returns exit zero;
- package audit has an explicit result;
- the real model call is PASS, or BLOCKED with the precise missing endpoint/key dependency.

Do not turn a mock endpoint into evidence that the real model works. A profile can be accepted as `PASS with expected auth blocker` only when configuration, skills, MCP discovery, runtime allowlists, and representative non-model calls are already verified and the remaining blocker is exactly the operator-supplied credential/service.

## Reporting

Separate:

- installed defaults;
- project-specific optional candidates;
- explicit exclusions and overlap reasons;
- upstream MCP tools vs runtime-selected tools;
- structural checks vs live calls;
- agent inference credential vs target-system credentials.

When the operator says “only insert the API key,” clarify which key: the inference key may be the sole remaining agent-start dependency, while each 1C/CRM/EDI tenant still requires its own scoped credentials when that tenant is connected.
