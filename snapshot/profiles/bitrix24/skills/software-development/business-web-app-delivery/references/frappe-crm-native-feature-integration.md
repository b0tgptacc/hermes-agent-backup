# Native feature integration in a Frappe CRM SPA

Use this reference when moving a standalone Frappe web page into the Frappe CRM Vue SPA while preserving financial/API controls.

## Integration shape

1. Add a lazy Vue route under CRM's existing `createWebHistory('/crm')` router.
2. Add the destination to the existing sidebar model; do not use an iframe or a link that leaves the CRM shell.
3. Reuse CRM's `LayoutHeader`, Frappe UI buttons, surface/outline/ink tokens, responsive sidebar and mobile action patterns.
4. Keep the server API authoritative. Client-side navigation gating is UX, not authorization.
5. Expose the current session user and roles in CRM boot data when the SPA does not already provide them.
6. Apply the same role predicate to both sidebar visibility and direct-route guarding. The allowed frontend roles must match the page's first automatic API call, not a broader read/export role.

## Vue event-boundary pitfall

Vue passes the click event to a method used as `@click="method"`. This is dangerous when the method also accepts optional business arguments:

```js
async function calculate(inputs = payload(), version = formVersion.value) { ... }
```

A click can then serialize `MouseEvent` fields (for example `_vts`) as the API input. The request fails while the old result remains visible.

Use a zero-argument UI boundary and a separate internal function:

```js
async function runCalculation(inputs, version) { ... }
async function calculate() {
  return runCalculation(payload(), formVersion.value)
}
```

Bind explicitly where useful: `@click="() => calculate()"`.

## Reactive form versioning

Use a monotonically increasing form generation to prevent stale calculation/save responses from re-enabling an old revision or PDF:

```js
watch(form, () => {
  formVersion.value += 1
  revisionId.value = ''
}, { deep: true, flush: 'sync' })
```

`flush: 'sync'` matters: with the default asynchronous watcher, a user can edit a field and immediately click Calculate; the calculation captures the old generation and incorrectly discards the legitimate response.

For calculate/save:

- capture an immutable payload and generation at request start;
- compare generation after every awaited response;
- discard stale responses;
- never restore `revisionId` if the form changed;
- keep PDF disabled until the current form is saved.

## Applying templates

After parsing a saved template:

1. Reject malformed JSON and non-object roots with a controlled UI status.
2. Prefer copying an explicit allowlist of expected fields; the server must still validate the payload.
3. Apply values to the reactive form.
4. `await nextTick()` before recalculation, or otherwise guarantee the form-generation watcher has completed.
5. Recalculate automatically and show an explicit success/error status.

Without the tick/generation coordination, the template fields may visibly load while the result is discarded as stale.

## Required browser regression

A route/static test is insufficient. Run a real authenticated Chromium regression that asserts exact behavior:

- click the actual CRM sidebar link and verify the route;
- change quantity and click Calculate without saving; assert the complete expected total changes;
- use both header and responsive action entry points where practical;
- load a saved template, assert exact restored fields and exact recalculated total;
- exercise percentage duty/markup and EUR-per-kg/margin modes;
- submit invalid quantity and blank template name; assert controlled errors and disabled PDF;
- mutate input while save is in flight; assert no revision is exposed and PDF stays disabled;
- save a revision and verify private PDF export through a separate API/browser smoke;
- assert no horizontal document overflow at desktop and mobile widths.

Keep deterministic API/domain tests for formulas in addition to browser tests.

## Reproducible release checks

- Run the actual Docker production frontend build; local source-string checks do not prove Vue/Vite compilation.
- Recreate backend/frontend from the final image.
- Compile the CRM PO catalog during reproducible startup when runtime translations depend on it.
- Compare SHA-256 for critical source files between repository and running container.
- Run full unit, HTTP authorization, calculator/PDF, concurrency and browser suites before an independent fail-closed review.
