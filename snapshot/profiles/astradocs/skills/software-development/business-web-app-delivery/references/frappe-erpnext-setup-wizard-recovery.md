# Frappe / ERPNext setup-wizard recovery

Use this when login succeeds but the first-run ERPNext wizard fails during preset/default installation.

## Diagnose before changing state

1. Confirm containers and HTTP health separately from setup completion.
2. Read the newest `Error Log` rows, not only proxy logs. The browser often shows only a shortened exception.
3. Inspect the captured wizard payload in the traceback. In particular, distinguish a missing value from an invalid canonical Link value.

Example diagnostic command:

```bash
docker compose exec -T backend \
  bench --site "$SITE_NAME" execute frappe.get_all \
  --kwargs '{"doctype":"Error Log","fields":["name","creation","method","error"],"order_by":"creation desc","limit_page_length":5}'
```

A characteristic failure is ERPNext `install_fixtures.get_preset_records()` calling `country.replace(...)` while `country=None`. This means the wizard reached ERPNext with incomplete System Settings; retrying unchanged will reproduce the failure.

## Canonical-value rule

Frappe Link fields require the stored DocType name, not an assumed label or translated country name. Query before setting:

```bash
docker compose exec -T backend \
  bench --site "$SITE_NAME" execute frappe.get_all \
  --kwargs '{"doctype":"Country","filters":[["name","like","%Rus%"]],"fields":["name","code"],"limit_page_length":20}'
```

For example, a deployment may store `Russian Federation`, not `Russia` or a localized display string. Treat the live `Country` record name as authoritative.

## Recovery sequence

1. Obtain business choices from the user: company name, country, base currency, fiscal-year boundaries. Infer nothing material.
2. Set missing `System Settings` values using canonical records. Do not print credentials.
3. Verify each value with `frappe.db.get_single_value`.
4. Re-submit `frappe.desk.page.setup_wizard.setup_wizard.setup_complete` as an authenticated Administrator session, passing complete arguments. Read credentials from the ignored local environment file; never embed or echo them.
5. The setup pipeline is resumable: completed app stages are recorded and skipped on retry. Still verify the final state rather than assuming the retry completed everything.

Representative settings commands:

```bash
docker compose exec -T backend bench --site "$SITE_NAME" execute \
  frappe.db.set_single_value --args '["System Settings","country","<canonical Country name>"]'
docker compose exec -T backend bench --site "$SITE_NAME" execute \
  frappe.db.set_single_value --args '["System Settings","currency","<currency>"]'
docker compose exec -T backend bench --site "$SITE_NAME" execute \
  frappe.db.set_single_value --args '["System Settings","time_zone","<IANA timezone>"]'
```

## Verification gate

Do not report recovery until all of these pass:

- `frappe.is_setup_complete` returns `true`;
- the expected `Company` exists with correct country and base currency;
- authenticated login returns success;
- authenticated `/desk` and `/crm` return HTTP 200;
- the user can refresh past `/desk/setup-wizard` without retrying the failed wizard.

## Pitfalls

- Healthy Docker services prove availability, not successful ERPNext initialization.
- Nginx/access logs usually show only HTTP 500; use Frappe `Error Log` for the traceback and payload.
- Do not patch ERPNext core merely to tolerate `None`; repair the missing upstream settings/payload.
- A second error such as `Could not find Country: X` is evidence that `X` is not the canonical Link value. Query the DocType and retry with the stored name.
- Preserve partial setup state and use the framework's resumable stages; destructive volume resets are unnecessary for this class of failure.
