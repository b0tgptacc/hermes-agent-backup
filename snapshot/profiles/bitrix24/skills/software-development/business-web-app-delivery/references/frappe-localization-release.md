# Frappe CRM localization release workflow

Use this when a Frappe/ERPNext/CRM app must be genuinely localized, not merely configured with a language code.

## Separate four localization layers

1. **Request/user locale:** set System Settings and target users explicitly. A translated catalog is bypassed when the active request language remains unset.
2. **Gettext catalog:** audit the exact vendored app/version rather than assuming upstream coverage.
3. **Dynamic/static UI:** find source strings absent from the catalog and raw Vue/HTML text that bypasses `__()`.
4. **Business display defaults:** language does not determine country, timezone, or currency. Synchronize CRM display currency from completed business defaults, never from a regional language guess.

## Catalog procedure

1. Parse the existing PO and report total, empty non-header, fuzzy, and source-identical counts.
2. Extract message IDs from the current source/POT and merge missing IDs before translation.
3. Translate all empty entries while preserving every placeholder multiset (`{0}`, `{name}`, `%s`, `%(name)s`), HTML tag structure, product names, enum semantics, and literal examples.
4. Validate UTF-8 bytes directly. On Windows, avoid Unicode text flowing through a shell pipe unless output encoding is forced to UTF-8; a successful command can otherwise replace Cyrillic with runs of `?`.
5. Reject the release if any non-header `msgstr` is empty, any entry is fuzzy, placeholders/tags differ, `�` exists, or a translated `msgstr` contains corruption runs such as `???`.
6. Compile with the framework command, e.g. `bench compile-po-to-mo --app <app> --locale ru --force`, then clear the site cache.

## Dynamic UI and runtime verification

- Search Vue/JS/Python source for current message IDs missing from the PO.
- Search static text nodes and user-facing attributes (`title`, `label`, `alt`, empty-state text) that bypass translation helpers.
- For third-party onboarding/help components with hardcoded English, wrap or replace them with app-owned localized components rather than editing transient `node_modules` output.
- Rebuild frontend assets from the vendored source and copy/use the generated asset directory consumed by the serving container. A backend-only catalog compile does not update SPA bundles.
- Use an authenticated browser in the real request locale. Assert required Russian labels and a forbidden list of known English leftovers.
- Verify dynamic charts, sidebar, onboarding/help, currency symbol, desktop/mobile overflow, and console/error state—not only the login page.
- Compare source/image/running-container hashes for representative catalog, frontend, and backend files before declaring a clean release.

## Release evidence

Retain:

- catalog audit counts;
- placeholder/HTML/Unicode validation;
- successful PO→MO compilation;
- frontend production build output;
- runtime language and business currency reads;
- authenticated desktop/mobile screenshots and DOM assertions;
- clean rebuild/recreate health and source-to-container parity.

## Pitfalls

- Treating `System Settings.language=ru` as proof that the CRM SPA is translated.
- Translating a stale PO without merging IDs from the exact current source.
- Trusting shell-rendered Cyrillic instead of reading the UTF-8 file bytes.
- Fixing only visible navigation while charts, onboarding, help, attributes, and empty states remain English.
- Inferring RUB/Russia/timezone from Russian UI language.
- Compiling MO successfully but serving stale frontend assets or a stale image.
