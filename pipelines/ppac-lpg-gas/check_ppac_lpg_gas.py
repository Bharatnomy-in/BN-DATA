"""Checks for the PPAC LPG / city gas tables (run from the repo root after build_ppac_lpg_gas.py).

- duplicate keys, state names, numbers parse, no negatives
- each "Sub Total <region>" = sum of the rows above it since the previous sub-total; All India = sum of sub-totals
- row totals = sum of their parts where the table prints a total column
"""
import glob
import re

import pandas as pd

for n in sorted(glob.glob("ENG_*_PPAC")):
    d = pd.read_csv(f"{n}/{n}.csv", dtype=str, keep_default_na=False)
    keys = [c for c in ("system", "area_group", "date", "as_on", "period", "source_row") if c in d]
    num = [c for c in d.columns if c.endswith(("_count", "_tmt", "_tmtpa", "_lakh", "_t"))]
    v = d[num].replace("", None).apply(pd.to_numeric, errors="coerce")
    print(f"\n== {n}: {d.shape[0]} rows x {d.shape[1]} cols")
    print("  duplicate keys:", int(d.duplicated(keys).sum()), "| non-numeric:", int((v.isna() & (d[num] != "")).sum().sum()),
          "| negatives:", int((v < 0).sum().sum()), "| blank cells:", int((d[num] == "").sum().sum()))
    if "system" not in d:
        t = d.area_group == "Grand Total"
        for date, g in d.groupby("date"):
            gv = v.loc[g.index]
            tot = gv[g.area_group == "Grand Total"].iloc[0]
            diff = (gv[g.area_group != "Grand Total"].sum() - tot).abs()
            print(f"  {date}: area groups vs Grand Total, differences:", {c: round(x, 2) for c, x in diff.items() if x > 0.5})
        continue
    groups = [g for _, g in d.groupby("as_on", sort=False)] if "as_on" in d else [d]
    bad = []
    for g in groups:
        gv = v.loc[g.index].fillna(0)
        last, subs = None, []
        idx = list(g.index)
        for k, i in enumerate(idx):
            if re.match(r"(?i)sub total", g.at[i, "system"]):
                part = gv.loc[idx[(idx.index(last) + 1) if last is not None else 0]:idx[k - 1]]
                diff = (part.sum() - gv.loc[i]).abs()
                bad += [(g.get("as_on", pd.Series([""], index=[i])).get(i, ""), g.at[i, "system"], c, round(x, 4)) for c, x in diff.items() if x > 0.051]
                subs.append(i)
                last = i
            if g.at[i, "state_ut"] == "All India":
                diff = (gv.loc[subs].sum() - gv.loc[i]).abs()
                bad += [(g.get("as_on", pd.Series([""], index=[i])).get(i, ""), "All India", c, round(x, 4)) for c, x in diff.items() if x > 0.051]
    print(f"  sub-totals and All India recomputed: {len(bad)} differences", bad[:8])
    tot = [c for c in num if c.startswith("total")]
    if tot:
        parts = [c for c in num if c not in tot]
        off = ((v[parts].sum(axis=1) - v[tot[0]]).abs() > 0.011).sum()
        print(f"  parts = {tot[0]}: rows off by > 0.011: {int(off)}")
