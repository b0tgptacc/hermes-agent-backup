# Fail-Closed Visual Acceptance for Operational Web Apps

Use this matrix after an implementation worker reports the redesign complete and before announcing acceptance.

## Mobile evidence matrix

At the primary mobile viewport, capture and inspect every core surface, not only the dashboard:

- dashboard and open navigation;
- representative list/table with long values and row actions;
- create/edit form, including validation errors;
- detail page with missing optional data;
- login;
- empty, success, and destructive confirmation states when material.

Wait for drawer/modal transitions to settle before measuring element bounds. Record page overflow separately from deliberately open off-canvas navigation.

## Deterministic blocking checks

- All mobile interactive controls are at least 44×44 CSS px, including icon, close, logout, navigation, and row-action targets.
- Meaningful small text meets WCAG AA contrast (normally 4.5:1). Low-contrast tokens are decorative only.
- Conditional actions reflect real data: hide or disable mail/call/download actions when their target is absent.
- A persistent topbar CTA is contextual or suppressed when the page already has a local primary action.
- `prefers-reduced-motion` disables nonessential transitions without hiding state.
- No horizontal page overflow, clipped controls, unreachable navigation, browser errors, or hidden primary actions.

## Composition and AI-slop gate

Fail when the interface relies on equal-weight KPI tiles, decorative gradient/blur/glass layers, accent rails, or abstract login art without task value. Operational exceptions and next actions should dominate decorative metrics. Require an overall slop score of 2/10 or lower.

## Scope-aware verdict

A functional/security baseline may remain accepted while the redesign fails visual acceptance. Report these scopes separately. A later fail-closed visual review supersedes the implementer's completion claim for the redesign only.
