# Electricity consumers and connected load by category and state, 31 March 2024

Number of electricity connections and the load they are sanctioned to draw (kW), for each consumer category, in each state.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *All India Electricity Statistics: General Review 2025* (data for 2023-24, published November 2025)
- **Table taken from:** Table 10, "Classification of Consumers and Connected Load Region-wise/State-wise, Utilities, 31.03.2024" (pages 159-161)
- **Link:** https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1001&subSubHeadingId=10084&title=General%20Review&lang=en (listed there as "2024")
- **Downloaded:** 17 Nov 2026 (original in [`_sources/cea-general-review/raw/`](../_sources/cea-general-review/raw/))
- **Script:** [`pipelines/cea-general-review/build_general_review.py`](../pipelines/cea-general-review/build_general_review.py); checks in `check_general_review.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `system` | Row label as printed (state, region, sub-total or total) |
| `date` | Date the figures refer to (as on), YYYY-MM-DD |
| `domestic_load_kw` | Domestic: connected load, kW |
| `domestic_consumers` | Domestic: number of consumers |
| `commercial_load_kw` | Commercial: connected load, kW |
| `commercial_consumers` | Commercial: number of consumers |
| `industrial_lv_mv_load_kw` | Industrial (LV & MV): connected load, kW |
| `industrial_lv_mv_consumers` | Industrial (LV & MV): number of consumers |
| `industrial_hv_load_kw` | Industrial (HV): connected load, kW |
| `industrial_hv_consumers` | Industrial (HV): number of consumers |
| `public_lighting_load_kw` | Public lighting: connected load, kW |
| `public_lighting_consumers` | Public lighting: number of consumers |
| `traction_load_kw` | Traction: connected load, kW |
| `traction_consumers` | Traction: number of consumers |
| `agriculture_load_kw` | Agriculture: connected load, kW |
| `agriculture_consumers` | Agriculture: number of consumers |
| `public_water_works_load_kw` | Public water works: connected load, kW |
| `public_water_works_consumers` | Public water works: number of consumers |
| `miscellaneous_load_kw` | Miscellaneous: connected load, kW |
| `miscellaneous_consumers` | Miscellaneous: number of consumers |
| `total_load_kw` | Total: connected load, kW |
| `total_consumers` | Total: number of consumers |

## Notes

- Each category has two columns in the PDF; reading the numbers (e.g. Delhi: 7.2 million consumers, 23.2 GW load) shows the first is connected load and the second is consumers, so they are named that way.
- On page 161 the J&K label overprints a number ("Lad1a8k2h486" = agriculture load 182486); it is split back.
- CEA note: in some cases the number of consumers and load may have gone down over the previous year due to reconciliation of data by the states.
- The number 933902 printed under the table (total connected load in MW) is not in the CSV.
- Checks: 41 rows; the three pages have the same rows in the same order; region sub-totals and All India recomputed in all 20 columns: one 2 kW difference.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
