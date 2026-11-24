"""Checks for the two Maharashtra power-station district tables. Run from the repo root."""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import build_station_districts_mh as b  # noqa: E402

ok = True


def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(f"{'PASS' if cond else 'FAIL'}  {name}{'  ' + str(detail) if detail and not cond else ''}")


def load(n):
    return pd.read_csv(Path(n) / f"{n}.csv", dtype={"lgd_district_code": str})


geo = pd.read_csv("_reference/geography.csv", dtype=str)
mh = geo[(geo.level == "district") & (geo.state_ut == "Maharashtra")]
valid = set(zip(mh.district, mh.lgd_district_code))
lk = pd.read_csv(b.LOOKUP, dtype=str)
check("lookup: one row per station", not lk.station.duplicated().any())
check("lookup: district + LGD code pairs exist in geography.csv", set(zip(lk.district, lk.lgd_district_code)) <= valid)

print(f"\n{b.OUT_CO2}")
c = load(b.OUT_CO2)
src = pd.read_csv(Path(b.CO2) / f"{b.CO2}.csv")
src = src[src.state_ut == "Maharashtra"]
check("rows = source Maharashtra rows (stations x years)", len(c) == len(src) == c.station.nunique() * c.year.nunique(),
      f"{len(c)} vs {len(src)}")
check("no duplicate station-year", not c.duplicated(["station", "year"]).any())
check("every row has a district code", c.lgd_district_code.notna().all())
m = c.merge(src, on=["station", "year"], suffixes=("", "_src"))
for col in ["net_generation_gwh", "co2_emissions_t", "capacity_mw_2026_03_31"]:
    a, s = pd.to_numeric(m[col]), pd.to_numeric(m[col + "_src"])
    check(f"{col} identical to source", ((a == s) | (a.isna() & s.isna())).all())
num = c[["net_generation_gwh", "co2_emissions_t", "capacity_mw_2026_03_31"]].apply(pd.to_numeric)
check("no negative generation, CO2 or capacity", (num.fillna(0) >= 0).all().all())
ci = pd.to_numeric(c.co2_intensity_t_per_mwh).dropna()
check("CO2 intensity within 0-2 t/MWh", ((ci >= 0) & (ci <= 2)).all(), ci[(ci < 0) | (ci > 2)].tolist())

print(f"\n{b.OUT_ASH}")
a = load(b.OUT_ASH)
srca = pd.read_csv(Path(b.ASH) / f"{b.ASH}.csv")
srca = srca[srca.state_ut == "Maharashtra"]
check("rows = source Maharashtra rows", len(a) == len(srca))
check("every plant tied to a CEA CO2 station", a[a.district != "State total"].cea_co2_station.isin(lk.station).all())
p = a[a.district != "State total"]
t = a[a.district == "State total"].iloc[0]
for col in ["ash_generation_lmt", "ash_utilization_lmt"]:
    s = round(p[col].sum(), 2)
    check(f"{col}: plants add up to the printed Grand Total ({s} vs {t[col]})", abs(s - t[col]) < 0.05)
cap = p.merge(lk, left_on="cea_co2_station", right_on="station")
co2cap = c[c.year == c.year.max()].set_index("station").capacity_mw_2026_03_31
diff = [(r.plant, r.installed_capacity_mw, co2cap[r.cea_co2_station]) for r in cap.itertuples()
        if float(r.installed_capacity_mw) != float(co2cap[r.cea_co2_station])]
check("fly-ash capacity = CO2-database capacity of the tied station (sanity check of the name tie)", not diff, diff)

print("\nSpot check (CSV | source):")
for _, r in c.sample(5, random_state=3).iterrows():
    s = src[(src.station == r.station) & (src.year == r.year)].iloc[0]
    print(f"  {r.station} {r.year} [{r.district}]: {r.net_generation_gwh} GWh, {r.co2_emissions_t} t | "
          f"{s.net_generation_gwh} GWh, {s.co2_emissions_t} t")
sys.exit(0 if ok else 1)
