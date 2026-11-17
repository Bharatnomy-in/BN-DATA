# Coal imports by port, 2024-25

Coking coal, non-coking coal and coke imported through each port, airport and inland container depot, with quantity (million tonnes) and value (Rs million and US$ million).

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 7, sheet "TB8.5", Table 8.5 "Port Wise Import of Coal, Coke & Other Coal Products to India during 2024-25"
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `port` | Port / customs point as printed; `Total` = all ports |
| `year` | Financial year (April to March) as printed |
| `coking_coal_mt` | Coking coal, million tonnes |
| `coking_coal_inr_million` | Coking coal, value, Rs million |
| `coking_coal_usd_million` | Coking coal, value, US$ million |
| `non_coking_coal_mt` | Non-coking coal, million tonnes |
| `non_coking_coal_inr_million` | Non-coking coal, value, Rs million |
| `non_coking_coal_usd_million` | Non-coking coal, value, US$ million |
| `total_coal_mt` | Total coal, million tonnes |
| `total_coal_inr_million` | Total coal, value, Rs million |
| `total_coal_usd_million` | Total coal, value, US$ million |
| `coke_coal_products_mt` | Coke & coal products, million tonnes |
| `coke_coal_products_inr_million` | Coke & coal products, value, Rs million |
| `coke_coal_products_usd_million` | Coke & coal products, value, US$ million |

## Notes

- `state_ut` is `All India` because ports are not assigned to states in the source.
- Very small quantities are written in full decimals (0.000000228).
- Blank cells are blank in the source (no import of that kind).
- **Nagpur:** "Concor Icd/Mmlp Khapri Nagpur" is an inland container depot row.
- Checks: ports add up to the Total in every column.
