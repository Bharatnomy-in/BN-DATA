# Royalty, DMF and taxes paid on coal by state, 2024-25

Money paid by coal companies in each coal-producing state: royalty to the state, District Mineral Foundation (DMF) and National Mineral Exploration Trust (NMET) contributions, GST, cess, income tax and dividends, in Rs crore.

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 6, sheet "tb7.2&3", Table 7.2 "State Wise Payment of Royalty, DMF, NMET and other Taxes during 2024-25 (Coal)"
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `year` | Financial year (April to March) as printed |
| `royalty_inr_crore` | Royalty paid, Rs crore |
| `dmf_inr_crore` | DMF paid, Rs crore |
| `nmet_inr_crore` | NMET paid, Rs crore |
| `cgst_inr_crore` | Central GST, Rs crore |
| `sgst_inr_crore` | State GST, Rs crore |
| `igst_inr_crore` | IGST, Rs crore |
| `cess_on_coal_inr_crore` | Cess on coal, Rs crore |
| `entry_tax_inr_crore` | Entry tax on coal, Rs crore |
| `corporate_income_tax_inr_crore` | Corporate income tax, Rs crore |
| `dividend_inr_crore` | Dividend, Rs crore |
| `total_inr_crore` | Total, Rs crore |
| `state_as_printed` | State name as printed in the source |

## Notes

- The share column is left out. The short state codes printed in the first column are left out (they are swapped for Maharashtra and Madhya Pradesh in the source).
- DMF here is what companies paid in; how much DMF money was spent is not in the Coal Directory.
- Checks: states add up to All India in every column; items add up to the total.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
