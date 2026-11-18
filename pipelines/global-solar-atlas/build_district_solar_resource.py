"""Solar resource per district, India (BNY from Global Solar Atlas v2, Solargis / World Bank ESMAP).

Input:  _sources/global-solar-atlas/raw/India_GISdata_LTAy_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF/
          GHI, DNI, DIF, GTI, PVOUT, OPTA, TEMP .tif and monthly/PVOUT_01..12.tif   (fetch_gsa.sh)
        _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011
        _reference/geography.csv
Output: ENG_solar-resource_1999-to-2018_STATES_BNY_DIST/<same>.csv          (long-term yearly averages)
        ENG_solar-pv-output-monthly_1999-to-2018_STATES_BNY_DIST/<same>.csv (long-term average per calendar month)

District value = mean of the grid cells whose centre lies inside the district's 2011 boundary (as for
CLM_wind-resource-100m_*). The layers are long-term averages of daily totals, so units are per day.
Run from the repo root.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
import rasterio.mask
import shapefile
from shapely.geometry import mapping, shape

RAW = "_sources/global-solar-atlas/raw/India_GISdata_LTAy_AvgDailyTotals_GlobalSolarAtlas-v2_GEOTIFF"
SHP = "_sources/datameet-maps/raw/datameet-maps_census2011-districts_2011"
GEO = "_reference/geography.csv"
NAME = "ENG_solar-resource_1999-to-2018_STATES_BNY_DIST"
NAME_M = "ENG_solar-pv-output-monthly_1999-to-2018_STATES_BNY_DIST"
# layer -> (column name, decimals)
LAYERS = {
    "GHI": ("ghi_kwh_m2_day", 3), "DNI": ("dni_kwh_m2_day", 3), "DIF": ("dif_kwh_m2_day", 3),
    "GTI": ("gti_kwh_m2_day", 3), "PVOUT": ("pvout_kwh_kwp_day", 3), "OPTA": ("optimum_tilt_deg", 1),
    "TEMP": ("air_temperature_c", 2),
}


def district_mean(src, geom):
    """Mean of valid cells with centre in geom, and the share of the district's cells that are valid."""
    try:
        a, _ = rasterio.mask.mask(src, [mapping(geom)], crop=True, filled=False)
    except ValueError:  # district outside the raster
        return None, 0.0
    v = a[0].compressed().astype("float64")
    if src.nodata is not None and not np.isnan(src.nodata):
        v = v[v != src.nodata]
    v = v[np.isfinite(v)]
    expected = geom.area / (src.res[0] * src.res[1])
    cover = min(100.0, 100 * len(v) / expected) if expected else 0.0
    return (v.mean() if len(v) else None), cover


def main():
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    k = geo[(geo.level == "district") & (geo.census2011_district_code != "")].drop_duplicates("census2011_district_code").set_index("census2011_district_code")
    shapes = []
    for sr in shapefile.Reader(SHP).shapeRecords():
        c = sr.record.as_dict()["censuscode"]
        if c:
            shapes.append((f"{c:03d}", shape(sr.shape.__geo_interface__).buffer(0)))
    srcs = {layer: rasterio.open(f"{RAW}/{layer}.tif") for layer in LAYERS}
    months = {m: rasterio.open(f"{RAW}/monthly/PVOUT_{m:02d}.tif") for m in range(1, 13)}
    rows, mrows = [], []
    for cc, g in shapes:
        place = dict(state_ut=k.at[cc, "state_ut"], lgd_state_code=k.at[cc, "lgd_state_code"], district=k.at[cc, "district"],
                     lgd_district_code=k.at[cc, "lgd_district_code"], district_census_code=cc)
        row, cover = dict(place), None
        for layer, (col, dec) in LAYERS.items():
            m, c = district_mean(srcs[layer], g)
            row[col] = round(m, dec) if m is not None else None
            if layer == "PVOUT":
                cover = c
        row["raster_coverage_pct"] = round(cover, 1)
        rows.append(row)
        for mo, src in months.items():
            m, _ = district_mean(src, g)
            mrows.append(dict(place, month_of_year=mo, pvout_kwh_kwp_day=round(m, 3) if m is not None else None))
    df = pd.DataFrame(rows)
    mdf = pd.DataFrame(mrows)
    # A value from a sliver of the district would mislead: blank it (same rule as the wind table).
    low = set(df.loc[df.raster_coverage_pct < 50, "district_census_code"])
    vcols = [c for c, _ in LAYERS.values()]
    df.loc[df.district_census_code.isin(low), vcols] = None
    mdf.loc[mdf.district_census_code.isin(low), "pvout_kwh_kwp_day"] = None
    df["source_flag"] = np.where(df[vcols].isna().any(axis=1), "not_available", "")
    mdf["source_flag"] = np.where(mdf.pvout_kwh_kwp_day.isna(), "not_available", "")
    # source_flag only when something is blank (repo rule)
    df, mdf = (d if (d.source_flag != "").any() else d.drop(columns="source_flag") for d in (df, mdf))
    for name, d, keys in ((NAME, df, ["state_ut", "district"]), (NAME_M, mdf, ["state_ut", "district", "month_of_year"])):
        d = d.sort_values(keys)
        Path(name).mkdir(exist_ok=True)
        d.to_csv(f"{name}/{name}.csv", index=False, lineterminator="\n")
        print(name, d.shape)
    print("coverage below 90%:", df[df.raster_coverage_pct < 90][["district", "raster_coverage_pct"]].values.tolist())


if __name__ == "__main__":
    main()
