"""Checks for WAT_odf-plus-villages_2022-to-2026_STATES_MOJS_DIST. Run from the repo root."""
import random
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import build_odf_plus as b  # noqa: E402

STATES = set("""Andaman & Nicobar Islands|Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chandigarh|Chhattisgarh|
Dadra & Nagar Haveli and Daman & Diu|Delhi|Goa|Gujarat|Haryana|Himachal Pradesh|Jammu & Kashmir|Jharkhand|
Karnataka|Kerala|Ladakh|Lakshadweep|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|
Puducherry|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal|All India"""
             .replace("\n", "").split("|"))
COUNTS = ["total_villages", "odf_plus_villages", "odf_plus_aspiring_villages", "odf_plus_rising_villages",
          "odf_plus_model_villages"]
ok = True


def check(name, cond, detail=""):
    global ok
    ok &= bool(cond)
    print(f"{'PASS' if cond else 'FAIL'}  {name}{'  ' + detail if detail and not cond else ''}")


d = pd.read_csv(Path(b.NAME) / f"{b.NAME}.csv", dtype={"lgd_state_code": str, "lgd_district_code": str,
                                                       "sbm_district_code": str})
dist = d[~d.district.isin(["State total", "All India"])]
tot = d[d.district == "State total"]
n_obj = len(b.district_objects(b.page()))
check("rows = districts x 2 dates", len(dist) == n_obj * 2, f"{len(dist)} vs {n_obj * 2}")
check("no duplicate keys", not d.duplicated(["state_ut", "district", "sbm_district_code", "date"]).any())
check("no empty keys", d[["state_ut", "district", "date"]].notna().all().all())
check("every district has an LGD code", dist.lgd_district_code.notna().all())
dup = dist[dist.date == b.PAGE_DATE].lgd_district_code.duplicated(keep=False)
check("no two dashboard districts share an LGD code", not dup.any(),
      str(dist[dist.date == b.PAGE_DATE][dup][["state_ut", "district", "lgd_district_code"]].values.tolist()))
check("state_ut in the list", set(d.state_ut) <= STATES, str(set(d.state_ut) - STATES))
check("counts numeric, non-negative", (d[COUNTS].apply(pd.to_numeric) >= 0).all().all())
pct = dist[["odf_plus_villages_pct", "odf_plus_model_villages_pct"]]
check("percentages 0-100", ((pct >= 0) & (pct <= 100)).all().all())
check("aspiring + rising + model = ODF Plus villages",
      (d[COUNTS[2:]].sum(axis=1) == d.odf_plus_villages).all())
check("ODF Plus villages <= total villages", (d.odf_plus_villages <= d.total_villages).all(),
      str(d[d.odf_plus_villages > d.total_villages][["state_ut", "district", "date"]].values.tolist()[:10]))
# published state totals vs district sums
s = dist.groupby(["state_ut", "date"])[COUNTS].sum()
t = tot.set_index(["state_ut", "date"])[COUNTS]
diff = (s - t.reindex(s.index)).abs().sum(axis=1)
check("district sums = printed state totals", (diff == 0).all(), str(diff[diff != 0].to_dict()))
ai = d[d.state_ut == "All India"].set_index("date")[COUNTS]
check("state totals add up to the printed All India row", (tot.groupby("date")[COUNTS].sum() - ai).abs().sum().sum() == 0)
pc = (dist.odf_plus_villages / dist.total_villages * 100).round(2)
check("published % = ODF Plus / total villages (2 dp)", ((pc - dist.odf_plus_villages_pct).abs() <= 0.011).all())

print("\nSpot check (CSV row | dashboard object):")
objs = {(o["dtcode11"], b.html.unescape(o["dtname"]).strip()): o for o in b.district_objects(b.page())}
random.seed(1)
for _, r in dist.sample(5, random_state=1).iterrows():
    o = objs[(r.sbm_district_code, r.district)]
    k = 0 if r.date == b.OLD_DATE else 1
    print(f"  {r.state_ut} / {r.district} {r.date}: model {r.odf_plus_model_villages}, ODF+ {r.odf_plus_villages} | "
          f"{b.FIELDS['odf_plus_model_villages'][k]}={o[b.FIELDS['odf_plus_model_villages'][k]]}, "
          f"{b.FIELDS['odf_plus_villages'][k]}={o[b.FIELDS['odf_plus_villages'][k]]}")
sys.exit(0 if ok else 1)
