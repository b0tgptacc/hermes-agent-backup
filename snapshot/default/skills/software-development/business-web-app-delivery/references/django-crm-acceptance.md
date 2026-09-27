# Django CRM Acceptance Patterns

Concrete checks for a Django-style transactional business application. Adapt names and fields; preserve the invariants.

## Financial state machine

Recommended invoice policy:

- `ISSUED`, `PARTIAL`, `PAID`, `OVERDUE` are computed.
- `CANCELED` is an explicit terminal/manual state.
- Status refresh returns immediately for `CANCELED`.
- Canceled invoices reject new payments.
- Existing payments remain auditable but canceled invoices and their payments are excluded from active billing totals.
- `is_overdue` excludes `PAID` and `CANCELED`.
- Lowering `Invoice.amount` below existing payments fails validation and the transactional update.

Tests must cover web form, direct `save()`, manager/service creation, Django admin, payment edit, payment delete, and concurrent writes.

## Payment integrity

Use three layers:

1. `CheckConstraint(amount__gt=0)` for row-local positivity.
2. `transaction.atomic()` plus `select_for_update()` on the invoice for cross-row balance checks.
3. One canonical save/service path that recalculates invoice status after create/edit/delete.

A model `clean()` alone is insufficient because `save()`, admin customization, managers, bulk operations, and raw SQL have different behavior. State exactly which surfaces the application guarantees.

## Protected history

Typical relationship policy:

- `Project.client = PROTECT`
- `Contract.project = PROTECT`
- `Invoice.contract = PROTECT`
- `Payment.invoice = PROTECT`

Catch `ProtectedError` in delete views. Show a user-facing refusal and keep the graph intact. Test assigned-user deletion when `responsible` or `assignee` uses `PROTECT`.

## Safe seed command

- New demo users only receive a password supplied through an explicit CLI flag or environment variable.
- Without a supplied password, call `set_unusable_password()` or print a generated one-time value once.
- Existing users retain their password hashes.
- `DEBUG=false` refuses the command unless `--allow-production` is present.
- README never publishes reusable credentials.

## Production settings gate

Local defaults may support HTTP development. With `DEBUG=false`:

- reject a missing or known-placeholder `DJANGO_SECRET_KEY` using `ImproperlyConfigured`;
- require explicit `ALLOWED_HOSTS`;
- support environment-driven `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_HSTS_SECONDS`, subdomain/preload flags, and proxy SSL header;
- make Compose require app/database secrets instead of supplying working fallbacks.

Release probe:

```text
DEBUG=false
DJANGO_SECRET_KEY=<temporary strong verification value>
SECURE_SSL_REDIRECT=true
SESSION_COOKIE_SECURE=true
CSRF_COOKIE_SECURE=true
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=true
SECURE_HSTS_PRELOAD=true
python manage.py check --deploy
```

Never print real secrets in verification output.

## Responsive navigation probe

Document width alone misses clipped links. A Playwright check should authenticate, set a 390px viewport, then for every `nav a`:

```javascript
const box = await link.boundingBox();
if (!box || box.x < 0 || box.x + box.width > viewportWidth) {
  throw new Error(`clipped nav link: ${await link.innerText()}`);
}
```

A robust small-screen rule lets navigation take a full flex row and wrap:

```css
@media (max-width: 720px) {
  .topbar nav {
    order: 3;
    flex: 0 0 100%;
    width: 100%;
    flex-wrap: wrap;
    overflow: visible;
  }
}
```

First run the bounding-box probe and preserve the failing output; then patch CSS and rerun it.

## Docker credential consistency without disclosure

When tool output redacts credentials as `***`, parse raw configuration inside a local script, compare the dependent values, and print only booleans such as:

```text
compose_defaults_match: true
env_values_match: true
```

Do not infer a mismatch from redacted display text.

## Review prompts that find real bugs

Ask the reviewer explicitly about:

- canceled-state preservation and aggregates;
- lowering a limit after dependent records exist;
- direct ORM/admin bypasses;
- payment create/edit/delete symmetry;
- PostgreSQL concurrency rather than SQLite-only tests;
- `CASCADE` across auditable records;
- `ProtectedError` user experience;
- seed password reset behavior;
- production fail-open defaults;
- fresh-volume Docker startup;
- mobile navigation bounding boxes.
