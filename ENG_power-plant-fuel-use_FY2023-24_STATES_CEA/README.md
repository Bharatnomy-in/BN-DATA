# Fuel burned in thermal power stations by state, 2023-24

Coal, lignite, oil, gas and biomass consumed by utility thermal power stations in each state, and the electricity these coal/lignite plants generated.

## Source

- **Data:** Central Electricity Authority (CEA), Ministry of Power, *All India Electricity Statistics: General Review 2025* (data for 2023-24, published November 2025)
- **Table taken from:** Table 7.1, "Consumption of Fossil Fuels for Electricity Generation in Thermal Power Stations State-wise by Kind of Fuels, 2023-24" (page 116)
- **Link:** https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1001&subSubHeadingId=10084&title=General%20Review&lang=en (listed there as "2024")
- **Downloaded:** 17 Nov 2026 (original in [`_sources/cea-general-review/raw/`](../_sources/cea-general-review/raw/))
- **Script:** [`pipelines/cea-general-review/build_general_review.py`](../pipelines/cea-general-review/build_general_review.py); checks in `check_general_review.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `system` | Row label as printed (state, region, sub-total or total) |
| `year` | Financial year (April to March) as printed |
| `coal_000_t` | Coal, thousand tonnes |
| `furnace_oil_kl` | Furnace oil, kilolitres |
| `light_diesel_oil_hsd_kl` | Light diesel oil / HSD, kilolitres |
| `lshs_hhs_kl` | LSHS/HHS, kilolitres |
| `gas_mmscm` | Gas, million standard cubic metres |
| `biomass_t` | Biomass, tonnes |
| `lignite_000_t` | Lignite, thousand tonnes |
| `generation_coal_lignite_plants_gwh` | Generation of the coal/lignite-based plants, GWh |
| `source_marks` | Symbols printed next to a label or number, as `<column>:<symbol>` (explained in Notes) |

## Notes

- `Central Sector (NR)` etc. are central-sector stations of each region, printed as separate rows (blank `state_ut`).
- `source_marks` `gas_mmscm:*`: Karnataka's gas figure 765898 carries a star; CEA's footnote: "JSW Toranagallu TPS (SBU I & II) uses by-product waste gas from steel plant as a fuel which reduces the coal consumption".
- Checks: 46 rows; region sub-totals and All India recomputed: equal in every column except coal in the Northern and Western sub-totals (2 thousand tonnes off, rounding).
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
