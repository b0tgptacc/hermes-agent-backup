Figma deployment uses one shared DESIGNER Hermes profile with a dedicated service account permitted by organization policy; DEVELOPER and RESEARCHER do not receive Figma MCP.
§
For the logistics CRM project, the user chose Frappe CRM + ERPNext as the core, with consolidation and customs-broker workflows, required integrations to 1C, banks, EDO, OCR, and BI, and wants the existing landed-cost calculator rewritten as a Frappe app before launch. The full specification is intended to be the authoritative basis for future implementation.
§
For the logistics CRM project, the landed-cost calculator must be a native page inside the Frappe CRM shell, reachable from CRM navigation and visually consistent with existing CRM components; a separate standalone link/page is not an acceptable primary UX.
§
For the logistics sourcing-agent project, the user requires browser-first research across many marketplaces without depending on marketplace APIs, prioritizing domestic Chinese platforms such as 1688. Existing RESEARCHER should be reused unchanged through a bounded evidence/verification bridge, while SOCIALRESEARCHER should be used selectively for Chinese community reviews, complaints, and operational human signals—not as the source of SKU, price, MOQ, or supplier terms.
§
Проект локального ИИ-агента должен использовать Qwen3.8 на двух NVIDIA A100; при проектировании нужно различать 40/80 GB и NVLink/PCIe, выбирать TP=2 для моделей/длинного контекста и независимые реплики для throughput.
§
Профиль Hermes `ruenterprise` использует VPN-only endpoint локальной Qwen3.8-27B: http://10.149.99.26:4000/v1; context_length 262144.
§
For logistics BOM dashboards, the user treats explicit ORD→PRD lists as authoritative; kit counts use unique-PRD aggregation and GCD. Quantity-only completeness includes positions without dates, while dated readiness stays separate with no invented dates. Higher-level kits may treat all ORD as required positions. Logistics planning uses multiple optimized shipment waves, ignores source shipment/terminal/client dates for simulation, and includes a rationale in every shipment object.
§
User wants datasets structured by section and meaning before decisions.