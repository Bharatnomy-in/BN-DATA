"""Checks for ENG_energy-supply-position_2013-01-to-2026-08_STATES_CEA (run from the repo root after build_psp_energy.py).

- one row per system and month; state names in the standard list
- shortfall = requirement - supplied (within 1 MU of rounding), for the month and April-to-month
- supplied <= requirement; percentages within -100..100
- region totals = sum of the rows listed above them in the same report (states, DVC, Others), within 2 MU
- All India = sum of the five regions, within 2 MU
"""
import pandas as pd

NAME = "ENG_energy-supply-position_2013-01-to-2026-08_STATES_CEA"
REGIONS = ["Northern Region", "Western Region", "Southern Region", "Eastern Region", "North-Eastern Region"]
MEMBERS = {
    "Northern Region": ["Chandigarh", "Delhi", "Haryana", "Himachal Pradesh", "Jammu & Kashmir", "J&K and Ladakh",
                        "Punjab", "Rajasthan", "Uttar Pradesh", "Uttarakhand", "Others (Northern Region)"],
    "Western Region": ["Chhattisgarh", "Gujarat", "Madhya Pradesh", "Maharashtra", "Daman & Diu", "Dadra & Nagar Haveli",
                       "Dadra & Nagar Haveli and Daman & Diu", "Goa", "Others (Western Region)"],
    "Southern Region": ["Andhra Pradesh", "Telangana", "Karnataka", "Kerala", "Tamil Nadu", "Puducherry",
                        "Others (Southern Region)"],
    "Eastern Region": ["Bihar", "DVC", "Jharkhand", "Odisha", "West Bengal", "Sikkim", "Others (Eastern Region)"],
    "North-Eastern Region": ["Arunachal Pradesh", "Assam", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Tripura",
                             "Others (North-Eastern Region)"],
}
REGION_OF = {s: r for r, ss in MEMBERS.items() for s in ss}
df = pd.read_csv(f"{NAME}/{NAME}.csv", dtype={"year": str}, keep_default_na=False)
num = [c for c in df.columns if c.endswith(("_mu", "_pct"))]
v = df[num].replace("", None).apply(pd.to_numeric)
print(NAME, df.shape, df.month.nunique(), "months", df.month.min(), "to", df.month.max())
print("duplicate system-month:", int(df.duplicated(["system", "month"]).sum()), "| empty system:", int((df.system == "").sum()))
print("state_ut values:", sorted(set(df.state_ut) - {""}))
for pre in ("", "apr_to_month_"):
    req, sup = v[f"{pre}energy_requirement_mu"], v[f"{pre}energy_supplied_mu"]
    gap = v[f"{pre}energy_not_supplied_mu"].fillna(-v[f"{pre}surplus_deficit_mu"])
    bad = df[((req - sup) - gap).abs() > 1]
    print(f"[{pre or 'month'}] shortfall != requirement - supplied: {len(bad)} rows", bad[["system", "month"]].head(5).values.tolist())
    over = df[sup > req + 0.5]
    print(f"[{pre or 'month'}] supplied > requirement: {len(over)} rows", over[["system", "month"]].head(5).values.tolist())
    p = v[[f"{pre}energy_not_supplied_pct", f"{pre}surplus_deficit_pct"]]
    print(f"[{pre or 'month'}] % outside -100..100:", int(((p < -100) | (p > 100)).sum().sum()))
    # region totals (Lakshadweep and Andaman & Nicobar are stand-alone systems outside the regional totals, per CEA)
    diffs = []
    reg = df.system.map(REGION_OF)
    col = f"{pre}energy_requirement_mu"
    for m, g in df.groupby("month"):
        gv = v.loc[g.index, col]
        for r in REGIONS:
            tot = gv[g.system == r]
            if tot.isna().all():
                continue
            d = gv[reg.loc[g.index] == r].sum() - tot.iloc[0]
            if abs(d) > 2:
                diffs.append((m, r, round(d, 1)))
        ai = gv[g.system == "All India"]
        if not ai.isna().all():
            d = gv[g.system.isin(REGIONS)].sum() - ai.iloc[0]
            if abs(d) > 2:
                diffs.append((m, "All India", round(d, 1)))
    print(f"[{pre or 'month'}] requirement totals off by > 2 MU: {len(diffs)}", diffs[:12])
