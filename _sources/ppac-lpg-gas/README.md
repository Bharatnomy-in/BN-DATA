# PPAC LPG and city gas data

Petroleum Planning & Analysis Cell (Ministry of Petroleum & Natural Gas): the half-yearly LPG Profile Report and the state-wise Excel tables on PPAC's LPG and natural gas pages.

- **Links:** LPG Profile Report H1 FY 2026-27 (Nov 2026): https://ppac.gov.in/download.php?file=rep_studies/1794560760_LPG_Profile_Report_H1_FY_2026-27_Web_Version.pdf ; pages https://ppac.gov.in/infrastructure/lpg-distributors , https://ppac.gov.in/natural-gas/city-gas-distribution-network , https://ppac.gov.in/consumption/active-domestic-customers , https://ppac.gov.in/consumption/state-wise-pmuy-data , https://ppac.gov.in/consumption/state-wise (no login)
- **Downloaded:** 17 Nov 2026
- **Scripts:** [`pipelines/ppac-lpg-gas/build_ppac_lpg_gas.py`](../../pipelines/ppac-lpg-gas/build_ppac_lpg_gas.py), [`check_ppac_lpg_gas.py`](../../pipelines/ppac-lpg-gas/check_ppac_lpg_gas.py)

## Files in `raw/` and tables taken

| File | Tables | Folder(s) |
|---|---|---|
| `ppac-lpg-gas_lpg-profile-report_H1-FY2026-27.pdf` | Tables 2-12 and the distributor table (printed as "Figure 40") | `ENG_lpg-*_PPAC`, `ENG_auto-lpg-*_PPAC`, `ENG_pmuy-connections_2026-10_STATES_PPAC` (12 folders) |
| `ppac-lpg-gas_lpg-distributors_2026.xlsx` | State-wise LPG distributors of PSU OMCs, 2001 to 01.08.2026 | [`ENG_lpg-distributors_2001-to-2026_STATES_PPAC`](../../ENG_lpg-distributors_2001-to-2026_STATES_PPAC/) |
| `ppac-lpg-gas_cgd-network_2026.xlsx` | PNG connections and CNG stations, 31.01.2025 and 31.07.2026 | [`ENG_png-connections-cng-stations_2025-01-to-2026-07_STATES_PPAC`](../../ENG_png-connections-cng-stations_2025-01-to-2026-07_STATES_PPAC/) |
| `ppac-lpg-gas_active-domestic-customers_2026.xlsx`, `ppac-lpg-gas_pmuy-connections_2026.xlsx` | Same tables as the report's Tables 6 and 12, as on 01.08.2026 (older) | not converted |
| `ppac-lpg-gas_statewise-sales_2026.xlsx` | State-wise sales of all petroleum products, petrol (MS) and diesel (HSD), 2008-09 to 2025-26 | not converted yet (no LPG sheet) |

## Not found at PPAC

LPG coverage per 100 households, refills per consumer (all and PMUY), state-wise commercial (19 kg) LPG sales, and retail cylinder prices outside the four metros are not in these files. Retail LPG prices for metro cities are published by IOCL (linked from PPAC's prices page).
