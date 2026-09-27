# Premium-Light Service CRM Example Brief

This is a session-derived reference, not a universal brand specification. Use it
as a concrete example of translating a vague request for a "modern senior CRM"
into a testable production brief.

## Confirmed choices

- Feel: premium light, friendly but precise; Attio/Stripe posture without
  cloning.
- Navigation: permanent left sidebar on desktop plus top action bar; accessible
  slide-in drawer on mobile.
- Accent: restrained blue-violet.
- Density: balanced for managers and executives.
- Surface: Monitor + Operate.

## Composition

### Sidebar

- Approximately 240–260px desktop width.
- Brand and workspace context at top.
- Intent-grouped routes with simple line icons.
- Active route uses a quiet tinted surface and strong label, not a large filled
  capsule.
- User identity, role, and logout at bottom.

### Top action bar

- Mobile menu toggle.
- Breadcrumb or page context.
- Contextual primary action, never a generic global CTA that does nothing.
- Compact user/avatar context where useful.

### Dashboard

Order information by decision value:

1. page title and current operating context;
2. active clients/projects;
3. contracted, invoiced, paid and outstanding money;
4. overdue invoices;
5. upcoming tasks.

Use only backend-provided data. Do not invent trends, percentages, charts, or
activity feeds.

### Operational surfaces

- Lists: premium table hierarchy, row hover/focus, status dot + text, action
  clarity, mobile fallback/intentional scroll.
- Details: back link, object/status/action header, grouped fields, related
  records only if available.
- Forms: visible labels, two-column responsive groups, adjacent errors,
  save/cancel hierarchy.
- Login: focused premium composition with subtle CSS atmosphere, no fake
  marketing claims.

## Token posture

Suggested families, adjusted to the product:

- canvas: cool near-white;
- surface: white;
- ink: deep navy;
- muted: slate;
- border: cool hairline;
- accent: indigo/violet around `#635bff`;
- success/warning/danger: semantic and restrained;
- control radius: 10–12px;
- panel radius: 16–18px;
- numbers: tabular figures;
- shadow: blue-gray ambient layer plus small close shadow.

Do not turn the whole screen into a violet gradient. Accent color is for active
navigation, focus, primary actions, and selected states.

## Motion posture

- button/row feedback: 120–180ms;
- surface entrance: 180–260ms;
- mobile drawer: 220–300ms;
- messages may enter/dismiss, but remain usable without animation;
- no looping ambient animation;
- full `prefers-reduced-motion` override.

## Acceptance evidence

- Structural tests for app shell/assets/routes fail before the redesign and pass
  after.
- Full application suite remains green.
- Screenshots inspected at 1440×1000 and 390×844 for dashboard, list, form,
  detail, and login.
- Every mobile navigation item is reachable; no page-level overflow.
- Slop score ≤2/10, with no feature-grid, center-stack, or wrong-surface tell.
- Fresh design reviewer passes the result.

## User correction encoded

A functional CRUD interface is not an acceptable stopping point when the user
asks for senior design. Do not claim "premium" based on rounded cards, one
accent color, and a fade-in. Re-compose the product and validate the whole
experience.
