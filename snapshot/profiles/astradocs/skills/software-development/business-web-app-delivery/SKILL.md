---
name: business-web-app-delivery
description: "Use when building transactional internal web apps."
version: 1.0.0
author: MASTER
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web-apps, crm, erp, transactional, django, delivery, verification]
    category: software-development
---

# Business Web Application Delivery

Build and verify transactional internal applications such as CRMs, ERPs, service portals, billing tools, and operations dashboards. This skill owns the gap between “CRUD pages work” and “the business system preserves money, permissions, history, and production safety.”

Compose rather than duplicate:

- `test-driven-development` for RED → GREEN → REFACTOR.
- `requesting-code-review` for an independent fail-closed review.
- `dogfood` for exploratory web QA.
- a relevant design skill for the visual system.

## Core principle

A green happy-path test suite is not sufficient. Delivery is complete only after all mutation surfaces, state transitions, database invariants, deployment defaults, desktop UI, and mobile UI have been exercised.

## Procedure

### 1. Define the business invariants before choosing pages

For each entity, write down:

- authoritative state and legal transitions;
- ownership and role permissions;
- which values are computed versus manually editable;
- whether deletion is allowed, protected, soft-deleted, or audited;
- cross-row invariants such as `payments <= invoice amount`;
- treatment of canceled, archived, refunded, or reversed records;
- concurrency behavior and required database locks.

Treat these as acceptance criteria, not implementation notes.

### 2. Choose the smallest maintainable architecture

For internal CRUD-heavy systems, prefer a proven server-rendered monolith unless an SPA is justified by real interaction complexity. Require:

- migrations and a relational database path;
- built-in CSRF/session protections;
- explicit roles;
- reproducible local and container startup;
- environment-driven production settings;
- no external integration in an MVP unless it changes the core outcome.

Complexity must earn its place.

### 3. Implement vertical TDD slices

Build one end-to-end behavior at a time:

1. Write the failing test.
2. Run it and confirm the expected RED.
3. Implement the smallest production path.
4. Run the specific test and full suite.
5. Refactor only while green.

Include tests for model validation, web forms, direct ORM writes, admin mutations, role boundaries, state transitions, aggregates, and deletion behavior. A web-only test does not prove the model or admin path is safe.

### 4. Centralize transactional writes

For financial or quota-like data:

- use database constraints for row-local invariants;
- use one service/manager path with `transaction.atomic()` and row locking for cross-row invariants;
- make model/admin/direct-ORM behavior consistent with that path;
- recalculate derived state after create, edit, and delete;
- test lowering a parent limit below already-consumed value;
- test canceled records and existing child records;
- add real PostgreSQL concurrency tests when `select_for_update()` matters.

Document explicitly if `bulk_create`, raw SQL, or external writers are outside the guarantee.

### 5. Make lifecycle and deletion policy explicit

Never let default `CASCADE` decide whether financial history disappears. For every relationship choose deliberately:

- `PROTECT` for invoices, payments, contracts, and auditable history;
- controlled cascade only for non-auditable dependent data;
- soft deletion when business restoration or audit is required.

Catch `ProtectedError` in user-facing delete flows and explain why deletion was refused. Confirm what administrators can do through both the custom UI and framework admin.

### 6. Treat framework admin as a separate mutation surface

Audit admin create/edit/delete independently. Framework permissions alone may not enforce the product’s role model. Verify:

- role-aware delete permission;
- password validation;
- computed fields are not manually persisted inconsistently;
- transactional service methods are used;
- post-delete totals/statuses are refreshed;
- managers cannot gain destructive access via `is_staff` plus model permissions.

### 7. Seed safely

A seed command must be idempotent without resetting real users.

- Never store known reusable passwords in source or README.
- Accept demo credentials from explicit CLI flags or environment variables.
- Set unusable passwords or generate one-time values when credentials are omitted.
- Never overwrite an existing password hash unless explicitly requested.
- Refuse to run with production settings unless the operator supplies a dedicated confirmation flag.

### 8. Fail closed in production

Development conveniences may default locally, but `DEBUG=false` must not start with:

- a known/default secret key;
- wildcard or absent hosts;
- working default database credentials;
- missing secure-cookie and HTTPS policy where TLS terminates in the app/proxy.

Expose production security settings through environment variables. Run `manage.py check --deploy` (or the framework equivalent) with production-like values as a release gate. Local HTTP defaults and production TLS policy should be distinct and documented.

### 9. Verify containers from a clean state

Do not rely on an old volume or hidden `.env`.

1. Validate Compose configuration.
2. Compare dependent credential fields programmatically without printing secret values.
3. Tear down test volumes.
4. Build from source.
5. Start with explicit temporary secrets.
6. Wait for database and web health.
7. Run migrations and smoke tests inside the real stack.
8. Verify login and authenticated routes.

A redacted tool display (`***`) is not proof that two stored values differ; compare inside a script and print only a boolean.

### 10. Run real browser checks at desktop and mobile widths

HTTP 200 is not visual verification. Use a real browser to:

- authenticate and visit every primary route;
- capture login, dashboard, representative lists/forms/details;
- assert no page-level horizontal overflow;
- assert each navigation link’s bounding box lies within the viewport;
- inspect responsive tables, cards, forms, empty states, and errors.

A navigation bar with `overflow-x:auto` can still make key sections effectively invisible. Verify every link, not just document width.

### 11. Independent fail-closed review

The implementer does not approve its own work. Give the reviewer the repository plus acceptance criteria and require checks for:

- secrets and production defaults;
- auth, CSRF, roles, and admin bypasses;
- financial/state invariants on every write surface;
- cancellation/refund/archive semantics;
- delete cascades and audit history;
- concurrency and stale derived state;
- Docker fresh-volume reproducibility;
- missing negative tests.

Any security concern or logic error fails the gate. Use a fresh fixer context, then re-run all checks and a second independent review.

## Required release evidence

Before reporting “done,” retain real output for:

- full automated test suite;
- migration drift check;
- framework system and production-security checks;
- static collection/build;
- Docker build and healthy services from a clean volume;
- unauthenticated redirect and authenticated route smoke tests;
- desktop and mobile browser evidence;
- independent reviewer verdict;
- exact remaining limitations.

## Common failure modes

- Testing only the custom web form while direct ORM/admin bypasses invariants.
- Allowing `CANCELED` to be overwritten by an automatic status refresh.
- Including canceled records in outstanding, overdue, or revenue totals.
- Letting a parent amount fall below already-recorded child payments.
- Assuming `select_for_update()` was validated on SQLite.
- Deleting a client and silently cascading through contracts, invoices, and payments.
- Seed commands that reset passwords on every run.
- Calling predictable Docker defaults “development only” without a production fail-closed path.
- Declaring responsive success because `scrollWidth == clientWidth` while nav links are clipped.
- Trusting a generated implementation report without re-running the commands.

## Reference

See `references/django-crm-acceptance.md` for concrete Django patterns and deterministic verification probes derived from a service-CRM build.
