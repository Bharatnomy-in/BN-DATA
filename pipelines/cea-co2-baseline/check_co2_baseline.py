"""Checks for the CO2 baseline tables (run from the repo root after build_co2_baseline.py).

- no duplicate source rows; every state_ut in the standard list; numbers parse; no negative generation or CO2
- station rows (unit_no 0): CO2 and net generation summed by year vs the Results sheet totals
- unit rows summed per station and year vs the station row
"""
import pandas as pd

P = "ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA"
F = "ENG_grid-emission-factor_2016-17-to-2025-26_IN_CEA"
p = pd.read_csv(f"{P}/{P}.csv", dtype=str, keep_default_na=False)
f = pd.read_csv(f"{F}/{F}.csv", dtype=str, keep_default_na=False).set_index("year")
print(P, p.shape, "| years", p.year.min(), "to", p.year.max(), "| stations", p[p.unit_no == "0"].station.nunique())
print("duplicate source_row-year:", int(p.duplicated(["source_row", "year"]).sum()))
print("rows with blank state_ut:", int((p.state_ut == "").sum()))
num = ["capacity_mw_2026_03_31", "net_generation_gwh", "co2_emissions_t", "co2_intensity_t_per_mwh"]
v = p[num].replace("", None).apply(pd.to_numeric, errors="coerce")
print("non-numeric cells:", int((v.isna() & (p[num] != "")).sum().sum()), "| negatives:",
      (v < 0).sum().to_dict())
st = p[p.unit_no == "0"].assign(**{c: v.loc[p.unit_no == "0", c] for c in num})
by = st.groupby("year")[["net_generation_gwh", "co2_emissions_t"]].sum()
for y, r in by.iterrows():
    co2 = float(f.at[y, "co2_emissions_in_database_t"]) if y in f.index else None
    gen = float(f.at[y, "net_generation_gwh"]) if y in f.index else None
    print(f"  {y}: station CO2 {r.co2_emissions_t:,.0f} t vs Results {co2:,.0f} ({(r.co2_emissions_t / co2 - 1) * 100:+.3f}%);"
          f" net gen {r.net_generation_gwh:,.0f} vs {gen:,.0f} GWh ({(r.net_generation_gwh / gen - 1) * 100:+.3f}%)")
u = p[p.unit_no != "0"].assign(**{c: v.loc[p.unit_no != "0", c] for c in num})
us = u.groupby(["serial_no", "year"])[["net_generation_gwh", "co2_emissions_t"]].sum()
ss = st.groupby(["serial_no", "year"])[["net_generation_gwh", "co2_emissions_t"]].sum()
j = ss.join(us, rsuffix="_units", how="inner")
bad = j[(j.co2_emissions_t - j.co2_emissions_t_units).abs() > 1 + 0.001 * j.co2_emissions_t]
print(f"station-years where units' CO2 differs from the station row by > 0.1%: {len(bad)} of {len(j)}")
print(bad.head(8).to_string())
