"""Checks for ENG_fly-ash-power-plants_FY2025-26_STATES_CEA (run from the repo root after build_fly_ash.py).

- one row per state and serial number; state printed in the row = state of the table; numbers parse
- each state's Grand Total = sum of its plants (generation, utilisation)
- utilisation % = utilisation / generation x 100 (within 0.1); % above 100 is possible (old ash from ponds is used)
"""
import pandas as pd

N = "ENG_fly-ash-power-plants_FY2025-26_STATES_CEA"
d = pd.read_csv(f"{N}/{N}.csv", dtype=str, keep_default_na=False)
num = ["installed_capacity_mw", "ash_generation_lmt", "ash_utilization_lmt", "ash_utilization_pct"]
v = d[num].replace("", None).apply(pd.to_numeric, errors="coerce")
pl = d.plant != "Grand Total"
print(N, d.shape, "|", int(pl.sum()), "plants in", d.state_ut.nunique(), "states")
print("duplicate state + s_no:", int(d[pl].duplicated(["state_ut", "s_no"]).sum()),
      "| s_no not 1..n:", [s for s, g in d[pl].groupby("state_ut") if list(g.s_no) != [str(i) for i in range(1, len(g) + 1)]])
print("state printed differs from table:", d[pl & (d.state_as_printed != d.state_ut)][["state_ut", "plant", "state_as_printed"]].values.tolist())
print("non-numeric:", int((v.isna() & (d[num] != "")).sum().sum()), "| blank plant/utility:",
      int(((d.plant == "") | (d.utility == "") & pl).sum()), "| negatives:", int((v < 0).sum().sum()))
for s, g in d.groupby("state_ut", sort=False):
    gv = v.loc[g.index]
    if not (g.plant == "Grand Total").any():
        print("  no Grand Total row:", s, len(g), "plant(s)")
        continue
    t = gv[g.plant == "Grand Total"].iloc[0]
    sm = gv[g.plant != "Grand Total"].sum()
    diff = {c: round(sm[c] - t[c], 2) for c in ("ash_generation_lmt", "ash_utilization_lmt") if abs(sm[c] - t[c]) > 0.05}
    if diff:
        print("  total differs:", s, diff)
calc = v.ash_utilization_lmt / v.ash_generation_lmt * 100
bad = d[(calc - v.ash_utilization_pct).abs() > 0.1]
print("% != utilisation/generation:", bad[["state_ut", "plant", "ash_generation_lmt", "ash_utilization_lmt", "ash_utilization_pct"]].values.tolist())
print("plants above 100% utilisation:", int((v.ash_utilization_pct[pl] > 100).sum()))
