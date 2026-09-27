# Retail Store Unit Economics

Use this pattern for quick viability checks of neighborhood retail stores before building a full workbook.

## Model contract

Label every number as one of:
- user-provided fact;
- sourced market benchmark;
- illustrative assumption;
- calculated output.

Do not present a generic scenario as an actual forecast. Ask for city, floor area, rent, payroll, opening hours, expected footfall, conversion, average check, gross margin, tax regime, and opening budget when a decision-grade result is required.

## Core equations

- Monthly revenue = daily visitors × conversion × average check × trading days.
- Gross profit = revenue × gross margin.
- Variable operating cost = revenue × variable-cost rate.
- Operating profit = gross profit − variable operating cost − fixed costs.
- Operating margin = operating profit ÷ revenue.
- Break-even revenue = fixed costs ÷ (gross margin − variable-cost rate).
- Required daily transactions = break-even revenue ÷ trading days ÷ average check.
- Required daily visitors = required daily transactions ÷ conversion.
- Simple payback months = startup investment ÷ positive monthly operating profit.

Calculate all arithmetic with a tool and retain enough precision to avoid rounding drift.

## Scenario structure

Show at least three scenarios:
1. downside: weak traffic and conversion;
2. base: plausible operating case;
3. strong location: high traffic and conversion.

Keep rent, payroll, utilities, marketing, admin, and owner compensation explicit. Separate inventory purchase from expense: cost of goods flows through sales, while opening stock is part of startup cash needs. Include deposits, fit-out, equipment, signage, POS, launch marketing, initial inventory, and working-capital reserve in startup investment.

## Interpretation

Lead with the decision threshold, not only the profit table:
- break-even monthly revenue;
- transactions and visitors required per day;
- downside cash burn;
- base and strong-case operating margin;
- simple payback;
- sensitivity to rent, gross margin, and traffic.

State whether debt service, owner salary, depreciation, inventory obsolescence, VAT, and seasonality are included. A seemingly profitable store may still be unattractive if base-case payback is long or the required traffic is not evidenced.

## Product and compliance overlay

For regulated categories, add a separate pre-opening gate for certification, labeling/marking, product safety, intellectual property, returns, warranty, and recalls. Do not let a healthy spreadsheet override a missing legal route to sale.

## Verification checklist

- Recompute one scenario independently.
- Confirm contribution margin is positive before calculating break-even.
- Confirm scenario assumptions are internally consistent.
- Check that startup inventory is not double-counted as a monthly fixed expense.
- Flag placeholder tax rates rather than presenting them as statutory advice.
- Explain that location footfall must be measured in person at relevant hours and days before signing a lease.
