---
name: production-product-ui-redesign
description: "Use when redesigning operational web apps to senior UI."
version: 1.0.0
author: MASTER
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [ui, ux, redesign, dashboard, crm, operational-software, motion, responsive, accessibility, visual-qa]
    category: creative
---

# Production Product UI Redesign

Redesign an existing operational web application—CRM, ERP, admin console,
back-office tool, dashboard, or workflow system—to a senior product-design
standard without weakening its behavior, permissions, data integrity, or
operability.

This skill is for production implementation in an existing repository, not a
standalone marketing mockup. It complements protected general design skills by
focusing on operational software, functional preservation, browser evidence,
and independent visual review.

## Trigger

Use when any of these is true:

- The user calls the interface dated, generic, unfriendly, basic CRUD, or
  visually poor.
- A functional dashboard needs premium product quality, coherent navigation,
  refined controls, purposeful motion, and responsive behavior.
- The product must feel comparable in craft—not copied in identity—to mature
  tools such as Attio, Stripe, Linear, Airtable, or Superhuman.
- A visual redesign must ship in the existing stack and survive automated and
  browser verification.

## Core Standard

A redesign is complete only when:

1. The composition matches the screen's job.
2. The full product—not only the dashboard—uses one coherent design system.
3. Important actions are obvious, fast, and accessible.
4. Motion clarifies state rather than decorating it.
5. Desktop and mobile are visually inspected in a real browser.
6. Existing behavior, authorization, validation, and routes still pass.
7. A fresh reviewer finds no blocking visual or UX defect.

A stylesheet refresh alone is not a redesign.

## 1. Inspect Before Asking

Read the actual repository before choosing a visual direction:

- base/app shell templates;
- dashboard, list, form, detail, login, empty and error states;
- CSS tokens and component rules;
- JavaScript interaction code;
- route names and authorization conditions;
- screenshots at primary desktop and mobile widths.

Identify whether the dominant surface is:

- **Monitor** — glanceable state and exceptions;
- **Operate** — lists, queues, records, and actions;
- **Command/Inspect** — drilling into one entity;
- **Configure** — forms and settings.

Operational products usually combine Monitor + Operate. Never redesign them as
marketing pages with a hero and equal-weight feature cards.

## 2. Clarify Taste Efficiently

For high-fidelity work, ask one compact batch covering only decisions that
materially change implementation:

- visual posture: premium light, dark precision, warm friendly, or variants;
- navigation: permanent sidebar, collapsible sidebar, top navigation, or
  responsive hybrid;
- accent family;
- density: compact, balanced, airy, or user-adjustable.

Recommend the strongest default first. Do not ask the user to choose token-level
values.

If the user has already supplied references, feel, and primary action, proceed.

## 3. Commit to a Product Composition

Before colors, commit to the shell and hierarchy.

For a typical CRM:

- persistent desktop sidebar for stable information architecture;
- top action bar for page context and primary action;
- dashboard ordered by decisions: health → money → exceptions → next actions;
- list views optimized for scanning and row action clarity;
- detail pages with back/context, status, primary action, and grouped facts;
- forms with clear labels, errors, save/cancel hierarchy, and progressive
  grouping;
- mobile drawer or bottom navigation with every route discoverable.

Do not rely on horizontal navigation scrolling as the only mobile affordance.
All navigation items must be visibly reachable.

## 4. Define a Small Design System

Use explicit tokens for:

- canvas, surfaces, elevated surfaces;
- primary, secondary, muted and disabled text;
- hairline and strong borders;
- accent, hover and pressed states;
- success, warning, danger and informational states;
- radius hierarchy;
- spacing rhythm;
- type scale and numeric treatment;
- elevation/shadow levels;
- motion durations and easing.

### Premium-light posture

A reliable premium-light baseline:

- cool or warm near-white canvas, white elevated surfaces;
- deep navy/ink instead of pure black;
- restrained blue-violet accent;
- tabular numerals for financial data;
- one or two blue-gray shadow layers, used sparingly;
- controls around 10–12px radius, panels around 16–18px;
- strong hierarchy through type and spacing, not a box around everything.

Transform reference principles into an original system. Do not clone proprietary
layouts, branded assets, or copy.

## 5. Redesign Every Core Surface

### App shell

- Group navigation by user intent.
- Use consistent inline SVG icons only where they improve scanning.
- Derive active state from the real route.
- Place identity, role, and logout predictably.
- Give mobile navigation a visible toggle, overlay, Escape close, correct
  `aria-expanded`, and 44px targets.

### Dashboard

- Show only real metrics already provided by application context.
- Prioritize exceptions and next actions over decorative numbers.
- Use hierarchy, alignment and subtle state color—not six identical icon cards.
- Avoid fake charts and invented trends.

### Lists and tables

- Strong object title plus secondary metadata.
- Clear status pills with dot + text.
- Refined header, row hover, focus and action states.
- On mobile, use intentional horizontal handling or a semantic card fallback;
  never silently clip columns or actions.

### Forms

- Labels remain visible; placeholders do not replace labels.
- Show field errors adjacent to the field and a useful error summary when
  needed.
- Use responsive grouping and a clear save/cancel footer.
- Preserve CSRF, method, route, form field names, validation, and authorization.

### Detail screens

- Back/context link, object name, status, primary action.
- Definition-grid or sections based on information hierarchy.
- Related records only when the backend already supplies them.
- Dangerous actions are visually distinct but not dominant.

### Empty, error, success and login states

- Empty states explain what is absent and offer the relevant action.
- Messages/toasts have semantic appearance and remain readable without motion.
- Login feels part of the same product; avoid fake claims, stock imagery, and
  decorative marketing sections.

## 6. Motion Discipline

Good default durations:

- control hover/press: 120–180ms;
- surface entrance: 180–280ms;
- drawer/modal: 220–320ms.

Use motion for:

- drawer continuity;
- button tactility;
- row/action feedback;
- message/toast entrance and dismissal;
- subtle page/surface reveal.

Avoid looping ambient animation, long stagger chains, bounce, and animation that
delays work.

Always include `prefers-reduced-motion: reduce` that removes nonessential
animation and smooth scrolling.

## 7. Preserve Functionality with Tests

Before editing production templates, add structural or route tests that can fail
for the intended shell behavior, such as:

- authenticated base renders sidebar, topbar, mobile toggle, and every route;
- active navigation marker is tied to the current route;
- JavaScript and CSS assets are referenced;
- login remains accessible;
- core list/form/detail routes render for both roles;
- CSRF and delete-role boundaries remain intact.

Then run targeted RED → implementation → GREEN. Do not rewrite business logic as
part of a visual task.

Run the full existing suite after template and static changes.

## 8. Real-Browser Verification

Automated route tests cannot prove design quality. Verify with a real headless or
isolated browser.

Minimum evidence:

- login;
- dashboard at approximately 1440×1000;
- dashboard at approximately 390×844;
- one list/table;
- one create/edit form;
- one detail screen;
- admin/manager navigation differences if relevant.

For each viewport check:

- horizontal page overflow;
- clipped navigation, text, controls, rows, and actions;
- all expected navigation links within the viewport or accessible drawer;
- focus visibility and touch-target size;
- broken icons/assets;
- browser console errors;
- empty/error/success state legibility.

A successful pattern for authenticated local QA is documented in
`references/operational-ui-browser-audit.md`.

## 9. Slop Diagnostic

Score before and after, 0–10. Count:

1. generic tech gradient;
2. arbitrary indigo with no brand rationale;
3. equal-weight feature tiles;
4. decorative accent rails;
5. unearned glass/blur;
6. monument stats used as filler;
7. icon toppers everywhere;
8. center-stacked composition;
9. default typography with no numeric/hierarchy treatment;
10. wrong surface archetype.

Do not finish with any composition tell (3, 8, or 10). Aim for ≤2/10 overall.

## 10. Independent Design Review

Use a fresh reviewer after implementation. Give it screenshots and the brief,
not the implementer's rationale. Fail closed on:

- clipped or unreachable controls;
- inconsistent shell/surface language;
- poor contrast or invisible focus;
- mobile navigation failure;
- broken motion/reduced-motion behavior;
- misleading visual hierarchy;
- obvious generic CRUD or AI-template composition.

Suggestions such as a custom icon set or non-root container hardening are
nonblocking unless required by the brief.

## Pitfalls

- **Polishing one screen only.** A beautiful dashboard beside raw generic forms
  makes the product feel less coherent, not more.
- **CSS-only cosmetic patch.** If the shell and information hierarchy are
  unchanged, the user will still perceive dated CRUD software.
- **Animation as quality.** More transitions do not compensate for weak layout.
- **Reference cloning.** Borrow posture and principles, not proprietary identity.
- **Hidden mobile overflow.** `overflow-x:auto` without a visible affordance can
  make routes functionally undiscoverable.
- **Changing backend behavior during redesign.** Preserve routes, names,
  validation, permissions and financial semantics.
- **Trusting self-report.** Inspect screenshots and execute browser flows.

## Verification Checklist

- [ ] Visual direction and density were confirmed or responsibly assumed.
- [ ] Surface archetype and shell were committed before tokens.
- [ ] Dashboard, list, form, detail, login and states are coherent.
- [ ] Purposeful motion and reduced-motion behavior exist.
- [ ] Structural/route tests passed.
- [ ] Full application tests passed.
- [ ] Desktop and mobile screenshots were inspected.
- [ ] No clipped/unreachable navigation or horizontal page overflow.
- [ ] Slop score ≤2 with no composition tells.
- [ ] Independent design review passed.
- [ ] Final response includes paths, verification, caveats and next decision.

## References

- `references/operational-ui-browser-audit.md` — authenticated desktop/mobile
  visual QA workflow and reliable checks for clipping and route coverage.
- `references/service-crm-premium-light.md` — session-derived example brief for a
  premium-light Monitor + Operate CRM redesign.
