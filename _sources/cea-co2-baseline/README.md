# CEA CO2 Baseline Database for the Indian Power Sector, Version 22.0

Station- and unit-wise net generation and CO2 emissions of India's grid-connected thermal, hydro and nuclear power plants, and the grid emission factors CEA computes from them (CDM methodology).

- **Link:** https://cea.nic.in/cdm-co2-baseline-view?mappingId=234&lang=en ("CDM-CO2 Baseline Database Reports", reached from the Climate Change division page; no login)
- **Downloaded:** 17 Nov 2026
- **`raw/`:** `cea-co2-baseline_database_v22.xlsx` (sheets Data, Results, Transfer (1G), Units + Abbrev, Assumptions) and `cea-co2-baseline_user-guide_v22.pdf`
- **Scripts:** [`pipelines/cea-co2-baseline/build_co2_baseline.py`](../../pipelines/cea-co2-baseline/build_co2_baseline.py), [`check_co2_baseline.py`](../../pipelines/cea-co2-baseline/check_co2_baseline.py)

## Tables taken

| Sheet | Folder |
|---|---|
| Data | [`ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA`](../../ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA/) |
| Results | [`ENG_grid-emission-factor_2016-17-to-2025-26_IN_CEA`](../../ENG_grid-emission-factor_2016-17-to-2025-26_IN_CEA/) |

Not taken: "Transfer (1G)" (electricity transfers with Bhutan and Nepal; some cells are `#REF!` in the file), "Units + Abbrev" and "Assumptions" (fuel emission factors and conversion constants; read them in the Excel file). Older versions (PDF and ZIP, back to about version 10) are listed on the same page.
