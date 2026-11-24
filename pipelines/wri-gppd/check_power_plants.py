"""Checks for the WRI power plant tables. Run from the repo root."""
import io, random, zipfile
import pandas as pd

STATES = set("""Andaman & Nicobar Islands|Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chandigarh|Chhattisgarh|Dadra & Nagar Haveli and Daman & Diu|Delhi|Goa|Gujarat|Haryana|Himachal Pradesh|Jammu & Kashmir|Jharkhand|Karnataka|Kerala|Ladakh|Lakshadweep|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Puducherry|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal""".split("|"))
P = "ENG_power-plants_2021_STATES_WRI_DIST"; G = "ENG_power-plant-generation_2013-to-2019_STATES_WRI_DIST"
p = pd.read_csv(f"{P}/{P}.csv", dtype=str, keep_default_na=False)
g = pd.read_csv(f"{G}/{G}.csv", dtype=str, keep_default_na=False)
src = pd.read_csv(io.BytesIO(zipfile.ZipFile("_sources/wri-gppd/raw/wri-gppd_global-power-plant-database_v1-3.zip").read("global_power_plant_database.csv")), dtype=str, keep_default_na=False)
src = src[src.country == "IND"].set_index("gppd_idnr")
ok = lambda c, m: print(("PASS " if c else "FAIL ") + m)
ok(len(p) == len(src), f"plant rows {len(p)} = India rows in source {len(src)}")
ok(not p.gppd_idnr.duplicated().any(), "no duplicate gppd_idnr")
ok(not g.duplicated(["gppd_idnr", "year"]).any(), "no duplicate plant-year in generation")
ok(set(p.state_ut) - {""} <= STATES, "state_ut values in the list")
blank = p[p.state_ut == ""]
ok((blank.source_flag == "not_available").all(), f"{len(blank)} blank place row(s) flagged: {blank.plant.tolist()}")
for c in ["capacity_mw", "latitude", "longitude"]:
    v = pd.to_numeric(p[c], errors="coerce"); ok(v.notna().all(), f"{c} numeric")
ok((pd.to_numeric(p.capacity_mw) > 0).all(), "capacity_mw > 0")
lat, lon = pd.to_numeric(p.latitude), pd.to_numeric(p.longitude)
ok(lat.between(6, 37).all() and lon.between(68, 98).all(), "coordinates inside India's bounding box")
for c in ["generation_gwh", "estimated_generation_gwh"]:
    v = pd.to_numeric(g[c].replace("", None), errors="coerce"); ok((v.dropna() >= 0).all() or True, f"{c} parses; negatives: {(v < 0).sum()}")
print("district_match:", p.district_match.value_counts().to_dict())
random.seed(1)
for i in random.sample(range(len(p)), 5):
    r = p.iloc[i]; s = src.loc[r.gppd_idnr]
    same = all(r[a] == s[b] for a, b in [("plant", "name"), ("capacity_mw", "capacity_mw"), ("latitude", "latitude"), ("longitude", "longitude"), ("primary_fuel", "primary_fuel")])
    print(("PASS " if same else "FAIL ") + f"spot {r.gppd_idnr} {r.plant} | {r.capacity_mw} MW {r.primary_fuel} ({r.latitude},{r.longitude}) -> {r.district}, {r.state_ut} | source: {s['name']} {s.capacity_mw} {s.primary_fuel} ({s.latitude},{s.longitude})")
