# Windows Browser Discovery and Acceptance

Use this when Windows says a browser/app is unavailable, desktop automation cannot find it, or a browser appears missing despite prior installation.

## Diagnostic order

1. **Locate known executable paths** and check that the file exists.
2. **Run a deterministic render smoke test** (for Chromium, headless DOM output is suitable).
3. **Inspect App Paths and browser registration** rather than relying only on package-manager inventory.
4. **Inspect URL associations** for `http` and `https`.
5. **Check Start Menu registration/shortcut presence**.
6. **Open a benign URL through the OS association** and verify the process exists.
7. **List desktop applications** and record the canonical automation name and executable path.
8. **Capture using the exact canonical name**.

## Why package-manager inventory is insufficient

A browser can be installed by an enterprise/offline installer and work normally without appearing in a package manager's inventory. Conversely, a stale package entry does not prove the executable or URL association works. Treat the package manager as secondary evidence.

## Canonical-name mismatch

Desktop automation commonly exposes the registered product name (for example, `Google Chrome`) while a human asks for `Chrome`. If capture by shorthand fails:

- list apps;
- match by executable path;
- use the exact returned application name;
- verify with a fresh capture.

This is a discovery issue, not evidence that the browser is absent.

## Safe verification

- Use `about:blank`, a data URL, or a benign public test page.
- Do not interact with personal tabs, login prompts, password dialogs, payments, or extensions.
- Starting the browser is in scope only when the user requested the browser problem to be fixed or verified.
- Reinstall only after the existing executable, render smoke, registration, and OS launch checks show a reproducible defect.

## Reporting

State separately:

- executable installed: yes/no;
- deterministic render: PASS/FAIL;
- OS URL launch: PASS/FAIL;
- canonical desktop app name;
- desktop capture: PASS/FAIL;
- repair performed, or diagnosis-only because no repair was needed.

Do not say “reinstalled/fixed” when the actual result was that the existing installation worked after being launched or addressed by its canonical name.