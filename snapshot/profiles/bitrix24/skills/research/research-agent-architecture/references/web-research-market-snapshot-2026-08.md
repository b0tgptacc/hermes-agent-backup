# Web Research Market Snapshot — 2026-08-18

Historical research snapshot supporting `research-agent-architecture`. Re-check all metrics, pricing, activity, audits, package versions, and provider contracts before a future implementation. Installs, npm downloads, and GitHub stars measure adoption, not quality.

Checked around 2026-08-18 07:35–07:40 UTC.

## Skill adoption snapshot

| Skill | Adoption observed | Durable interpretation |
|---|---:|---|
| `vercel-labs/agent-browser/agent-browser` | 692,331 skills.sh installs; ~40.8K repo stars | Highly popular browser executor, but overlaps native Hermes browser and Playwright. Optional backend, not workflow owner. |
| `mattpocock/skills/research` | 320,506 installs; ~220K repo stars | Best compact generic workflow template found. Adapt its primary-source and delegation patterns to Hermes instead of installing it unchanged. |
| `anthropics/skills/pdf` | 180,494 installs; ~170K repo stars | Broad PDF toolkit; overlaps native reading and OCR. A Snyk failure was visible at snapshot time and required investigation before use. |
| Firecrawl `firecrawl-deep-research` | 32,791 installs | Vendor-specific exhaustive report workflow. Use as an alternative execution mode only. |
| `sfkislev/the-news` | 17,146 installs | Useful lead discovery, but aggregators are not final evidence. |
| Tavily `tavily-research` | 15,927 installs | Duplicates a native Tavily backend plus local orchestration. |
| Parallel `parallel-deep-research` | 13,217 installs | Expensive exhaustive alternative; not a concurrent default. |
| GitHub `doublecheck` | 4,154 installs | Valuable adversarial high-stakes verification pattern; integrate as an optional verifier gate. |
| `blogwatcher` | 3,296 via search API and about 4.5K on detail page | Index counters disagreed. Treat as RSS/Atom discovery, not evidence or synthesis. |
| DeepMind `literature-search-arxiv` | 2,237 installs | Academic discovery; choose it or another arXiv workflow as the owner. |
| DeepMind `literature-search-openalex` | 2,056 installs | Complements arXiv with a broader literature graph. |
| Hermes `ocr-and-documents` | 332 installs | Official specialized ingestion owner; low adoption was not a quality signal. |
| Hermes `grounded-citations` | 36 installs | Official local provenance/citation core; new at snapshot time. |
| Hermes `competitor-news-monitor` | 14 installs | Specialized policy for company watchlists and materiality. |
| Hermes `blocked-page-recovery` | 7 installs | New official recovery skill; browser is its last expensive fallback. |

Key skill sources:

- https://skills.sh/mattpocock/skills/research
- https://skills.sh/nousresearch/hermes-agent/grounded-citations
- https://skills.sh/nousresearch/hermes-agent/blocked-page-recovery
- https://skills.sh/nousresearch/hermes-agent/ocr-and-documents
- https://skills.sh/nousresearch/hermes-agent/competitor-news-monitor
- https://skills.sh/github/awesome-copilot/doublecheck
- https://skills.sh/firecrawl/firecrawl-workflows/firecrawl-deep-research
- https://skills.sh/tavily-ai/skills/tavily-research
- https://skills.sh/parallel-web/parallel-agent-skills/parallel-deep-research
- https://skills.sh/vercel-labs/agent-browser/agent-browser
- https://skills.sh/anthropics/skills/pdf
- https://skills.sh/google-deepmind/science-skills/literature-search-arxiv
- https://skills.sh/google-deepmind/science-skills/literature-search-openalex
- https://skills.sh/openclaw/openclaw/blogwatcher

## MCP and tool adoption snapshot

NPM weekly downloads covered 2026-08-09 through 2026-08-15.

| Tool | Adoption observed | Recommendation at snapshot time |
|---|---:|---|
| Microsoft Playwright MCP | 4,819,822 npm/week; ~36K stars | Project-specific browser owner. Do not run beside native browser without precedence. |
| Firecrawl MCP | 167,934 npm/week; 7,261 stars | Strong crawl/map fallback. Prefer native Hermes provider integration. |
| Tavily MCP | 24,471 npm/week; 2,333 stars | Recommended initial single provider through native Hermes web tools, not MCP. |
| Exa MCP | 18,221 npm/week; 4,881 stars | Alternative for semantic, similarity, and paper discovery. |
| Brave Search MCP | 15,795 npm/week; 1,388 stars | Alternative independent index; requires separate extraction. |
| Apify MCP | 14,351 npm/week; 4,040 stars | One allowlisted Actor only. Full dynamic Store is too broad. |
| Browserbase MCP | 1,401 npm/week; ~3.4K stars | Hermes already had a native Browserbase path; MCP added overlap. |
| Crawl4AI | ~79K stars | Self-hosted privacy alternative to Firecrawl; operationally heavy. |
| SearXNG | ~36K stars | Self-hosted search-only option requiring a separate extractor. |
| Reference MCP servers repo | ~90K stars | Fetch server duplicated Hermes extraction and was excluded. |
| Context7 | ~61K stars | Useful for versioned library documentation, not generic web research. |
| Perplexity MCP | 2,447 stars | Second opinion only; avoid citation laundering through model synthesis. |

NPM evidence endpoints used:

- https://api.npmjs.org/downloads/point/last-week/firecrawl-mcp
- https://api.npmjs.org/downloads/point/last-week/tavily-mcp
- https://api.npmjs.org/downloads/point/last-week/exa-mcp-server
- https://api.npmjs.org/downloads/point/last-week/%40playwright%2Fmcp
- https://api.npmjs.org/downloads/point/last-week/%40apify%2Factors-mcp-server
- https://api.npmjs.org/downloads/point/last-week/%40browserbasehq%2Fmcp-server-browserbase
- https://api.npmjs.org/downloads/point/last-week/%40modelcontextprotocol%2Fserver-brave-search

Official repositories:

- https://github.com/firecrawl/firecrawl-mcp-server
- https://github.com/tavily-ai/tavily-mcp
- https://github.com/exa-labs/exa-mcp-server
- https://github.com/microsoft/playwright-mcp
- https://github.com/apify/apify-mcp-server
- https://github.com/browserbase/mcp-server-browserbase
- https://github.com/unclecode/crawl4ai
- https://github.com/searxng/searxng
- https://github.com/modelcontextprotocol/servers
- https://github.com/perplexityai/modelcontextprotocol

## Hermes-specific findings

Hermes v0.20.0 documentation described native `web_search` and `web_extract` backends for Firecrawl, SearXNG, Parallel, Tavily, and Exa. It supported distinct `search_backend` and `extract_backend`, so provider MCP servers were usually redundant.

Useful references at snapshot time:

- https://hermes-agent.nousresearch.com/docs/reference/tools-reference
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration
- https://hermes-agent.nousresearch.com/docs/user-guide/features/web-search
- https://hermes-agent.nousresearch.com/docs/user-guide/features/browser
- https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp

Firecrawl's README exposed a read-only search profile at `https://mcp.firecrawl.dev/v2/mcp-search`. It was considered only when native web integration was unavailable; using both would duplicate the search surface.

Tavily was recommended as the initial single native backend because it combined search and extraction with low setup complexity. This was explicitly a starting hypothesis. The production decision must come from a representative Tavily-versus-Exa-versus-Firecrawl benchmark.

## Durable conclusions from the snapshot

1. Keep a separate research profile instead of adding browser/search surfaces to a developer profile.
2. Create one Hermes-native orchestration skill rather than install several generic deep-research skills.
3. Use local grounded citations as the only ledger even when a provider returns its own citations.
4. Start with no default MCP; add one only for a measured capability gap.
5. Treat provider-specific research skills as mutually exclusive execution backends.
6. Browser, PDF/OCR, monitoring, academic, product-market, and citation skills need narrow triggers and phase owners.
7. Keep popularity, recommendation, and installed/tested state in separate report columns.
8. Use a persistent Hermes session for leaf fan-out; one-shot mode should be able to execute sequentially.
9. Use scheduled durable jobs for monitoring, not background delegation tied to a live chat process.
10. Preserve market/news/academic timestamps and source-family independence in the evidence model.
