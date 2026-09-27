---
name: evidence-grounded-presentation-delivery
description: "Use when producing research-backed executive presentations."
version: 1.0.0
author: MASTER
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [presentations, research, citations, visual-design, verification]
    category: productivity
---

# Evidence-Grounded Presentation Delivery

Create concise, executive-ready presentations where research quality, visual hierarchy, and artifact verification matter as much as the prose. This skill complements format-specific tooling such as `powerpoint`; it governs evidence, narrative, design production, and verification.

## Core principle

A presentation is complete only when:

- every load-bearing external claim maps to a retrieved source;
- unlike evidence designs are not flattened into one universal number;
- each slide communicates one decision-relevant message;
- the actual visual output has been inspected;
- the generated presentation has been read back and structurally verified;
- editability and rendering limitations are disclosed.

## Procedure

### 1. Define the decision and evidence boundary

Before designing slides, determine:

- the audience and decision the deck must support;
- what outcomes matter: time, quality, throughput, errors, adoption, risk, or ROI;
- which claims require primary research versus official product documentation;
- what is an internal case observation rather than external evidence.

Keep surveys, randomized experiments, field rollouts, official documentation, and internal verified cases visibly distinct.

### 2. Build a citation-led research brief first

Use `grounded-citations` and, for measured effects, `empirical-evidence-synthesis`.

1. Reset a task-specific citation ledger.
2. Register sources when retrieved, not after drafting.
3. Prefer primary papers, institutional pages, and official documentation.
4. Attach verbatim evidence for every headline number.
5. Write a short research brief with inline citation IDs.
6. Include at least one limitation, null result, or boundary condition.
7. Verify the brief before producing slides.

Do not cite a search snippet as though the full study was inspected.

### 3. Design the narrative before decorating

For an executive research deck, a strong default arc is:

1. thesis;
2. why now;
3. operating model or concept;
4. strongest measured evidence;
5. practical workflow map;
6. before/after process;
7. verified internal case;
8. economics and KPIs;
9. boundary condition or failure mode;
10. governance;
11. pilot roadmap;
12. decision and sources.

Choose the slide count from the argument. Do not stretch sparse content to hit a round number.

### 4. Keep text sparse but preserve meaning

- One claim per slide.
- Prefer one headline, one supporting sentence, and 3–6 visual labels.
- Put exact study design and sample size near the metric.
- Use short source IDs in footers and a full source slide at the end.
- Never remove a qualifier that changes the meaning of a number.
- Use recommendations as recommendations, not as research findings.

### 5. Choose the production path deliberately

Use a native editable deck when the user needs to revise individual text, charts, or brand components in PowerPoint.

Use an image-backed deck when pixel-consistent visual fidelity is the dominant requirement and the user did not request native editability:

1. Render each slide as a 1920×1080 PNG.
2. Embed each PNG edge-to-edge on a 16:9 blank slide.
3. Overlay transparent hyperlink shapes on source URLs when clickability matters.
4. Retain the deterministic generator script and slide PNGs.
5. Explicitly disclose that text inside the slide image is not directly editable.

Do not present an image-backed deck as fully editable PowerPoint.

### 6. Verify visuals in two passes

1. Generate a contact sheet of every slide and inspect the whole narrative for rhythm, density, hierarchy, and consistency.
2. Inspect evidence-heavy, source-heavy, and unusually dense slides at full resolution.

Check:

- clipped or overlapping text;
- elements outside card boundaries;
- low-contrast footers;
- tiny URLs and caveats;
- inconsistent terminology or decimal formatting;
- numbers that changed during layout work;
- slides that look good alone but repeat or break the overall story.

A successful file write is not visual verification.

### 7. Verify the final deck structurally

Read the `.pptx` back with the PowerPoint inspection tool and verify:

- slide count;
- 16:9 dimensions;
- image or shape inventory per slide;
- expected hyperlinks;
- title and document metadata;
- no missing embedded media.

Record file size and checksum when reproducibility matters. If no Office/LibreOffice renderer is available and the deck is image-backed, inspect the exact PNGs embedded into the deck and say that Office-engine rendering was not exercised.

### 8. Deliver the artifact, evidence, and limitation

Return:

- the absolute `.pptx` path;
- slide count and content outline;
- research brief path;
- contact sheet path;
- generator/source path;
- verification performed;
- editability or rendering limitations.

## Common failure modes

- Starting in PowerPoint before the argument is coherent.
- Using self-reported adoption data as proof of productivity.
- Mixing task speed, quality, and organization-level ROI into one headline.
- Hiding a negative boundary result because it weakens the sales narrative.
- Citing product marketing for causal productivity effects.
- Building visually polished slides with uncited or rounded numbers.
- Inspecting only a contact sheet; dense slides also need full-resolution review.
- Claiming native editability for slides that are full-slide images.
- Reporting a valid `.pptx` without reading it back.

## References

- `references/evidence-and-visual-verification.md` — compact production and verification checklist.
- `references/image-backed-pptx.md` — pixel-locked PowerPoint pattern with clickable source overlays.
