---
name: product-market-research
description: "Use when comparing products or curating agent skills/tools."
version: 1.1.0
author: MASTER
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, shopping, vendors, pricing, comparison, procurement, xlsx, agent-skills, mcp, capability-curation, tool-selection]
    category: research
---

# Product Market Research

Research a concrete product across manufacturers, marketplaces, distributors, and B2B suppliers. Produce a decision-ready comparison that separates technical fit from purchase confidence and preserves a traceable source chain.

## When to Use

- Compare sellers, current prices, variants, delivery terms, and risks.
- Research demand, ICPs, offers, and acquisition channels for operational B2B services in under-documented markets; use `references/service-market-gtm.md`.
- Identify an ambiguously named marketplace product from its specifications.
- Evaluate exact offers and close substitutes for procurement.
- Deliver a brief recommendation plus a detailed spreadsheet/report with charts.
- Curate an AI-agent capability set across skills, MCP servers, coding CLIs,
  built-in tools, worker roles, and dependencies without creating overlaps.
- Select import categories for cross-border marketplace sales while separating
  macro trade volume, consumer demand, regulation, and SKU economics; load
  `references/cross-border-marketplace-category-research.md`.

For agent capability ecosystems, load `references/agent-capability-curation.md`.
It defines popularity-vs-quality evidence, overlap ownership, execution-surface
probes, dependency tiers, and acceptance tests. For web-research agent stacks,
also load `references/web-research-tool-stack.md`; it defines native-vs-MCP
ownership, safe escalation, provider privacy review, and duplicate-exclusion
rules. For recurring threshold alerts, use `product-price-monitor` after this
workflow establishes a verified baseline.

## Core Principles

1. **Pin the exact item before comparing prices.** Convert the title into hard requirements: sensor/model, interface, resolution, frame rate at that resolution, shutter type, stream formats/codecs, lens/FOV, focus type, trigger, enclosure, and quantity.
2. **Separate sensor capability from finished-module capability.** A sensor supporting full-resolution 120 fps does not prove that a USB/UVC module exposes that mode. ISP, bridge, firmware, bandwidth, and codec can lower the delivered mode.
3. **Treat marketplace titles as claims, not specifications.** Prefer a mode table, UVC descriptor, datasheet, or vendor-supplied sample over title text.
4. **Score technical fit and procurement confidence separately.** The closest title match can be a riskier purchase than a slightly weaker but well-documented industrial product.
5. **Normalize price honestly.** Retain source currency, timestamp, selected variant, MOQ, shipping/tax status, and destination assumptions. Never present a base listing price as an all-in landed price.
6. **Keep unknowns unknown.** Use `unknown`/`not confirmed`; do not silently infer seller identity, stock, codecs, field of view, or delivery.

## Procedure

### 1. Build the target specification

Create a requirement table with three levels:

- **Must-have:** failure makes the offer unsuitable.
- **Preferred:** affects ranking but not eligibility.
- **Context:** quantity, destination, OS, SDK constraints, return needs.

Disambiguate terms such as `120 fps`: require the paired resolution and output format. Disambiguate FOV as horizontal, vertical, or diagonal.

### 2. Identify the product family

Search distinctive combinations of attributes. Confirm likely sensor/model against an authoritative manufacturer page or datasheet. Record both:

- raw sensor capabilities;
- finished camera/module output modes.

When these conflict, the finished module's published mode table governs procurement.

### 3. Collect offers using a source hierarchy

Use this order where possible:

1. Sensor manufacturer or official datasheet.
2. Camera/module manufacturer product page and documentation.
3. Authorized distributor or industrial supplier.
4. Marketplace search result and exact item page.
5. B2B marketplace supplier page and audit credentials.

For blocked or dynamic pages, use the proven recovery patterns in `references/marketplace-retrieval.md`. Register URLs in the citation ledger at retrieval time when `grounded-citations` is available.

For each offer collect:

- seller and platform (or explicitly `seller not exposed`);
- item ID/SKU and exact variant;
- title and URL;
- current price, currency, MOQ, shipping/tax status;
- availability and visible sales/review signals;
- resolution/fps pairs;
- interface, shutter, formats/codecs, FOV/focus;
- documentation quality and contradictions;
- retrieval timestamp and source ID.

### 4. Evaluate each offer

Maintain at least these dimensions on a 0–100 scale:

- Technical fit.
- Documentation/evidence quality.
- Seller reliability.
- Price/value.
- Purchase convenience.

A useful default weighting is 40/20/15/15/10. Show the weights and formulas. Do not let a high overall score hide failure of a must-have; add a separate eligibility or mismatch column.

Recommended outputs by scenario:

- **Best exact match.**
- **Lowest procurement risk.**
- **Best value/bulk option.**
- **Closest documented substitute.**

### 5. Reconcile contradictions

Explicitly compare title claims with specifications. Common contradictions:

- sensor says full-resolution 120 fps, module says Full HD 60 fps;
- `100°` is diagonal in one listing and horizontal in another;
- `H.264` appears in the title but not the UVC mode table;
- one price belongs to a different lens/enclosure variant;
- `$0.00` on a manufacturer page means request a quote, not free product.

Flag the contradiction and lower confidence rather than selecting the more favorable claim.

### 6. Produce the deliverables

Brief chat summary:

- likely product identity;
- best exact offer and current price;
- best low-risk alternative;
- decisive technical caveat;
- concrete pre-purchase verification request;
- inline citations and source list.

Detailed workbook/report:

- Executive summary.
- Full offers table.
- Requirements/match matrix.
- Scoring methodology.
- Sources and evidence notes.
- At least two useful charts: price comparison and technical-fit/overall-score comparison.

Use hyperlinks and source IDs in the detailed table. State that marketplace prices are dynamic and whether shipping, duties, and taxes are excluded.

### 7. Verify before delivery

- Recount offers and sources programmatically.
- Confirm prices map to the correct variant and item ID.
- Confirm every external claim has a source ID.
- Validate workbook archive, expected sheets, tables, charts, and hyperlinks.
- Re-open the artifact and inspect key cells/formulas.
- If spreadsheet rendering is available, render and visually inspect; otherwise disclose structural verification only.

## Pre-Purchase Evidence Request

For high-frame-rate USB cameras, ask the seller for:

- `v4l2-ctl --list-formats-ext` or USB Device Tree Viewer output;
- proof of the exact resolution/fps/codec combination;
- a short original sample plus MediaInfo/ffprobe output;
- sensor, ISP/USB bridge, firmware, and lens model;
- FOV split into H/V/D;
- OS/UVC/SDK/trigger support;
- return terms if the promised mode is absent.

## Pitfalls

- Ranking only by price.
- Calling different lens or enclosure variants identical.
- Using review stars without sales count or seller identity.
- Treating marketplace search snippets as full product documentation.
- Converting to local currency without rate date/source.
- Claiming delivery to a destination that was not checked.
- Averaging a price range without preserving the original range and MOQ.
- Presenting a high overall score as proof that every must-have is met.

## References

- `references/marketplace-retrieval.md` — resilient retrieval and extraction patterns for dynamic/blocked shopping pages.
- `references/service-market-gtm.md` — evidence-first segmentation, offer design, lead channels, and sparse-web retrieval for operational B2B services.
- `references/local-directory-landscape-research.md` — multi-intent 2GIS research, streamed HTML extraction, evidence caveats, and conversion of directory listings into competitor, lead-pool, and partner maps.
- `references/ar0234-usb-camera-case.md` — worked case showing sensor-vs-module contradictions and offer scoring.
- `references/agent-capability-curation.md` — evidence model, overlap ownership, dependency tiers, architecture, and acceptance tests for skills/tools/MCP curation.
- `references/web-research-tool-stack.md` — minimal native-first web-research stack, escalation ladder, provider privacy review, and MCP duplicate-exclusion rules.