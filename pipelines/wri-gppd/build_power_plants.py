"""Power plants of India with their location and district (WRI Global Power Plant Database v1.3).

Input:  _sources/wri-gppd/raw/wri-gppd_global-power-plant-database_v1-3.zip   (fetch_gppd.sh)
        _sources/datameet-maps/raw/datameet-maps_census2011-districts_2011     (district boundaries, 2011)
        _reference/geography.csv                                              (census code -> LGD codes)
Output: ENG_power-plants_2021_STATES_WRI_DIST/<same>.csv                      (one row per plant)
        ENG_power-plant-generation_2013-to-2019_STATES_WRI_DIST/<same>.csv    (one row per plant per year)

The only thing Bharatnomy adds is the place: each plant's point is placed in the 2011 district whose
boundary contains it. Points just outside every boundary (coast, river, border) go to the nearest
district within 0.1 degree (about 11 km) and are marked in `district_match`. Every published value
is kept as published. Run from the repo root.
"""
import io
import zipfile
from pathlib import Path

import pandas as pd
import shapefile
from shapely.geometry import Point, shape
from shapely.strtree import STRtree

ZIP = "_sources/wri-gppd/raw/wri-gppd_global-power-plant-database_v1-3.zip"
SHP = "_sources/datameet-maps/raw/datameet-maps_census2011-districts_2011"
GEO = "_reference/geography.csv"
NAME = "ENG_power-plants_2021_STATES_WRI_DIST"
NAME_G = "ENG_power-plant-generation_2013-to-2019_STATES_WRI_DIST"
NEAR_DEG = 0.1
PLACE = ["state_ut", "lgd_state_code", "district", "lgd_district_code", "district_census_code"]


def load_gppd():
    with zipfile.ZipFile(ZIP) as z:
        raw = z.read("global_power_plant_database.csv")
    d = pd.read_csv(io.BytesIO(raw), dtype=str, keep_default_na=False)
    return d[d.country == "IND"].copy()


def districts():
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    k = (geo[(geo.level == "district") & (geo.census2011_district_code != "")]
         .drop_duplicates("census2011_district_code").set_index("census2011_district_code"))
    codes, geoms = [], []
    for sr in shapefile.Reader(SHP).shapeRecords():
        c = sr.record.as_dict()["censuscode"]
        if c:
            codes.append(f"{c:03d}")
            geoms.append(shape(sr.shape.__geo_interface__).buffer(0))
    return k, codes, geoms


def main():
    d = load_gppd()
    k, codes, geoms = districts()
    tree = STRtree(geoms)
    place, how = [], []
    for lat, lon in zip(d.latitude.astype(float), d.longitude.astype(float)):
        p = Point(lon, lat)
        hit = [i for i in tree.query(p, predicate="intersects")]
        if hit:
            i, m = hit[0], "inside"
        else:
            i = int(tree.nearest(p))
            dist = geoms[i].distance(p)
            i, m = (i, "nearest_within_11km") if dist <= NEAR_DEG else (None, "outside_all_districts")
        if i is None:
            place.append({c: "" for c in PLACE})
        else:
            cc = codes[i]
            r = k.loc[cc] if cc in k.index else None
            place.append(dict(
                state_ut=r["state_ut"] if r is not None else "", lgd_state_code=r["lgd_state_code"] if r is not None else "",
                district=r["district"] if r is not None else "", lgd_district_code=r["lgd_district_code"] if r is not None else "",
                district_census_code=cc))
        how.append(m)
    pl = pd.DataFrame(place, index=d.index)
    d = pd.concat([pl, d], axis=1)
    d["district_match"] = how

    plants = d[PLACE + [
        "name", "gppd_idnr", "capacity_mw", "latitude", "longitude", "primary_fuel", "other_fuel1", "other_fuel2",
        "other_fuel3", "commissioning_year", "owner", "source", "url", "geolocation_source", "wepp_id",
        "year_of_capacity_data", "generation_data_source", "district_match"]].rename(columns={"name": "plant"})
    # The one place we leave blank is ours (point outside every 2011 boundary), so it gets a flag.
    plants["source_flag"] = (plants.state_ut == "").map({True: "not_available", False: ""})
    plants = plants.sort_values(["state_ut", "district", "plant", "gppd_idnr"])

    rows = []
    for _, r in d.iterrows():
        for y in range(2013, 2020):
            rep = r.get(f"generation_gwh_{y}", "")
            est = r.get(f"estimated_generation_gwh_{y}", "") if y <= 2017 else ""
            note = r.get(f"estimated_generation_note_{y}", "") if y <= 2017 else ""
            if rep == "" and est == "":
                continue
            rows.append({**{c: r[c] for c in PLACE}, "plant": r["name"], "gppd_idnr": r["gppd_idnr"], "year": str(y),
                         "generation_gwh": rep, "estimated_generation_gwh": est, "estimated_generation_note": note})
    gen = pd.DataFrame(rows).sort_values(["state_ut", "district", "plant", "gppd_idnr", "year"])

    for name, df in ((NAME, plants), (NAME_G, gen)):
        Path(name).mkdir(exist_ok=True)
        df.to_csv(f"{name}/{name}.csv", index=False, lineterminator="\n")
        print(name, df.shape)
    print(plants.district_match.value_counts().to_dict())


if __name__ == "__main__":
    main()
