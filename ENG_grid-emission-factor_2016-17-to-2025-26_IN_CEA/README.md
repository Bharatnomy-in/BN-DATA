# Grid CO2 emission factors and totals, All India, 2016-17 to 2025-26

How much CO2 the Indian grid emits per unit of electricity (tonnes CO2 per MWh), by the CDM methods (weighted average, operating margin, build margin, combined margin), with the generation and emission totals behind them.

## Source

- **Data:** Central Electricity Authority (CEA), *CO2 Baseline Database for the Indian Power Sector*, Version 22.0 (1 August 2026)
- **Table taken from:** sheet "Results"
- **Link:** https://cea.nic.in/cdm-co2-baseline-view?mappingId=234&lang=en (CDM-CO2 Baseline Database Reports; Excel file "1. Baseline Carbon Dioxide Emission Database Version 22.0")
- **Downloaded:** 17 Nov 2026 (original in [`_sources/cea-co2-baseline/raw/`](../_sources/cea-co2-baseline/raw/) (database and user guide))
- **Script:** [`pipelines/cea-co2-baseline/build_co2_baseline.py`](../pipelines/cea-co2-baseline/build_co2_baseline.py); checks in `check_co2_baseline.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `year` | Financial year (April to March) as printed |
| `weighted_avg_emission_rate_t_per_mwh` | Weighted average emission rate of the fossil and must-run plants in the database (excl. imports), t CO2/MWh |
| `weighted_avg_grid_emission_rate_incl_re_captive_t_per_mwh` | Weighted average grid emission rate including renewables and captive injection (excl. imports): the usual "grid emission factor", t CO2/MWh |
| `simple_operating_margin_t_per_mwh` | Simple operating margin, t CO2/MWh |
| `build_margin_t_per_mwh` | Build margin, t CO2/MWh |
| `combined_margin_t_per_mwh` | Combined margin, t CO2/MWh |
| `weighted_avg_emission_rate_incl_imports_t_per_mwh` | Weighted average emission rate adjusted for imports, t CO2/MWh |
| `weighted_avg_grid_emission_rate_incl_re_captive_incl_imports_t_per_mwh` | Grid emission rate incl. renewables and captive, adjusted for imports, t CO2/MWh |
| `simple_operating_margin_incl_imports_t_per_mwh` | Simple operating margin adjusted for imports, t CO2/MWh |
| `build_margin_not_adjusted_for_imports_t_per_mwh` | Build margin (not adjusted for imports), t CO2/MWh |
| `combined_margin_incl_imports_t_per_mwh` | Combined margin adjusted for imports, t CO2/MWh |
| `gross_generation_gwh` | Gross generation total, GWh |
| `net_generation_gwh` | Net generation total, GWh |
| `must_run_share_of_net_generation` | Share of must-run (hydro/nuclear) in net generation, as a fraction (0.1459 = 14.59%) |
| `net_generation_in_operating_margin_gwh` | Net generation in the operating margin, GWh |
| `net_generation_20pct_gwh` | 20% of net generation, GWh |
| `net_generation_in_build_margin_gwh` | Net generation in the build margin, GWh |
| `net_renewable_generation_gwh` | Net renewable generation, GWh |
| `net_import_gwh` | Net import, GWh |
| `captive_injected_gwh` | Captive power injected into the grid, GWh |
| `thermal_captive_injected_gwh` | Thermal captive power injected into the grid, GWh |
| `total_net_generation_incl_imports_re_captive_gwh` | Total net generation including imports, renewables and captive, GWh |
| `co2_emissions_total_t` | Absolute CO2 emissions total, tonnes |
| `co2_emissions_in_database_t` | CO2 emissions of the stations in the database, tonnes |
| `co2_emissions_captive_t` | CO2 emissions of captive power injected, tonnes |
| `co2_emissions_operating_margin_t` | Absolute emissions in the operating margin, tonnes |
| `co2_emissions_build_margin_t` | Absolute emissions in the build margin, tonnes |

## Notes

- Operating margin uses the same year's data (ex post option). Import adjustments use the operating margin of the exporting grid; imports from other countries count as zero (CEA notes).
- The Results sheet's block "Not to publish: For User Examples" is not taken.
- National only: no state-wise emission factor is published.
