# Minimal Web-Research Tool Stack

Use this reference when curating search, extraction, browser, crawl, document, and citation capabilities for this MCP-backed research profile.

## Default ownership map

Assign one default owner per phase:

1. **Search + clean extraction:** Exa MCP with exactly `web_search_exa` and `web_fetch_exa`.
2. **Interactive or JS-heavy pages:** Playwright MCP only after clean extraction fails or interaction is required.
3. **Local documents:** native file reader first; local PDF text extraction next; OCR only for scanned or empty-text pages.
4. **Provenance:** a local URL/evidence ledger with retrieval timestamps and verbatim quotes; keep citation tracking independent from Exa output.
5. **Monitoring:** `blogwatcher-cli` for feeds and Hermes cron for durable schedules; no RSS MCP.

This profile deliberately uses two non-overlapping MCP servers: Exa for search/fetch and Playwright for interaction. Additional MCP is justified only by a capability absent from those servers and the native file/vision tools.

## Provider selection rule

Choose one search/extract backend based on the project, not popularity alone:

- a combined search/extract provider for general research;
- a semantic/similarity provider for papers or related-page discovery;
- a traditional independent index when source diversity is an explicit requirement;
- a crawler only for site-wide map/crawl jobs.

Do not expose the same provider through both native tools and its MCP server. Treat alternate providers as mutually exclusive backends or bounded cross-checks, not simultaneous defaults.

## Escalation ladder

Use the cheapest, narrowest surface that can complete the step:

1. Search result metadata.
2. Direct page extraction.
3. Alternate URL-to-Markdown reader.
4. Interactive browser.
5. Specialized crawler, cloud browser, proxy, or site-specific scraper.
6. Human login/CAPTCHA intervention.

Record why escalation occurred. Do not use a browser for every URL merely because it is available.

## Security review

For each candidate record:

- transport: local stdio, remote HTTP/Streamable HTTP, or ordinary REST;
- Windows execution path: native binary, `npx`, Python/`uvx`, Docker, or WSL;
- exact credentials and where they are passed;
- whether the vendor receives queries, URLs, page content, documents, browser state, or retained datasets;
- filesystem, browser, network, and private-LAN reach;
- prompt-injection exposure from retrieved content;
- whether server-initiated sampling is supported.

Safe defaults:

- treat every retrieved page and MCP result as untrusted data;
- disable MCP sampling for untrusted external servers;
- use per-server tool allowlists (`tools.include`) rather than exposing broad catalogs;
- block private/LAN targets for cloud tools and guard against redirect-based SSRF;
- use isolated browser profiles without personal sessions;
- never send signed URLs, intranet pages, or sensitive documents to public readers;
- minimize cloud dataset/session retention;
- keep secret redaction enabled and credentials in the agent's secret store.

## Classification guidance

- **Default:** Exa search/fetch MCP, Playwright MCP for interactive pages, native files/vision, local provenance ledger.
- **Optional:** replacement search backend, fallback reader, RSS monitoring, independent second-opinion service.
- **Project-specific:** deep crawler, cloud browser/proxy, documentation index, site-specific actors, self-hosted metasearch, heavy OCR.
- **Exclude by default:** generic Fetch MCP, Filesystem MCP, omnibus multi-search MCP, generic citation MCP, and any MCP that merely republishes native tools.

When a project-specific MCP is retained, expose only its unique tools. Examples: crawl/map but not search/extract; one allowlisted scraper actor rather than an entire marketplace.

## Evidence and dynamic metrics

For official projects, prefer official docs, pricing pages, repositories, and transport/auth READMEs. Keep popularity and quality separate. Timestamp stars, latest commit/push, pricing, and free-tier claims. If the GitHub API is rate-limited, a current shields.io stars JSON badge and the repository's branch Atom feed can provide a reproducible fallback for approximate stars and latest commit time. Label rounded badge counts as approximate.

Pricing pages rendered through a text reader are acceptable only when the source URL remains the vendor's official pricing page. Avoid quoting search snippets as pricing evidence.

## Acceptance checks

Before approving the stack:

- every research phase has one default owner;
- no provider is exposed through both native and MCP interfaces;
- no browser stack has two equal-precedence owners;
- optional servers have a trigger and a disable-by-default policy;
- tool schemas are filtered to unique capabilities;
- source claims include retrieval timestamps and official URLs;
- a smoke test proves search, extraction, browser fallback, PDF handling, and citation verification without leaking a private URL or credential.
