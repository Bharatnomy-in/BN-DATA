"""Light tidy + 2-3 added columns for 13 selected datasets (17 Nov 2026). Edits the CSVs in place and appends a
"Changes on 17 Nov 2026" section to each README. Run once, from the repo root, AFTER the dataset's own build
script (re-running a build script removes these columns; then run this again).

Tidy: helper columns dropped (source_marks, *_as_printed, census codes, source row ids where noted);
region / sub-total / central-sector rows dropped (state rows and All India kept).
Added columns are derived (Bharatnomy calculations), named in each README.
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd

TODAY = "17 Nov 2026"
DONE = {}
AGG = re.compile(r"(?i)sub.?total|region|central sector|^others")


def load(n):
    return pd.read_csv(f"{n}/{n}.csv", dtype=str, keep_default_na=False)


def num(s):
    return pd.to_numeric(s.replace("", np.nan), errors="coerce")


def fmt(x, nd=2):
    return x.round(nd).map(lambda v: "" if pd.isna(v) else (f"{v:.{nd}f}".rstrip("0").rstrip(".") if nd else str(int(v))))


def save(n, df, dropped, added, rows_note=""):
    df.to_csv(f"{n}/{n}.csv", index=False, lineterminator="\n")
    lines = ["", f"## Changes on {TODAY}", ""]
    if dropped:
        lines.append(f"- Columns removed (helpers): {', '.join(f'`{c}`' for c in dropped)}.")
    if rows_note:
        lines.append(f"- {rows_note}")
    lines.append("- Columns added (Bharatnomy calculations from the columns above, not published by the source):")
    lines += [f"  - `{c}`: {m}" for c, m in added.items()]
    lines.append(f"- Script: [`pipelines/enrich/enrich_13.py`](../pipelines/enrich/enrich_13.py). Re-running this folder's build script removes these changes; run `enrich_13.py` again after it.")
    p = Path(f"{n}/README.md")
    t = p.read_text()
    t = t.split(f"\n## Changes on {TODAY}")[0].rstrip("\n") + "\n"
    p.write_text(t + "\n".join(lines) + "\n")
    DONE[n] = df.shape
    print(n, df.shape)


def drop(df, cols):
    cols = [c for c in cols if c in df.columns]
    return df.drop(columns=cols), cols


def anomaly(df, col, base=(1981, 2010), key="district"):
    y = num(df.year)
    v = num(df[col])
    ref = v[(y >= base[0]) & (y <= base[1])].groupby(df.loc[(y >= base[0]) & (y <= base[1]), key]).mean()
    return v - df[key].map(ref)


def decade(df):
    return (num(df.year.str[:4]) // 10 * 10).astype("Int64").astype(str) + "s"


def fy(month):  # 2023-08 -> 2023-24
    y, m = int(month[:4]), int(month[5:7])
    s = y if m >= 4 else y - 1
    return f"{s}-{str(s + 1)[2:]}"


# ---------------------------------------------------------------- climate (user's three)
n = "CLM_temperature-indices_1951-to-2024_MH_BNY_DIST"
d = load(n); d, dr = drop(d, ["district_census_code"])
d["decade"] = decade(d)
d["tmax_mean_anomaly_c"] = fmt(anomaly(d, "tmax_mean_c"))
d["heatwave_days_anomaly"] = fmt(anomaly(d, "heatwave_days"), 1)
save(n, d, dr, {"decade": "Decade of the year (e.g. `2010s`)",
                "tmax_mean_anomaly_c": "Annual mean maximum temperature minus the district's 1981-2010 average, °C (positive = hotter than normal)",
                "heatwave_days_anomaly": "Heatwave days minus the district's 1981-2010 average"})

n = "CLM_rainfall-indices_1951-to-2025_MH_BNY_DIST"
d = load(n); d, dr = drop(d, ["district_census_code"])
d["decade"] = decade(d)
dep = num(d.rainfall_jun_sep_departure_pct)
d["monsoon_category"] = np.select([dep <= -100, dep <= -60, dep <= -20, dep < 20, dep < 60, dep >= 60],
                                  ["no rain", "large deficient", "deficient", "normal", "excess", "large excess"], "")
spi = num(d.spi_jun_sep)
d["monsoon_drought_class"] = np.select([spi <= -2, spi <= -1.5, spi <= -1, spi.notna()], ["extreme", "severe", "moderate", "none"], "")
save(n, d, dr, {"decade": "Decade of the year",
                "monsoon_category": "IMD category of June-September rainfall departure: large excess (60% or more), excess (20 to 59%), normal (-19 to +19%), deficient (-20 to -59%), large deficient (-60 to -99%), no rain",
                "monsoon_drought_class": "Drought class from `spi_jun_sep`: moderate (-1 to -1.49), severe (-1.5 to -1.99), extreme (-2 or less), none"})

n = "CLM_wind-humidity_1981-to-2025_MH_BNY_DIST"
d = load(n); d, dr = drop(d, ["district_census_code"])
d["decade"] = decade(d)
d["wind_speed_10m_anomaly_ms"] = fmt(anomaly(d, "wind_speed_10m_mean_ms"))
wb = num(d.wet_bulb_temp_highest_c)
d["wet_bulb_heat_stress"] = np.select([wb >= 35, wb >= 31, wb >= 28, wb.notna()], ["extreme", "high", "moderate", "low"], "")
save(n, d, dr, {"decade": "Decade of the year",
                "wind_speed_10m_anomaly_ms": "Mean 10 m wind speed minus the district's 1981-2010 average, m/s",
                "wet_bulb_heat_stress": "Class of the year's highest wet-bulb temperature: low (<28 °C), moderate (28-31), high (31-35, dangerous for outdoor work), extreme (35 or more, limit of human survivability)"})

# ---------------------------------------------------------------- energy
REGION = {"Northern": ["Chandigarh", "Delhi", "Haryana", "Himachal Pradesh", "Jammu & Kashmir", "Ladakh", "Punjab", "Rajasthan", "Uttar Pradesh", "Uttarakhand"],
          "Western": ["Chhattisgarh", "Gujarat", "Madhya Pradesh", "Maharashtra", "Daman & Diu", "Dadra & Nagar Haveli", "Dadra & Nagar Haveli and Daman & Diu", "Goa"],
          "Southern": ["Andhra Pradesh", "Telangana", "Karnataka", "Kerala", "Tamil Nadu", "Puducherry", "Lakshadweep"],
          "Eastern": ["Bihar", "Jharkhand", "Odisha", "West Bengal", "Sikkim", "Andaman & Nicobar Islands"],
          "North-Eastern": ["Arunachal Pradesh", "Assam", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Tripura"]}
REG = {s: r for r, ss in REGION.items() for s in ss}
REG["All India"] = "All India"

n = "ENG_energy-supply-position_2013-01-to-2026-08_STATES_CEA"
d = load(n); before = len(d)
d = d[~d.system.str.contains(AGG) & ~d.system.eq("DVC")].copy()
d, dr = drop(d, ["source_marks"])
d["financial_year"] = d.month.map(fy)
d["shortage_mu"] = d.energy_not_supplied_mu.where(d.energy_not_supplied_mu != "", fmt(-num(d.surplus_deficit_mu), 0))
d["shortage_pct"] = d.energy_not_supplied_pct.where(d.energy_not_supplied_pct != "", fmt(-num(d.surplus_deficit_pct), 1))
d.insert(2, "power_region", d.state_ut.map(REG).fillna(""))
save(n, d, dr, {"power_region": "CEA power region of the state (Northern, Western, Southern, Eastern, North-Eastern)",
                "financial_year": "April-March financial year of the month",
                "shortage_mu": "Energy not supplied in one sign convention, MU: positive = shortage (from `energy_not_supplied_mu`, or minus `surplus_deficit_mu` before 2017)",
                "shortage_pct": "Same as % of requirement"},
     f"Region, DVC and \"Others\" rows removed ({before - len(d)} rows); state rows (incl. the joint J&K and Ladakh row) and All India kept.")

n = "ENG_peak-demand_2013-01-to-2026-08_STATES_CEA"
d = load(n); before = len(d)
d = d[~d.system.str.contains(AGG) & ~d.system.eq("DVC")].copy()
d, dr = drop(d, ["source_marks"])
d["financial_year"] = d.month.map(fy)
d["shortage_mw"] = d.demand_not_met_mw.where(d.demand_not_met_mw != "", fmt(-num(d.surplus_deficit_mw), 0))
d["had_shortage"] = np.where(num(d.shortage_mw) > 0, "yes", np.where(num(d.shortage_mw).notna(), "no", ""))
save(n, d, dr, {"financial_year": "April-March financial year of the month",
                "shortage_mw": "Peak shortage in one sign convention, MW: positive = demand not met (from `demand_not_met_mw`, or minus `surplus_deficit_mw` before 2017)",
                "had_shortage": "`yes` if peak demand was not fully met that month"},
     f"Region, DVC and \"Others\" rows removed ({before - len(d)} rows).")

n = "ENG_electricity-sales-by-category_FY2023-24_STATES_CEA"
d = load(n); before = len(d)
d = d[~d.system.str.contains(AGG)].copy()
tot = num(d.total_sold_gwh)
d["domestic_share_pct"] = fmt(num(d.domestic_gwh) / tot * 100, 1)
d["industrial_share_pct"] = fmt((num(d.industrial_lv_mv_gwh) + num(d.industrial_hv_gwh)) / tot * 100, 1)
d["agriculture_share_pct"] = fmt(num(d.agriculture_gwh) / tot * 100, 1)
save(n, d, [], {"domestic_share_pct": "Domestic sales as % of total sold", "industrial_share_pct": "Industrial (LV, MV and HV) as % of total sold",
                "agriculture_share_pct": "Agriculture as % of total sold"}, f"Region sub-total rows removed ({before - len(d)} rows).")

n = "ENG_per-capita-consumption_FY2023-24_STATES_CEA"
d = load(n); before = len(d)
d = d[~d.system.str.contains(AGG)].copy()
pc = num(d.per_capita_consumption_kwh)
ai = pc[d.state_ut == "All India"].iloc[0]
d["ratio_to_all_india"] = fmt(pc / ai, 2)
st = d.state_ut.ne("All India")
d["rank_among_states"] = ""
d.loc[st, "rank_among_states"] = pc[st].rank(ascending=False, method="min").astype(int).astype(str)
d["consumption_band"] = np.select([pc < 1000, pc < 2000, pc.notna()], ["low (<1000 kWh)", "medium (1000-1999 kWh)", "high (2000+ kWh)"], "")
save(n, d, [], {"ratio_to_all_india": "Per capita consumption divided by the All India figure (1400 kWh)",
                "rank_among_states": "Rank by per capita consumption, 1 = highest (states and the joint J&K-Ladakh row)",
                "consumption_band": "Low (<1000), medium (1000-1999) or high (2000+ kWh per person)"}, f"Region rows removed ({before - len(d)} rows).")

n = "ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA"
d = load(n); before = len(d)
d = d[d.unit_no == "0"].copy()
d, dr = drop(d, ["unit_no", "commissioned", "state_as_printed", "source_marks", "in_operating_margin", "in_build_margin"])
cap = num(d.capacity_mw_2026_03_31)
d["plant_load_factor_pct"] = fmt((num(d.net_generation_gwh) * 1000 / (cap * 8760) * 100).where(cap > 0), 1)
d["is_coal"] = np.where(d.fuel_1.isin(["COAL", "LIGN"]), "yes", "no")
NAG = {"KORADI", "K_KHEDA II", "MOUDA STPS", "BUTIBORI TPP -II", "MIHAN TPP"}
d["near_nagpur"] = np.where(d.station.str.strip().isin(NAG), "yes", "no")
save(n, d, dr, {"plant_load_factor_pct": "Net generation as % of what the station's 31 Mar 2026 capacity could produce running all year (approximate PLF: uses current capacity and net, not gross, generation)",
                "is_coal": "`yes` if the main fuel is coal or lignite",
                "near_nagpur": "`yes` for stations in Nagpur district: Koradi, Khaparkheda (K_KHEDA II), Mouda, Butibori, MIHAN"},
     f"Unit rows removed: one row per station and year (station totals, `unit_no` 0); {before - len(d)} unit rows dropped.")

n = "ENG_coal-production_2015-16-to-2024-25_STATES_MOC"
d = load(n); d, dr = drop(d, ["state_as_printed"])
v = num(d.production_mt)
d["yoy_growth_pct"] = fmt(v.groupby(d.state_ut).pct_change(fill_method=None) * 100, 1)
ai = d[d.state_ut == "All India"].set_index("year").production_mt.map(float)
d["share_of_india_pct"] = fmt(v / d.year.map(ai) * 100, 1)
st = d.state_ut.ne("All India")
d["rank_in_year"] = ""
d.loc[st, "rank_in_year"] = v[st].groupby(d.loc[st, "year"]).rank(ascending=False, method="min").astype("Int64").astype(str).replace("<NA>", "")
save(n, d, dr, {"yoy_growth_pct": "Change from the previous year, %", "share_of_india_pct": "Share of All India production, %",
                "rank_in_year": "Rank among coal-producing states that year, 1 = largest"})

n = "ENG_pmuy-connections_2026-10_STATES_PPAC"
d = load(n); before = len(d)
reg, cur = [], []
for s in reversed(d.system.tolist()):
    m = re.match(r"(?i)sub total (.+)", s)
    if m:
        cur = m.group(1).title().replace("North East", "North-East")
    reg.append(cur if not m and s != "All India" else "")
d["ppac_region"] = list(reversed(reg))
d = d[~d.system.str.contains(AGG)].copy()
v = num(d.pmuy_connections_count)
ai = v[d.state_ut == "All India"].iloc[0]
d["share_of_india_pct"] = fmt(v / ai * 100, 2)
st = d.state_ut.ne("All India")
d["rank"] = ""
d.loc[st, "rank"] = v[st].rank(ascending=False, method="min").astype(int).astype(str)
d.loc[~st, "ppac_region"] = "All India"
save(n, d, [], {"ppac_region": "PPAC region the state is listed under (North, North-East, East, West, South)",
                "share_of_india_pct": "Share of All India PMUY connections, %", "rank": "Rank by PMUY connections, 1 = most"},
     f"Region sub-total rows removed ({before - len(d)} rows).")

# ---------------------------------------------------------------- environment / agriculture
n = "ENV_built-up-surface_1975-to-2030_STATES_BNY_DIST"
d = load(n); d, dr = drop(d, ["district_census_code"])
d = d.sort_values(["state_ut", "district", "year"], kind="stable")
v = num(d.built_up_sq_km)
key = d.state_ut + "|" + d.district
prev = v.groupby(key).shift(1)
d["change_since_previous_sq_km"] = fmt(v - prev, 3)
d["growth_since_previous_pct"] = fmt(((v - prev) / prev * 100).where(prev > 0), 1)
d["is_projection"] = np.where(num(d.year) > 2020, "yes", "no")
save(n, d, dr, {"change_since_previous_sq_km": "Change in built-up area since the previous epoch (5 years earlier), km²",
                "growth_since_previous_pct": "Same as % of the previous epoch's built-up area",
                "is_projection": "`yes` for 2025 and 2030, which GHSL projects rather than observes"})

n = "ENV_active-fires_2001-to-2025_STATES_BNY_DIST"
d = load(n); d, dr = drop(d, ["district_census_code"])
v = num(d.fire_detections)
d["share_mar_may_pct"] = fmt((num(d.fire_detections_mar_may) / v * 100).where(v > 0), 1)
d["share_oct_dec_pct"] = fmt((num(d.fire_detections_oct_dec) / v * 100).where(v > 0), 1)
d["rank_in_state_year"] = v.groupby([d.state_ut, d.year]).rank(ascending=False, method="min").astype("Int64").astype(str).replace("<NA>", "")
save(n, d, dr, {"share_mar_may_pct": "Share of the year's fire detections in March-May (forest fire season), %",
                "share_oct_dec_pct": "Share in October-December (kharif crop-residue burning season), %",
                "rank_in_state_year": "District's rank within its state that year, 1 = most fire detections"})

n = "AGR_land-use-irrigation_1998-99-to-2024-25_MH_MOAFW_DIST"
d = load(n); before = len(d)
d = d[d.district != "State total"].copy()
ns = num(d.net_area_sown_ha)
d["net_irrigated_pct_of_net_sown"] = fmt(num(d.net_irrigated_area_total_ha) / ns * 100, 1)
d["cropping_intensity_pct"] = fmt(num(d.gross_cropped_area_ha) / ns * 100, 1)
d["forest_pct_of_reporting_area"] = fmt(num(d.forests_ha) / num(d.reporting_area_ha) * 100, 1)
save(n, d, [], {"net_irrigated_pct_of_net_sown": "Net irrigated area as % of net sown area",
                "cropping_intensity_pct": "Gross cropped area as % of net sown area (100 = one crop a year)",
                "forest_pct_of_reporting_area": "Forest as % of reporting area"}, f"`State total` rows removed ({before - len(d)} rows).")

print(len(DONE), "datasets updated")
