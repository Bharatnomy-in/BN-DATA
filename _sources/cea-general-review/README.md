# CEA General Review 2025 (All India Electricity Statistics)

Central Electricity Authority's yearly compendium of electricity statistics: capacity, generation, losses, fuel, consumption by category, consumers and connected load, per capita consumption, by state. The 2025 edition contains data for 2023-24.

- **Link:** https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1001&subSubHeadingId=10084&title=General%20Review&lang=en (the 2025 edition is listed there as "2024"; no login)
- **Downloaded:** 17 Nov 2026
- **`raw/`:** `cea-general-review_all-india-electricity-statistics_2025.pdf` (198 pages, 12 MB)
- **Scripts:** [`pipelines/cea-general-review/build_general_review.py`](../../pipelines/cea-general-review/build_general_review.py) (numbers placed by x-position under the columns of the total row), [`check_general_review.py`](../../pipelines/cea-general-review/check_general_review.py)

## Tables taken

| Table | Folder |
|---|---|
| 1.7 Electricity consumption by ultimate consumers, state-wise, 2012-13 to 2023-24 | [`ENG_electricity-consumption_2012-13-to-2023-24_STATES_CEA`](../../ENG_electricity-consumption_2012-13-to-2023-24_STATES_CEA/) |
| 3.11 Installed renewable capacity by state, 31.03.2024 | [`ENG_renewable-capacity_2024-03_STATES_CEA`](../../ENG_renewable-capacity_2024-03_STATES_CEA/) |
| 6.4 State-wise system (T&D) losses | [`ENG_td-losses_FY2023-24_STATES_CEA`](../../ENG_td-losses_FY2023-24_STATES_CEA/) |
| 7.1 Fossil fuel consumption in thermal stations by state | [`ENG_power-plant-fuel-use_FY2023-24_STATES_CEA`](../../ENG_power-plant-fuel-use_FY2023-24_STATES_CEA/) |
| 9.3 Sales to ultimate consumers by category and state | [`ENG_electricity-sales-by-category_FY2023-24_STATES_CEA`](../../ENG_electricity-sales-by-category_FY2023-24_STATES_CEA/) |
| 9.7 Per capita ultimate consumption by category and state | [`ENG_per-capita-consumption-by-category_FY2023-24_STATES_CEA`](../../ENG_per-capita-consumption-by-category_FY2023-24_STATES_CEA/) |
| 9.9 Annual per capita consumption by state | [`ENG_per-capita-consumption_FY2023-24_STATES_CEA`](../../ENG_per-capita-consumption_FY2023-24_STATES_CEA/) |
| 10 Consumers and connected load by category and state | [`ENG_consumers-connected-load_2024-03_STATES_CEA`](../../ENG_consumers-connected-load_2024-03_STATES_CEA/) |

## Not taken yet

The other tables of the release are in the PDF: installed capacity and generation by state and mode (3.3-3.10, 4.3-4.7), captive plants (chapter 5), auxiliary consumption (6.5.x), peak demand (7.4), plant load factor (7.6), coal consumption by plant (7.7), transmission line length and transformers by state (8.1, 8.2: useful for substations), category-wise shares (9.6), electrical accidents (9.10), villages electrified and pump sets energised (11.2, 11.3), power trading (chapter 12), and the station lists (Appendices A-C: every thermal, hydro and nuclear station with units and capacity). Older editions (2019-2024) are on the same page; the 2024 edition's file (data 2022-23) arrives truncated from CEA's server (17 Nov 2026).
