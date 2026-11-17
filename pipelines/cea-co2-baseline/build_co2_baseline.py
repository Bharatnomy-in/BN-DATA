"""CEA CO2 Baseline Database for the Indian Power Sector, Version 22.0 (1 Aug 2026).

Reads  _sources/cea-co2-baseline/raw/cea-co2-baseline_database_v22.xlsx
Writes ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA  (sheet "Data": every grid-connected
       thermal, hydro and nuclear station and unit, net generation and CO2 by year)
       ENG_grid-emission-factor_2016-17-to-2025-26_IN_CEA  (sheet "Results": grid emission factors and totals)
Run from the repo root:  .venv/bin/python pipelines/cea-co2-baseline/build_co2_baseline.py
"""
import re
from decimal import Decimal
from pathlib import Path

import openpyxl
import pandas as pd

XLSX = "_sources/cea-co2-baseline/raw/cea-co2-baseline_database_v22.xlsx"
PLANTS = "ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA"
FACTORS = "ENG_grid-emission-factor_2016-17-to-2025-26_IN_CEA"

STATE = {"ANDAMAN & NICOBAR": "Andaman & Nicobar Islands", "ANDHRA PRADESH": "Andhra Pradesh",
         "ARUNACHAL": "Arunachal Pradesh", "ASSAM": "Assam", "BIHAR": "Bihar", "CHATTISGARH": "Chhattisgarh",
         "CHHATISGARH": "Chhattisgarh", "DELHI": "Delhi", "GOA": "Goa", "GUJARAT": "Gujarat", "HARYANA": "Haryana",
         "HIMACHAL": "Himachal Pradesh", "HIMACHAL PRADESH": "Himachal Pradesh", "JAMMU & KASHMIR": "Jammu & Kashmir",
         "JHARKHAND": "Jharkhand", "KARNATAKA": "Karnataka", "KERALA": "Kerala", "LADAKH": "Ladakh",
         "LAKSHADWEEP": "Lakshadweep", "MADHYA PRADESH": "Madhya Pradesh", "MAHARASHTRA": "Maharashtra",
         "MANIPUR": "Manipur", "MEGHALAYA": "Meghalaya", "MIZORAM": "Mizoram", "NAGALAND": "Nagaland",
         "ODISHA": "Odisha", "ORISSA": "Odisha", "PUDUCHERRY": "Puducherry", "PUNJAB": "Punjab",
         "RAJASTHAN": "Rajasthan", "SIKKIM": "Sikkim", "TAMIL NADU": "Tamil Nadu", "TELANGANA": "Telangana",
         "TRIPURA": "Tripura", "UTTAR PRADESH": "Uttar Pradesh", "UTTARAKHAND": "Uttarakhand",
         "WEST BENGAL": "West Bengal"}
MEASURES = ["net_generation_gwh", "co2_emissions_t", "co2_intensity_t_per_mwh", "in_operating_margin", "in_build_margin"]


def plain(x):
    """12 significant digits (drops binary noise such as 8652.237000000001) written without an exponent."""
    s = f"{x:.12g}"
    return format(Decimal(s), "f") if "e" in s else s


def num(x):
    if x is None or (isinstance(x, str) and not x.strip()):
        return ""
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (int, float)):
        # 12 significant digits drops binary noise from the spreadsheet (8652.237000000001 -> 8652.237)
        return plain(x) if isinstance(x, float) else str(x)
    return str(x).strip()


def plants():
    ws = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)["Data"]
    rows = ws.iter_rows(values_only=True)
    hdr = [re.sub(r"\s+", " ", str(h or "")).strip() for h in next(rows)]
    assert hdr[:11] == ["S_NO", "NAME", "UNIT_NO", "DT_ COMM", "CAPACITY as on 31.03.2026 (MW)", "STATE", "SECTOR",
                        "SYSTEM", "TYPE", "FUEL 1", "FUEL 2"], hdr[:11]
    years = []
    for i in range(11, len(hdr), 5):
        y = hdr[i][:7]
        assert all(h.startswith(y) for h in hdr[i:i + 5]), hdr[i:i + 5]
        assert "Net Generation" in hdr[i] and "Absolute" in hdr[i + 1] and "Specific" in hdr[i + 2] \
            and "Operating" in hdr[i + 3] and "Build" in hdr[i + 4], hdr[i:i + 5]
        years.append((y, i))
    out, skipped = [], 0
    for n, r in enumerate(rows, start=2):
        if r[1] is None:
            skipped += 1
            continue
        st = str(r[5] or "").strip()
        # "TSECL" (Tripura State Electricity Corporation) is printed in the state column for Gumti HPS, in Tripura
        base = dict(state_ut=STATE.get(st.upper(), "Tripura" if st == "TSECL" else ""), station=str(r[1]).strip(), unit_no=num(r[2]),
                    commissioned=r[3].strftime("%Y-%m-%d") if hasattr(r[3], "strftime") else num(r[3]),
                    capacity_mw_2026_03_31=num(r[4]), state_as_printed=st, sector=num(r[6]), owner=num(r[7]),
                    type=num(r[8]), fuel_1=num(r[9]), fuel_2=num(r[10]), serial_no=num(r[0]), source_row=n)
        for y, i in years:
            vals = [num(v) for v in r[i:i + 5]]
            if not any(vals):
                continue  # the unit has no entry for this year
            marks = [f"{m}:-" for m, x in zip(MEASURES, vals) if x == "-"]  # "-" printed instead of a number
            vals = ["" if x == "-" else x for x in vals]
            out.append(dict(base, year=y, **dict(zip(MEASURES, vals)), source_marks="; ".join(marks)))
    df = pd.DataFrame(out)
    cols = ["state_ut", "station", "unit_no", "year", "commissioned", "capacity_mw_2026_03_31", "state_as_printed",
            "sector", "owner", "type", "fuel_1", "fuel_2"] + MEASURES + ["serial_no", "source_row", "source_marks"]
    df = df[cols]
    print("blank rows skipped:", skipped)
    return df, [y for y, _ in years]


def factors():
    ws = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)["Results"]
    grid = [list(r) for r in ws.iter_rows(values_only=True)]
    recs = {}

    def take(row_i, label_col, year_cols, prefix):
        hdr_row = next(i for i in range(row_i, -1, -1) if grid[i][year_cols[0]] in ("2016-17",))
        ys = [grid[hdr_row][c] for c in year_cols]
        label = re.sub(r"\s+", " ", str(grid[row_i][label_col])).strip()
        for y, c in zip(ys, year_cols):
            recs.setdefault(y, {})[(prefix, label)] = num(grid[row_i][c])
    for i, r in enumerate(grid):
        if r[2] and i in range(12, 17):
            take(i, 2, list(range(5, 15)), "excl")
            take(i, 16, list(range(17, 27)), "incl")
        if r[2] and i in range(30, 41):
            take(i, 2, list(range(5, 15)), "gen")
            if r[16] and i in range(30, 35):
                take(i, 16, list(range(17, 27)), "em")
    names = {
        ("excl", "Weighted Average Emission Rate"): "weighted_avg_emission_rate_t_per_mwh",
        ("excl", "Weighted Average Grid Emission Rate (Incl. RES,Captive)"): "weighted_avg_grid_emission_rate_incl_re_captive_t_per_mwh",
        ("excl", "Simple Operating Margin (1)"): "simple_operating_margin_t_per_mwh",
        ("excl", "Build Margin"): "build_margin_t_per_mwh",
        ("excl", "Combined Margin (1)"): "combined_margin_t_per_mwh",
        ("incl", "Weighted Average Emission Rate (2)"): "weighted_avg_emission_rate_incl_imports_t_per_mwh",
        ("incl", "Weighted Average Grid Emission Rate (Incl. RES,Captive) (2)"): "weighted_avg_grid_emission_rate_incl_re_captive_incl_imports_t_per_mwh",
        ("incl", "Simple Operating Margin (1) (2)"): "simple_operating_margin_incl_imports_t_per_mwh",
        ("incl", "Build Margin (not adjusted for imports)"): "build_margin_not_adjusted_for_imports_t_per_mwh",
        ("incl", "Combined Margin (1) (2)"): "combined_margin_incl_imports_t_per_mwh",
        ("gen", "Gross Generation Total (GWh)"): "gross_generation_gwh",
        ("gen", "Net Generation Total (GWh)"): "net_generation_gwh",
        ("gen", "Share of Must-Run (Hydro/Nuclear) (% of Net Generation)"): "must_run_share_of_net_generation",
        ("gen", "Net Generation in Operating Margin (GWh)"): "net_generation_in_operating_margin_gwh",
        ("gen", "20% of Net Generation (GWh)"): "net_generation_20pct_gwh",
        ("gen", "Net Generation in Build Margin (GWh)"): "net_generation_in_build_margin_gwh",
        ("gen", "Net Renewable Generation (GWh)"): "net_renewable_generation_gwh",
        ("gen", "Net Import (GWh)"): "net_import_gwh",
        ("gen", "Captive power Injected into grid (GWh)"): "captive_injected_gwh",
        ("gen", "Thermal Captive power Injected into grid (GWh)"): "thermal_captive_injected_gwh",
        ("gen", "Total Net Generation (including Imports, RE and Captive) (GWh)"): "total_net_generation_incl_imports_re_captive_gwh",
        ("em", "Absolute CO2 Emissions Total (tCO2)"): "co2_emissions_total_t",
        ("em", "CO2 Emissions in Database (tCO2)"): "co2_emissions_in_database_t",
        ("em", "CO2 Emission by Captive (tCO2)"): "co2_emissions_captive_t",
        ("em", "Absolute Emissions OM (tCO2)"): "co2_emissions_operating_margin_t",
        ("em", "Absolute Emissions BM (tCO2)"): "co2_emissions_build_margin_t",
    }
    found = set(k for v in recs.values() for k in v)
    missing, extra = set(names) - found, found - set(names)
    if missing or extra:
        raise SystemExit(f"Results sheet labels changed: missing {missing}, unexpected {extra}")
    df = pd.DataFrame([dict(state_ut="All India", year=y, **{names[k]: v[k] for k in names}) for y, v in recs.items()])
    return df.sort_values("year")


def main():
    p, years = plants()
    for name, df in ((PLANTS, p), (FACTORS, factors())):
        Path(name).mkdir(exist_ok=True)
        df.to_csv(f"{name}/{name}.csv", index=False, lineterminator="\n")
        print(name, df.shape)


if __name__ == "__main__":
    main()
