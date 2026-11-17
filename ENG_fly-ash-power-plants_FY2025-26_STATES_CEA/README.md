# Fly ash generated and used by coal power plants, 2025-26

For each coal/lignite thermal power plant (196 plants in 17 states): ash produced in the year and ash put to use (bricks, cement, roads, mine filling etc.), in lakh tonnes, and the share used.

## Source

- **Data:** Central Electricity Authority (CEA), *India Fly Ash Year Book 2026* (data for FY 2025-26, published August 2026)
- **Table taken from:** Tables 5.1 to 5.17, "Ash Generation and Utilization Data of <State> for the FY 2025-26" (pages 47-94)
- **Link:** https://cea.nic.in/divisionPage/516?lang=en (file: https://cea.nic.in/api/dashboardReports/view-pdf/en/28e765d2-e835-4aad-91f7-4fd73891f82b)
- **Downloaded:** 17 Nov 2026 (original in [`_sources/cea-fly-ash/raw/`](../_sources/cea-fly-ash/raw/))
- **Script:** [`pipelines/cea-fly-ash/build_fly_ash.py`](../pipelines/cea-fly-ash/build_fly_ash.py); checks in `check_fly_ash.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `plant` | Plant name as printed; `Grand Total` for the state total row |
| `year` | Financial year (April to March) as printed |
| `s_no` | Serial number in the state table |
| `utility` | Power utility (owner) as printed |
| `installed_capacity_mw` | Installed capacity, MW |
| `state_as_printed` | State name as printed in the source |
| `ash_generation_lmt` | Total ash generated in 2025-26, lakh tonnes (1 LMT = 100,000 tonnes) |
| `ash_utilization_lmt` | Total ash utilised, lakh tonnes |
| `ash_utilization_pct` | Actual ash utilisation, % (above 100 when ash stored in ponds from earlier years is also used) |
| `table` | Table number in the Year Book |

## Notes

- Plant names and utilities printed on two lines are joined; words split by a hyphen at the line end are rejoined ("LIM-" + "ITED").
- In Maharashtra row 11 the source prints "APL" as the plant and "ADANI ELECTRICITY MUMBAI LIMITED" as the utility (Dahanu); kept as printed.
- Assam has one plant and no Grand Total row.
- Checks (17 Nov 2026): 196 plants, matching the Year Book's count; every state's Grand Total equals the sum of its plants; serial numbers run 1..n. In 12 rows the printed % differs from utilisation / generation by more than 0.1 (e.g. Ropar 376.68 against 376.9); kept as printed.
- **Nagpur:** plants in Nagpur district are Koradi, Khaparkheda and Mouda (NTPC); nearby in Vidarbha: Chandrapur, Tiroda, GMR Warora, Dhariwal, Sai Wardha, Bela TPS, Amravati. Butibori and MIHAN are not in the Year Book.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
