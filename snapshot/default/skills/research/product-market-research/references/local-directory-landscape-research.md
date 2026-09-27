# Local directory landscape research

Use this workflow for markets where ordinary search engines expose little local B2B information but a city directory such as 2GIS has server-rendered listings.

## Validated workflow

1. Query the directory by multiple intent classes, not just the target service:
   - direct competitors (`фулфилмент`);
   - demand pools (`интернет-магазины`, marketplace sellers);
   - acquisition partners (`обучение маркетплейсам`, photo studios);
   - compliance partners (`сертификация товаров`, `маркировка товаров`);
   - upstream logistics (`карго Китай`);
   - downstream delivery (`курьерские услуги`, postal services).
2. Fetch the public search-result HTML with a normal browser user agent. 2GIS result pages can contain server-rendered business cards even when search engines or interactive browser automation are unavailable.
3. Parse each `/city/firm/<id>` card into at least:
   - business name;
   - canonical directory URL;
   - category and address;
   - visible positioning text;
   - ratings/review counts only as discovery signals, never as proof of service quality.
4. Follow selected firm pages to collect public website, Instagram, Telegram, or WhatsApp links. Do not infer ownership if the page does not expose it.
5. Build separate outputs for competitors, seller communities/training hubs, marketplaces, upstream logistics, compliance/content partners, and last-mile channels.
6. Treat map-directory counts as a dated visibility snapshot, not a registry or market-share estimate. Cite the exact query URLs and state that listings, ratings, and branch counts are dynamic.
7. Turn the landscape into actions: named lead pools, partnership offers, channel-specific messages, and a short test plan with conversion milestones.

## Extraction pattern

For large HTML pages, avoid letting a shell/tool truncate the response before parsing. Stream the full response directly into a small parser:

```bash
curl -L -s -A 'Mozilla/5.0' '<directory-search-url>' | python parse_directory.py
```

The parser should consume stdin, split on firm-card anchors, strip HTML, and emit JSON. Keep the parser generic enough to adapt if CSS class names change; firm URL patterns are often more stable than generated classes.

## Grounding rules

- Quote only visible claims from cards or firm pages; label ad copy as operator positioning, not independently verified capability.
- Do not repeat dynamic prices unless the user explicitly needs them and retrieval date/variant are recorded.
- Distinguish observation from inference: for example, repeated emphasis on cross-border marketplace delivery supports a positioning hypothesis, not a complete demand estimate.
- Validate major marketplace presence with official seller portals or physical infrastructure listings where possible.
