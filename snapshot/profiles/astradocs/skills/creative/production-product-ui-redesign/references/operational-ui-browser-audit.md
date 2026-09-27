# Operational UI Browser Audit

Use this after route/unit tests pass. It verifies what tests cannot: visual hierarchy,
clipping, discoverability, responsive behavior, and motion safety.

## Preconditions

- Use an isolated/headless browser, never the user's signed-in profile.
- The app runs locally with seeded non-sensitive demo data.
- Pass login credentials only through ephemeral environment variables; never
  write or print them.
- Capture console errors and HTTP failures.

## Required viewports and surfaces

Capture at minimum:

1. Login — desktop.
2. Dashboard — 1440×1000.
3. Dashboard — 390×844.
4. One list/table — desktop and mobile.
5. One form — desktop and mobile.
6. One detail screen.

## Deterministic checks

For every page:

- response status is 200 after authentication;
- `document.documentElement.scrollWidth <= clientWidth + 1`, unless a named,
  intentionally scrollable table container owns the overflow;
- every navigation link is either within the viewport or reachable in the open
  mobile drawer;
- no icon-only control lacks an accessible name;
- no expected primary action is hidden or clipped;
- no browser console error appears;
- focus states are visible under keyboard navigation.

For mobile navigation, assert each item has a non-null bounding box inside the
open drawer. A page-level no-overflow check alone is insufficient: clipped
children inside `overflow:hidden/auto` can still be unreachable while the page
reports no overflow.

## Authenticated Playwright pattern

Use a tiny temporary script outside the repository or under ignored artifacts.
Launch an installed Chrome channel when possible:

```js
const { chromium } = require('playwright');
const browser = await chromium.launch({ channel: 'chrome', headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
await page.goto(process.env.BASE_URL + '/login/');
await page.fill('input[name="username"]', process.env.UI_USER);
await page.fill('input[name="password"]', process.env.UI_PASSWORD);
await Promise.all([
  page.waitForURL(process.env.BASE_URL + '/'),
  page.click('button[type="submit"]'),
]);
```

Then visit every required route, save screenshots, and inspect them directly.
Do not treat status 200 as visual success.

## Mobile clipping assertion

```js
const links = page.locator('nav a');
for (let i = 0; i < await links.count(); i++) {
  const box = await links.nth(i).boundingBox();
  if (!box || box.x < 0 || box.x + box.width > viewportWidth) {
    throw new Error(`Clipped navigation item: ${await links.nth(i).innerText()}`);
  }
}
```

For drawer navigation, run this after opening the drawer and scope the locator
to the drawer.

## Visual review rubric

Fail closed on:

- unreachable navigation or actions;
- horizontal clipping without affordance;
- raw browser-default forms beside polished pages;
- inconsistent status/button systems;
- unreadable contrast or focus;
- mobile content hidden behind fixed chrome;
- motion without a reduced-motion fallback;
- dashboard composition that reads as a marketing hero or generic feature grid.

## Evidence to retain

Keep before/after screenshots in an ignored `artifacts/` directory. Record:
viewport, route, role, HTTP status, overflow result, console errors, and reviewer
verdict. Never retain session cookies or credentials.
