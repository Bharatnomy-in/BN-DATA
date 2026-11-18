"""Population per district, all India, 1975 to 2030 (BNY from JRC GHSL GHS-POP R2023A).

Input:  _sources/jrc-ghsl/raw/GHS_POP_E<year>_GLOBE_R2023A_4326_30ss_V1_0.tif  (fetch_ghsl_pop.sh)
        _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011
        _reference/geography.csv
Output: POP_population-grid_1975-to-2030_STATES_BNY_DIST/<same>.csv

Each grid cell (30 arc-seconds, about 0.9 x 0.9 km) holds a number of residents. A cell belongs to the district
that contains its centre (same assignment as ENV_built-up-surface_*). District population = sum of its cells;
density = population / the cells' area on the WGS84 ellipsoid. Run from the repo root.
"""
import glob
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.windows import from_bounds

sys.path.insert(0, str(Path(__file__).parent))
from build_district_builtup import BOUNDS, RAW, cell_area_m2, districts, keys  # noqa: E402

NAME = "POP_population-grid_1975-to-2030_STATES_BNY_DIST"


def main():
    files = sorted(glob.glob(f"{RAW}/GHS_POP_E*_GLOBE_R2023A_4326_30ss_V1_0.tif"))
    assert len(files) == 12, f"expected 12 epochs, found {len(files)}"
    dists = districts()
    with rasterio.open(files[0]) as src:
        win = from_bounds(*BOUNDS, transform=src.transform).round_offsets().round_lengths()
        tr = src.window_transform(win)
        h, w = int(win.height), int(win.width)
    ids = rasterize(((g, c) for c, g in dists), out_shape=(h, w), transform=tr, fill=0, dtype="int32")
    area = np.repeat(cell_area_m2(tr, h, w)[:, None], w, axis=1)
    flat = ids.ravel()
    inside = flat > 0
    codes = np.unique(flat[inside])
    land = pd.Series(np.bincount(flat[inside], weights=area.ravel()[inside]))[codes].values
    rows = []
    for f in files:
        year = int(re.search(r"_E(\d{4})_", f).group(1))
        with rasterio.open(f) as src:
            v = src.read(1, window=win).astype("float64")
            if src.nodata is not None:
                v[v == src.nodata] = 0
        v[v < 0] = 0
        s = pd.Series(np.bincount(flat[inside], weights=v.ravel()[inside]))[codes].values
        rows.append(pd.DataFrame({"census": codes, "year": year, "pop": s, "area": land}))
        print(Path(f).name, "India total (in district polygons):", round(s.sum() / 1e6, 1), "million")
    r = pd.concat(rows)
    k = keys()
    out = pd.DataFrame({
        "state_ut": [k.at[f"{c:03d}", "state_ut"] for c in r.census],
        "lgd_state_code": [k.at[f"{c:03d}", "lgd_state_code"] for c in r.census],
        "district": [k.at[f"{c:03d}", "district"] for c in r.census],
        "lgd_district_code": [k.at[f"{c:03d}", "lgd_district_code"] for c in r.census],
        "district_census_code": [f"{c:03d}" for c in r.census],
        "year": r.year.values,
        "population_persons": r["pop"].round(0).astype("int64").values,
        "grid_land_area_sq_km": (r.area / 1e6).round(1).values,
        "population_density_per_sq_km": (r["pop"] / (r.area / 1e6)).round(1).values,
        "source_flag": np.where(r.year.values > 2020, "estimated", ""),
    })
    out = out.sort_values(["state_ut", "district", "year"])
    Path(NAME).mkdir(exist_ok=True)
    out.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, out.shape, "districts:", out.district_census_code.nunique())


if __name__ == "__main__":
    main()
