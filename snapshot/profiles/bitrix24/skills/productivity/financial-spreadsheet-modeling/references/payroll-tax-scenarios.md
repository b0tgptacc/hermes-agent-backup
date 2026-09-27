# Payroll and Tax Scenario Workbook

Use this reference for payroll-style templates where the user requests multiple taxes or scenario rates. It is a modeling pattern, not jurisdiction-specific tax advice.

## Recommended Columns

1. Sequential row number
2. Employee/reference ID
3. Employee name
4. Department
5. Position
6. Employment/contract type
7. Worked days or units
8. Gross/accrued amount before scenario tax
9. Scenario indirect tax amount
10. Amount including scenario indirect tax
11. Personal-income-tax base
12. Personal income tax withheld
13. Net payable to worker
14. Total scenario cost
15. Payment/review status
16. Notes

Keep the indirect-tax amount, personal-income-tax base, withheld tax, net payment, and total cost separate even if some values coincide in a simplified model.

## Formula Pattern

Assume the input amount is in `H7`, indirect tax rate in `Настройки!$B$4`, and income-tax rate in `Настройки!$B$5`:

```excel
I7 = IF(H7="","",ROUND(H7*'Настройки'!$B$4,2))
J7 = IF(H7="","",ROUND(H7+I7,2))
K7 = IF(H7="","",H7)
L7 = IF(K7="","",ROUND(K7*'Настройки'!$B$5,2))
M7 = IF(H7="","",ROUND(H7-L7,2))
N7 = IF(J7="","",J7)
```

These formulas describe a transparent scenario in which personal income tax applies to the amount excluding the indirect tax. If the jurisdiction or contract uses a different base, change the settings/methodology and formulas rather than relabelling the same calculation.

## Handling Unusual Tax Requests

Payroll for employees is often outside the scope of VAT or other indirect taxes. When a user explicitly requests an indirect-tax rate:

- include it as a clearly labelled scenario column;
- do not refuse an otherwise useful template;
- add a visible methodology note that applicability must be confirmed;
- avoid claiming statutory correctness without jurisdiction, date, worker classification, thresholds, deductions, and current authoritative sources;
- keep the rate editable on the settings sheet.

## Professional Template Features

- Requested number of neutral employee IDs; leave names blank.
- Summary sheet with headcount, gross amount, scenario indirect tax, amount including tax, income tax, net payable, and total cost.
- Settings sheet with rates, period, organization, responsible person, and methodology warning.
- Validation lists for department, status, and employment type.
- Conditional formatting for paid/review/held statuses.
- Comments on gross amount, scenario tax, and net payment headers.
- Native table, freeze panes, print titles, page numbering, and wide-table print scaling.

## Deterministic Verification Example

For a base amount of `100000.00`, an indirect-tax rate of `22%`, and an income-tax rate of `13%` under the formula pattern above:

- indirect tax: `22000.00`;
- amount including indirect tax: `122000.00`;
- income tax: `13000.00`;
- net payable: `87000.00`.

Compute this independently with decimal arithmetic; do not treat it as proof that the chosen tax treatment is legally applicable.

## Workbook Checks

- Rates are numeric `0.22` and `0.13`, not text.
- Data range contains exactly the requested employee rows.
- First and final rows use the same formula pattern.
- Summary formulas end on the final requested row.
- Workbook recalculation-on-open flags are set.
- XLSX ZIP archive passes integrity testing.
- No invented personal or payroll data is present in the template.
