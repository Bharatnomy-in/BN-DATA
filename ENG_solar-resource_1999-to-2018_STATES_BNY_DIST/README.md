# Solar resource by district, India, 1999 to 2018 (long-term average)

How much sunlight reaches the ground and how much electricity a solar panel would produce in every district: long-term averages of daily irradiation (global, direct, diffuse, at optimum tilt), potential PV output per kW of panels, the best panel tilt, and air temperature. Computed by Bharatnomy from the Global Solar Atlas.

## Source

- **Data:** Global Solar Atlas 2.0 (Solargis, for the World Bank / ESMAP), India country GIS data, long-term averages of daily totals (`India_GISdata_LTAy_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF`). Irradiation and PV output cover 1999-2018, air temperature 1994-2018. CC BY 4.0
- **Link:** https://globalsolaratlas.info/download/india (file list: https://api.globalsolaratlas.info/download/India; no login)
- **Downloaded:** 18 Nov 2026 (rasters not committed, about 820 MB; `pipelines/global-solar-atlas/fetch_gsa.sh` downloads them, see [`_sources/global-solar-atlas/`](../_sources/global-solar-atlas/))
- **District boundaries:** Census 2011 district map from DataMeet (see [`_sources/datameet-maps/`](../_sources/datameet-maps/))
- **Script:** [`pipelines/global-solar-atlas/build_district_solar_resource.py`](../pipelines/global-solar-atlas/build_district_solar_resource.py) (writes both solar tables)

## How it is computed

- District value = plain mean of the grid cells whose centre lies inside the district's 2011 boundary (GHI, DNI, DIF, GTI on a 9 arc-second grid, about 250 m; PVOUT and temperature on 30 arc-seconds, about 1 km; optimum tilt on 2 arc-minutes). Same method as [`CLM_wind-resource-100m_*`](../CLM_wind-resource-100m_2008-to-2017_STATES_BNY_DIST/).
- `raster_coverage_pct` = cells with a value as % of the cells the district's area would hold; a district below 50% would be left blank (none is; Lakshadweep is lowest at 53%, its islands are small).

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code`, `district`, `lgd_district_code`, `district_census_code` | Place (2011 boundary; today's name and LGD code; LGD code blank for Mahe and Yanam) |
| `ghi_kwh_m2_day` | Global horizontal irradiation, long-term daily average, kWh per sq m per day |
| `dni_kwh_m2_day` | Direct normal irradiation (what concentrating solar uses), kWh/sq m/day |
| `dif_kwh_m2_day` | Diffuse horizontal irradiation, kWh/sq m/day |
| `gti_kwh_m2_day` | Global irradiation on a panel at the optimum tilt, kWh/sq m/day |
| `pvout_kwh_kwp_day` | Potential electricity output of a typical ground-mounted PV system per kW-peak installed, kWh/kWp/day (x 365 for a year) |
| `optimum_tilt_deg` | Panel tilt that maximises yearly output, degrees from horizontal |
| `air_temperature_c` | Air temperature at 2 m, long-term average (1994-2018), °C |
| `raster_coverage_pct` | Share of the district covered by valid grid cells, % |

## Notes

- **Our calculation from a modelled satellite product.** Values are averages over the whole district, including land not suitable for solar plants; the best sites in a district do better than the mean.
- PVOUT assumes Solargis' standard PV configuration (crystalline-silicon modules, fixed mount at optimum tilt, typical losses); a real plant's yield differs.
- 2011 boundaries throughout: `Thane` includes today's Palghar, etc.
- Checks (18 Nov 2026): 640 rows = 640 districts; no duplicate keys; no blank values; diffuse never above global irradiation; ranges: GHI 3.25-5.63, PVOUT 2.94-4.96 (highest Leh Ladakh, Rajsamand, Sirohi; lowest Kurung Kumey, Upper Subansiri, Upper Siang); the day-weighted mean of the 12 monthly PVOUT values equals the yearly value within 0.001. Nagpur: GHI 5.25, PVOUT 4.39, tilt 24.7°.
