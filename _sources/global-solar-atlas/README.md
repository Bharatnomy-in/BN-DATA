# Global Solar Atlas 2.0

Used for [`ENG_solar-resource_1999-to-2018_STATES_BNY_DIST/`](../../ENG_solar-resource_1999-to-2018_STATES_BNY_DIST/) and [`ENG_solar-pv-output-monthly_1999-to-2018_STATES_BNY_DIST/`](../../ENG_solar-pv-output-monthly_1999-to-2018_STATES_BNY_DIST/).

- **Data:** Global Solar Atlas 2.0 (Solargis, for the World Bank / ESMAP), India country GIS data: long-term yearly averages of daily totals of GHI, DNI, DIF, GTI, PVOUT, optimum tilt (OPTA) and air temperature (TEMP), plus monthly PVOUT, GeoTIFF (EPSG:4326). CC BY 4.0.
- **Link:** https://globalsolaratlas.info/download/india; the file is `https://api.globalsolaratlas.info/download/India/India_GISdata_LTAym_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF.zip` (no login)
- **Downloaded:** 18 Nov 2026
- **`raw/`:** not committed (about 820 MB unzipped). Run `sh pipelines/global-solar-atlas/fetch_gsa.sh` from the repo root.
- Not taken: the same data as ASCII grids (`AAIGRID`) and as monthly/yearly totals (`YearlyMonthlyTotals`), which are the same values in other units; and the PNG/TIF poster maps.
