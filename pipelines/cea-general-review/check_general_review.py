"""Checks for the CEA General Review 2025 tables (run after build_general_review.py, from the repo root).

For each table: duplicate keys, state names, numbers parse, no negatives, percentages 0-100,
and printed totals recomputed: each region sub-total = sum of the rows above it (since the previous sub-total),
All India = sum of the region sub-totals. Differences are reported, never corrected.
"""
import glob
import re

import pandas as pd

STATES = set("""Andaman & Nicobar Islands|Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chandigarh|Chhattisgarh|Dadra & Nagar Haveli and Daman & Diu|Delhi|Goa|Gujarat|Haryana|Himachal Pradesh|Jammu & Kashmir|Jharkhand|Karnataka|Kerala|Ladakh|Lakshadweep|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Puducherry|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal|All India|Dadra & Nagar Haveli|Daman & Diu""".split("|"))
SUB = re.compile(r"sub-total|region", re.I)
NAMES = ["ENG_renewable-capacity_2024-03_STATES_CEA", "ENG_td-losses_FY2023-24_STATES_CEA",
         "ENG_power-plant-fuel-use_FY2023-24_STATES_CEA", "ENG_electricity-sales-by-category_FY2023-24_STATES_CEA",
         "ENG_per-capita-consumption-by-category_FY2023-24_STATES_CEA", "ENG_per-capita-consumption_FY2023-24_STATES_CEA",
         "ENG_consumers-connected-load_2024-03_STATES_CEA", "ENG_electricity-consumption_2012-13-to-2023-24_STATES_CEA"]
# columns that are ratios (per capita, %) cannot be summed
NOSUM = re.compile(r"_pct$|_kwh$|per_capita")


def check(name):
    df = pd.read_csv(f"{name}/{name}.csv", dtype=str, keep_default_na=False)
    keys = ["system"] + [c for c in ("year", "date") if c in df]
    num = [c for c in df.columns if c not in ("state_ut", "lgd_state_code", "system", "year", "date", "source_marks")]
    print(f"\n== {name}: {df.shape[0]} rows x {df.shape[1]} cols")
    print("  duplicate keys:", int(df.duplicated(keys).sum()), "| empty system:", int((df.system == "").sum()))
    bad = sorted(set(df.state_ut) - STATES - {""})
    print("  state_ut not in list:", bad or "none")
    v = df[num].replace("", None).apply(pd.to_numeric, errors="coerce")
    nonnum = int((v.isna() & (df[num] != "")).sum().sum())
    print("  non-numeric cells:", nonnum, "| blank cells:", int((df[num] == "").sum().sum()),
          "| negatives:", int((v < 0).sum().sum()))
    pct = [c for c in num if c.endswith("_pct")]
    if pct:
        print("  % outside 0-100:", int(((v[pct] < 0) | (v[pct] > 100)).sum().sum()))
    sumcols = [c for c in num if not NOSUM.search(c) and not c.startswith("population")]
    if not sumcols:
        print("  totals: ratio columns only, not summable")
        return
    groups = [df] if "year" not in df or df.year.nunique() == 1 else [g for _, g in df.groupby("year", sort=False)]
    worst = []
    for g in groups:
        g = g.reset_index(drop=True)
        gv = g[sumcols].replace("", None).apply(pd.to_numeric, errors="coerce").fillna(0)
        last, subs = 0, []
        for i, s in enumerate(g.system):
            if SUB.search(s):
                part = gv.iloc[last:i]
                part = part[[not SUB.search(x) for x in g.system.iloc[last:i]]]
                d = (part.sum() - gv.iloc[i]).abs()
                worst += [(g.get("year", pd.Series([""])).iloc[0], s, c, round(d[c], 2)) for c in sumcols if d[c] > 1]
                subs.append(i)
                last = i + 1
        tot = [i for i, s in enumerate(g.state_ut) if s == "All India"]
        if tot:
            base = gv.iloc[subs] if subs else gv.iloc[: tot[0]]
            d = (base.sum() - gv.iloc[tot[0]]).abs()
            worst += [(g.get("year", pd.Series([""])).iloc[0], "All India", c, round(d[c], 2)) for c in sumcols if d[c] > 1]
    print(f"  totals recomputed ({len(sumcols)} columns): differences over 1 unit:", len(worst))
    for w in worst[:15]:
        print("   ", w)


for n in NAMES:
    check(n)
