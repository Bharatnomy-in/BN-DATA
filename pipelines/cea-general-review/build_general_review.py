"""CEA General Review 2025 (All India Electricity Statistics, data for 2023-24): state-wise tables.

Reads  _sources/cea-general-review/raw/cea-general-review_all-india-electricity-statistics_2025.pdf
Writes one folder per table (see TABLES below).
Numbers are placed by their x-position under the column of the table's total row, so blank cells stay blank.
Run from the repo root:  .venv/bin/python pipelines/cea-general-review/build_general_review.py
"""
import re
from pathlib import Path

import pandas as pd
import pdfplumber

PDF = "_sources/cea-general-review/raw/cea-general-review_all-india-electricity-statistics_2025.pdf"
NUM = re.compile(r"^-?[\d,]*\.?\d+$")

STATE = {
    "andaman & nicobar": "Andaman & Nicobar Islands", "andaman- nicobar": "Andaman & Nicobar Islands",
    "a&n island": "Andaman & Nicobar Islands", "a & n islands": "Andaman & Nicobar Islands",
    "a.& n. islands": "Andaman & Nicobar Islands", "andhra pradesh": "Andhra Pradesh",
    "arunachal pradesh": "Arunachal Pradesh", "assam": "Assam", "bihar": "Bihar", "chandigarh": "Chandigarh",
    "chandigrah": "Chandigarh", "chhattisgarh": "Chhattisgarh", "chattisgarh": "Chhattisgarh",
    "chhatisgarh": "Chhattisgarh", "chhattisgrah": "Chhattisgarh", "delhi": "Delhi", "goa": "Goa",
    "gujarat": "Gujarat", "haryana": "Haryana", "himachal pradesh": "Himachal Pradesh", "himachal": "Himachal Pradesh",
    "jammu & kashmir": "Jammu & Kashmir", "jharkhand": "Jharkhand", "karnataka": "Karnataka", "kerala": "Kerala",
    "ladakh": "Ladakh", "lakshadweep": "Lakshadweep", "lakshwadeep": "Lakshadweep",
    "madhya pradesh": "Madhya Pradesh", "madhay pradesh": "Madhya Pradesh", "maharashtra": "Maharashtra",
    "maharastra": "Maharashtra", "manipur": "Manipur", "meghalaya": "Meghalaya", "mizoram": "Mizoram",
    "nagaland": "Nagaland", "odisha": "Odisha", "orissa": "Odisha", "puducherry": "Puducherry",
    "pondicherry": "Puducherry", "punjab": "Punjab", "rajasthan": "Rajasthan", "sikkim": "Sikkim",
    "tamil nadu": "Tamil Nadu", "tamilnadu": "Tamil Nadu", "telangana": "Telangana", "tripura": "Tripura",
    "uttar pradesh": "Uttar Pradesh", "uttarakhand": "Uttarakhand", "west bengal": "West Bengal",
    "dnh & dd": "Dadra & Nagar Haveli and Daman & Diu",
    "dadra & nagar haveli & daman & diu": "Dadra & Nagar Haveli and Daman & Diu",
    "daman & diu & dadra & nagar haveli": "Dadra & Nagar Haveli and Daman & Diu",
    "daman & diu and dadra & nagar haveli": "Dadra & Nagar Haveli and Daman & Diu",
    "dadar & nagar haveli": "Dadra & Nagar Haveli", "dadra & nagar haveli": "Dadra & Nagar Haveli",
    "daman & diu": "Daman & Diu", "d. & n. haveli": "Dadra & Nagar Haveli",
    "total (all india)": "All India", "total(all india)": "All India", "all india": "All India",
    "total (mw)": "All India",
}


def state_of(system):
    s = re.sub(r"\s+", " ", system.lower().replace(" and ", " & ")).strip(" *$#")
    s = s.replace("ut of ", "")
    return STATE.get(s, "")


def lines_of(page):
    """Words grouped into text lines (by top, within 2 pt), left to right."""
    ws = sorted(page.extract_words(x_tolerance=1.5, keep_blank_chars=False), key=lambda w: (round(w["top"]), w["x0"]))
    out, cur, top = [], [], None
    for w in ws:
        if top is None or abs(w["top"] - top) > 2.5:
            if cur:
                out.append(sorted(cur, key=lambda w: w["x0"]))
            cur, top = [w], w["top"]
        else:
            cur.append(w)
    if cur:
        out.append(sorted(cur, key=lambda w: w["x0"]))
    return out


def fix_interleaved(words):
    """'Lad1a8k2h486' (a label with a number printed into it) -> label word + number word.
    '76589*8' (a footnote star printed inside a number) -> number '765898' with mark '*'."""
    out = []
    for w in words:
        t = w["text"]
        if re.fullmatch(r"[\d.,]+\*[\d.,]*|\*[\d.,]+", t):
            out.append(dict(w, text=t.replace("*", ""), mark="*"))
            continue
        if re.search(r"[A-Za-z]", t) and re.search(r"\d", t) and not NUM.match(t) and not re.match(r"^\(?\d", t):
            letters = "".join(c for c in t if not c.isdigit())
            digits = "".join(c for c in t if c.isdigit())
            if len(digits) >= 3 and letters.isalpha():
                out.append(dict(w, text=letters, x1=w["x0"] + 1))
                out.append(dict(w, text=digits, x0=w["x1"] - 1))
                continue
        out.append(w)
    return out


def parse_pages(pages, ncols, label_xmax, start, stop=r"^(Note|Source|\*|\(\*|\$)"):
    """Rows of (label, {col index: value}) for the given pages.

    Column positions come from the right edges of the numbers on the first row that has all ncols numbers.
    start: regex the first data label must match (rows above it are headers)."""
    rows = []
    for page in pages:
        ls = [fix_interleaved(l) for l in lines_of(page)]
        # column right edges from the fullest row
        ref = None
        i0 = next((i for i, l in enumerate(ls) if re.search(start, " ".join(w["text"] for w in l))), None)
        if i0 is None:
            raise SystemExit(f"page {page.page_number}: no line matches {start!r}")
        for l in ls[i0:]:
            nums = [w for w in l if NUM.match(w["text"]) and w["x0"] > label_xmax]
            if len(nums) == ncols:
                ref = [w["x1"] for w in nums]
                break
        if ref is None:
            raise SystemExit(f"page {page.page_number}: no row with {ncols} numbers")
        started = False
        pending = ""
        for l in ls:
            label = " ".join(w["text"] for w in l if not NUM.match(w["text"]) or w["x1"] <= label_xmax)
            nums = [w for w in l if NUM.match(w["text"]) and w["x1"] > label_xmax]
            if not started:
                if re.search(start, label):
                    started = True
                else:
                    continue
            if re.search(stop, label):
                break
            if not nums:
                if label:
                    pending = (pending + " " + label).strip()
                continue
            vals, marks = {}, {}
            for w in nums:
                k = min(range(ncols), key=lambda i: abs(ref[i] - w["x1"]))
                if abs(ref[k] - w["x1"]) > 14:
                    raise SystemExit(f"page {page.page_number}: {w['text']} at x1={w['x1']:.0f} not under a column ({label!r})")
                if k in vals:
                    raise SystemExit(f"page {page.page_number}: two numbers in column {k} ({label!r})")
                vals[k] = w["text"].replace(",", "")
                if w.get("mark"):
                    marks[k] = w["mark"]
            label = (pending + " " + label).strip() if pending and not label else label
            pending = ""
            rows.append([label, vals, round(l[0]["top"]), marks])
            if state_of(label) == "All India":
                break  # anything below the total row is a note
    return rows


def frame(rows, cols, numbered=False):
    recs = []
    for label, vals, _, marks in rows:
        if numbered:
            label = re.sub(r"^\d+\s+", "", label)
        recs.append(dict(system=label, **{c: vals.get(i, "") for i, c in enumerate(cols)},
                         source_marks="; ".join(f"{cols[k]}:{m}" for k, m in sorted(marks.items()))))
    df = pd.DataFrame(recs)
    if not df.source_marks.any():
        df = df.drop(columns="source_marks")
    df.insert(0, "state_ut", df.system.map(state_of))
    return df


def save(df, name, year=None):
    if year:
        df.insert(2, "year", year)
    Path(name).mkdir(exist_ok=True)
    df.to_csv(f"{name}/{name}.csv", index=False, lineterminator="\n")
    print(name, df.shape)
    return df


def side_by_side(parts, key="system"):
    """Join the column blocks of a table printed over several pages (same rows in the same order)."""
    base = parts[0]
    for p in parts[1:]:
        a, b = list(base[key]), list(p[key])
        # the merged UT is printed "DNH & DD" on one page and "Daman & Diu" on the next (same row, Table 9.7)
        bad = [(x, y) for x, y in zip(a, b) if state_of(x) != state_of(y) and (x, y) != ("DNH & DD", "Daman & Diu")]
        if bad or len(a) != len(b):
            raise SystemExit(f"row labels differ between pages: {bad[:5]} {len(a)} {len(b)}")
        if "source_marks" in p and "source_marks" in base:
            base["source_marks"] = ["; ".join(x for x in ab if x) for ab in zip(base.source_marks, p.source_marks)]
            p = p.drop(columns="source_marks")
        base = pd.concat([base, p.drop(columns=["state_ut", key])], axis=1)
        if "source_marks" in base:
            base = base[[c for c in base.columns if c != "source_marks"] + ["source_marks"]]
    return base


def main():
    pdf = pdfplumber.open(PDF)
    P = lambda *ns: [pdf.pages[n - 1] for n in ns]
    out = {}

    # Table 1.7 Growth of total electricity consumption by ultimate consumers, state-wise, utilities (GWh), 2012-13 to 2023-24
    years = ["2012-13", "2013-14", "2014-15", "2015-16", "2016-17", "2017-18", "2018-19", "2019-20", "2020-21",
             "2021-22", "2022-23", "2023-24"]
    rows = parse_pages(P(32), 12, 130, r"^Chandigarh")
    fixed = []
    for label, vals, top, _ in rows:
        # unlabeled rows (labels not printed in the PDF): see README
        if not label and top == 261:
            label = "Daman & Diu"
        elif not label and top == 269:
            label = "Dadra & Nagar Haveli"
        elif label == "Daman & Diu" and set(vals) == {10, 11}:
            label = "Dadra & Nagar Haveli and Daman & Diu"
        elif not label and set(vals) == {0, 1}:
            label = "Andhra Pradesh (undivided)"
        elif not label:
            raise SystemExit(f"table 1.7: unlabeled row at {top}: {vals}")
        fixed.append([label, vals, top, {}])
    long = []
    for label, vals, top, _ in fixed:
        for i, y in enumerate(years):
            if i in vals:
                long.append(dict(system=label, year=y, consumption_gwh=vals[i]))
    df = pd.DataFrame(long)
    df.insert(0, "state_ut", df.system.map(state_of))
    df.loc[df.system == "Andhra Pradesh (undivided)", "state_ut"] = ""
    order = list(dict.fromkeys(df.system))
    df = df.assign(_o=df.system.map(order.index)).sort_values(["_o", "year"]).drop(columns="_o")
    out["t1_7"] = save(df.reset_index(drop=True), "ENG_electricity-consumption_2012-13-to-2023-24_STATES_CEA")

    # Table 3.11 State-wise installed capacity of renewable power, 31.03.2024 (MW); source MNRE
    cols = ["small_hydro_mw", "wind_mw", "bio_power_bagasse_cogen_mw", "bio_power_non_bagasse_cogen_mw",
            "waste_to_energy_mw", "waste_to_energy_offgrid_mw", "bio_power_total_mw", "solar_mw", "total_re_mw"]
    df = frame(parse_pages(P(66), 9, 175, r"^1 Andhra"), cols, numbered=True)
    df.insert(2, "date", "2024-03-31")
    out["t3_11"] = save(df, "ENG_renewable-capacity_2024-03_STATES_CEA")

    # Table 6.4 State-wise system (T&D) losses, 2023-24
    cols = ["own_ipp_exbus_generation_gwh", "exbus_import_from_grid_gwh", "exbus_import_from_cpp_gwh",
            "availability_exbus_gwh", "total_consumption_gwh", "td_losses_gwh", "td_losses_pct", "td_losses_2022_23_pct"]
    out["t6_4"] = save(frame(parse_pages(P(106), 8, 135, r"^Chandigrah"), cols), "ENG_td-losses_FY2023-24_STATES_CEA", "2023-24")

    # Table 7.1 Fossil fuel consumption for electricity generation in thermal stations, state-wise, 2023-24
    cols = ["coal_000_t", "furnace_oil_kl", "light_diesel_oil_hsd_kl", "lshs_hhs_kl", "gas_mmscm", "biomass_t",
            "lignite_000_t", "generation_coal_lignite_plants_gwh"]
    out["t7_1"] = save(frame(parse_pages(P(116), 8, 140, r"^Delhi"), cols), "ENG_power-plant-fuel-use_FY2023-24_STATES_CEA", "2023-24")

    # Table 9.3 Electrical energy sales to ultimate consumers, category-wise / state-wise, utilities, 2023-24 (GWh)
    a = frame(parse_pages(P(139), 5, 130, r"^Chandigarh"),
              ["domestic_gwh", "commercial_gwh", "industrial_lv_mv_gwh", "industrial_hv_gwh", "public_lighting_gwh"])
    b = frame(parse_pages(P(140), 5, 130, r"^Chandigarh"),
              ["public_water_works_gwh", "traction_gwh", "agriculture_gwh", "miscellaneous_gwh", "total_sold_gwh"])
    out["t9_3"] = save(side_by_side([a, b]), "ENG_electricity-sales-by-category_FY2023-24_STATES_CEA", "2023-24")

    # Table 9.7 Per capita ultimate consumption, state-wise / category-wise, utilities, 2023-24 (kWh)
    pr = [pdf.pages[150], pdf.pages[151]]
    a = frame(parse_pages(pr[:1], 5, 130, r"^Chandigarh"),
              ["population_million", "domestic_kwh", "commercial_kwh", "industrial_lv_mv_kwh", "industrial_hv_kwh"])
    b = frame(parse_pages(pr[1:], 6, 130, r"^Chandigarh"),
              ["public_lighting_kwh", "traction_kwh", "agriculture_kwh", "public_water_works_kwh", "miscellaneous_kwh",
               "total_kwh"])
    out["t9_7"] = save(side_by_side([a, b]), "ENG_per-capita-consumption-by-category_FY2023-24_STATES_CEA", "2023-24")
    # Table 9.9 Annual per capita consumption (utilities + non-utilities), 2023-24
    a = frame(parse_pages(P(154), 5, 130, r"^Chandigarh"),
              ["population_000", "net_generation_and_drawal_gwh", "aux_consumption_own_generation_gwh",
               "aux_consumption_for_regional_drawal_gwh", "total_aux_consumption_gwh"])
    b = frame(parse_pages(P(155), 4, 130, r"^Chandigarh"),
              ["gross_generation_and_drawal_gwh", "captive_consumption_from_self_generation_gwh",
               "gross_consumption_gwh", "per_capita_consumption_kwh"])
    out["t9_9"] = save(side_by_side([a, b]), "ENG_per-capita-consumption_FY2023-24_STATES_CEA", "2023-24")

    # Table 10 Consumers and connected load, region-wise / state-wise, utilities, 31.03.2024
    a = frame(parse_pages(P(159), 6, 130, r"^Chandigarh"),
              ["domestic_load_kw", "domestic_consumers", "commercial_load_kw", "commercial_consumers",
               "industrial_lv_mv_load_kw", "industrial_lv_mv_consumers"])
    b = frame(parse_pages(P(160), 6, 140, r"^Chandigarh"),
              ["industrial_hv_load_kw", "industrial_hv_consumers", "public_lighting_load_kw", "public_lighting_consumers",
               "traction_load_kw", "traction_consumers"])
    c = frame(parse_pages(P(161), 8, 140, r"^Chandigarh"),
              ["agriculture_load_kw", "agriculture_consumers", "public_water_works_load_kw", "public_water_works_consumers",
               "miscellaneous_load_kw", "miscellaneous_consumers", "total_load_kw", "total_consumers"])
    df = side_by_side([a, b, c])
    df.insert(2, "date", "2024-03-31")
    out["t10"] = save(df, "ENG_consumers-connected-load_2024-03_STATES_CEA")
    return out


if __name__ == "__main__":
    main()
