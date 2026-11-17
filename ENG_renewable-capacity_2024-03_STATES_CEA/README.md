# Installed renewable power capacity by state, 31 March 2024

Grid-connected renewable capacity in each state, by source (small hydro, wind, bio-power, waste-to-energy, solar), in megawatts. Large hydro is not included.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *All India Electricity Statistics: General Review 2025* (data for 2023-24, published November 2025)
- **Table taken from:** Table 3.11, "State-wise Installed Capacity of Renewable Power as on 31.03.2024" (page 66; CEA gives MNRE as the source)
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
| `small_hydro_mw` | Small hydro (up to 25 MW per plant), MW |
| `wind_mw` | Wind, MW |
| `bio_power_bagasse_cogen_mw` | Biomass power / bagasse cogeneration, MW |
| `bio_power_non_bagasse_cogen_mw` | Biomass cogeneration (non-bagasse), MW |
| `waste_to_energy_mw` | Waste to energy, MW |
| `waste_to_energy_offgrid_mw` | Waste to energy (off-grid), MW |
| `bio_power_total_mw` | Total bio-power, MW |
| `solar_mw` | Solar, MW |
| `total_re_mw` | Total renewable capacity, MW |

## Notes

- Blank cells are blank in the source (no capacity of that type is printed); the source has no symbol for them.
- `Others` (blank `state_ut`) is a row in the source. Dadra & Nagar Haveli and Daman & Diu are printed separately here.
- Checks: 39 rows; the printed Total (MW) equals the sum of the states in every column.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
