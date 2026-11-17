"""Ministry of Coal (Coal Controller's Organisation), Coal Directory of India 2024-25: state-wise tables.

Reads  _sources/moc-coal-directory/raw/moc-coal-directory_chapter-NN_2024-25.xlsx (the Ministry's own Excel files)
Writes one folder per table (see the calls in main()).
Only quantities and amounts are kept; "Share (%)" and "Growth (%)" columns are left out (they are computed
from the quantities kept here). Blank cells are kept blank (the source leaves them empty, usually meaning nil).
Run from the repo root:  .venv/bin/python pipelines/moc-coal-directory/build_coal_directory.py
"""
import re
from decimal import Decimal
from pathlib import Path

import openpyxl
import pandas as pd

RAW = "_sources/moc-coal-directory/raw/moc-coal-directory_chapter-{:02d}_2024-25.xlsx"
STATES = set("""Andaman & Nicobar Islands|Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chandigarh|Chhattisgarh|Dadra & Nagar Haveli and Daman & Diu|Delhi|Goa|Gujarat|Haryana|Himachal Pradesh|Jammu & Kashmir|Jharkhand|Karnataka|Kerala|Ladakh|Lakshadweep|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Puducherry|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal|All India""".split("|"))
ALIAS = {"J & K": "Jammu & Kashmir", "J&K": "Jammu & Kashmir", "Tamilnadu": "Tamil Nadu", "Orissa": "Odisha",
         "Chattisgarh": "Chhattisgarh", "Pondicherry": "Puducherry", "Dadra & Nagar Haveli": "Dadra & Nagar Haveli",
         "Daman & Diu": "Daman & Diu", "Andaman & Nicobar": "Andaman & Nicobar Islands", "Uttaranchal": "Uttarakhand",
         "Total": "All India", "All India": "All India", "Grand Total": "All India"}


def clean(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()


def state(s):
    s = clean(s)
    s = ALIAS.get(s, s)
    return s if s in STATES or s in ("Dadra & Nagar Haveli", "Daman & Diu") else ""


def plain(x):
    """12 significant digits (drops binary noise such as 8652.237000000001) written without an exponent."""
    s = f"{x:.12g}"
    return format(Decimal(s), "f") if "e" in s else s


def num(x):
    if x is None or (isinstance(x, str) and not x.strip()):
        return ""
    if isinstance(x, float):
        return plain(x)
    if isinstance(x, int):
        return str(x)
    return clean(x)


def grid(ch, sheet):
    ws = openpyxl.load_workbook(RAW.format(ch), data_only=True)[sheet]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def save(df, name):
    bad = [c for c in df.columns if c.endswith(("_mt", "_inr_crore", "_count", "_000_t", "_inr_million", "_usd_million"))
           and df[c].map(lambda v: v != "" and not re.fullmatch(r"-?\d+(\.\d+)?(e-?\d+)?", str(v))).any()]
    if bad:
        raise SystemExit(f"{name}: non-numeric values in {bad}")
    Path(name).mkdir(exist_ok=True)
    df.to_csv(f"{name}/{name}.csv", index=False, lineterminator="\n")
    print(name, df.shape)
    return df


def year_panels(g, measure, first_year=None):
    """Tables 3.9, 3.10, 4.7: blocks of 'Year | <State> (Quantity, Share, Growth) x 3' stacked down the sheet."""
    out = []
    for i, r in enumerate(g):
        if clean(r[0]) != "Year":
            continue
        heads = [(j, clean(v)) for j, v in enumerate(r) if j > 0 and j < 10 and clean(v)]
        for k in range(i + 1, len(g)):
            y = clean(g[k][0])
            if clean(g[k][0]) == "Year" or (not y and not any(g[k][1:10])):
                if k > i + 3:
                    break
                continue
            if not re.fullmatch(r"\d{4}-\d\d", y) or (first_year and y < first_year):
                continue
            for j, name in heads:
                out.append(dict(state_as_printed=name, year=y, **{measure: num(g[k][j])}))
    df = pd.DataFrame(out)
    df.insert(0, "state_ut", df.state_as_printed.map(state))
    order = list(dict.fromkeys(df.state_ut))
    order = [s for s in order if s != "All India"] + ["All India"]
    return df.assign(_o=df.state_ut.map(order.index)).sort_values(["_o", "year"]).drop(columns="_o")[
        ["state_ut", "year", measure, "state_as_printed"]]


def coal_resources():
    """Table 2.2: state-wise inventory of geological resources of coal, Gondwana and Tertiary panels."""
    g = grid(1, "2.2")
    out = []
    for panel, c0, typ in ((0, 0, "Gondwana"), (1, 6, "Tertiary")):
        cur = ""
        for r in g[6:]:
            lab = clean(r[c0])
            if lab and not re.match(r"\d", lab) and lab not in ("Gondawana Coalfields", "Tertiary Coalfields"):
                cur = lab
            d = clean(r[c0 + 1])
            if not d or not cur:
                continue
            m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", d)
            if not m:
                raise SystemExit(f"table 2.2: date {d!r}")
            out.append(dict(state_as_printed=cur, coalfield_type=typ,
                            date=f"{m.group(3)}-{int(m.group(2)):02d}-{int(m.group(1)):02d}",
                            proved_mt=num(r[c0 + 2]), indicated_mt=num(r[c0 + 3]), inferred_mt=num(r[c0 + 4]),
                            total_mt=num(r[c0 + 5])))
    df = pd.DataFrame(out)
    df.insert(0, "state_ut", df.state_as_printed.map(state))
    df.loc[df.state_as_printed.isin(["Total Gondwana", "Total Tertiary", "Total\nTertiary"]) |
           df.state_as_printed.str.startswith("Total"), "state_ut"] = ""
    df.loc[df.state_as_printed == "All India", "state_ut"] = "All India"
    df = df[["state_ut", "coalfield_type", "date", "proved_mt", "indicated_mt", "inferred_mt", "total_mt",
             "state_as_printed"]]
    return save(df, "ENG_coal-resources_2005-to-2025_STATES_MOC")


def mine_type_production():
    """Table 3.25: state-wise production of raw coal by type of mine (open cast / underground)."""
    g = grid(2, "PT25")
    years = {j: clean(v) for j, v in enumerate(g[2]) if re.fullmatch(r"\d{4}-\d\d", clean(v))}
    out = []
    for r in g[5:]:
        if not clean(r[0]):
            continue
        for j, y in years.items():
            out.append(dict(state_as_printed=clean(r[0]), year=y, open_cast_mt=num(r[j]), underground_mt=num(r[j + 1]),
                            total_mt=num(r[j + 2])))
    df = pd.DataFrame(out)
    df.insert(0, "state_ut", df.state_as_printed.map(state))
    df = df.sort_values(["state_ut", "year"], key=lambda s: s.map(lambda v: (v == "All India", v)))
    return save(df[["state_ut", "year", "open_cast_mt", "underground_mt", "total_mt", "state_as_printed"]],
                "ENG_coal-production-by-mine-type_2021-22-to-2024-25_STATES_MOC")


def despatch_by_mode():
    """Table 4.18: mode-wise despatch of raw coal, All India, last ten years (quantity rows only)."""
    g = grid(3, "dt18")
    modes = ["rail", "road", "belt", "rope", "mgr", "other", "total"]
    out = []
    for r in g[5:]:
        if clean(r[1]) != "Quantity":
            continue
        rec = dict(state_ut="All India", year=clean(r[0]))
        rec.update({f"external_{m}_mt": num(r[2 + i]) for i, m in enumerate(modes)})
        rec.update({f"internal_{m}_mt": num(r[9 + i]) for i, m in enumerate(modes)})
        rec["grand_total_mt"] = num(r[16])
        out.append(rec)
    return save(pd.DataFrame(out), "ENG_coal-despatch-by-mode_2015-16-to-2024-25_IN_MOC")


def offtake_by_sector():
    """Table 4.20: company-wise off-take of raw coal to priority sectors, 2024-25."""
    g = grid(3, "dt20")
    hdr = [clean(v) for v in g[2]]
    cols = ["power_utility_mt", "power_captive_mt", "direct_feed_mt", "steel_coke_oven_cokeries_mt", "steel_boilers_mt",
            "cement_mt", "fertilisers_mt", "sponge_iron_mt", "other_basic_metal_mt", "chemical_mt", "pulp_paper_mt",
            "textiles_rayons_mt", "bricks_mt", "other_mt", "total_despatch_mt", "colliery_own_consumption_mt",
            "colliery_staff_mt", "total_offtake_mt"]
    assert hdr[1].startswith("Power (Utility)") and hdr[18].startswith("Total Offtake") and len(hdr) >= 19, hdr
    out = []
    for r in g[4:]:
        c = clean(r[0])
        if not c or c.startswith("("):
            continue
        out.append(dict(state_ut="All India", company=c, year="2024-25", **{k: num(r[1 + i]) for i, k in enumerate(cols)}))
    return save(pd.DataFrame(out), "ENG_coal-offtake-by-sector_FY2024-25_IN_MOC")


def source_destination():
    """Table 4.21: raw coal despatch from source state to destination state, 2024-25 (matrix to long)."""
    g = grid(3, "dt21")
    src = {j: clean(v) for j, v in enumerate(g[3]) if j >= 1 and clean(v)}
    out = []
    for r in g[5:]:
        dest = clean(r[0])
        if not dest:
            continue
        for j, s in src.items():
            v = num(r[j])
            if v == "":
                continue  # blank cell: no despatch from that state
            out.append(dict(destination_as_printed=dest, source_state_as_printed=s, year="2024-25", despatch_mt=v))
    df = pd.DataFrame(out)
    df.insert(0, "state_ut", df.destination_as_printed.map(state))
    df.insert(1, "source_state", df.source_state_as_printed.map(lambda s: "All India" if s == "Total" else state(s)))
    return save(df[["state_ut", "source_state", "year", "despatch_mt", "destination_as_printed", "source_state_as_printed"]],
                "ENG_coal-despatch-source-destination_FY2024-25_STATES_MOC")


def royalty_taxes():
    """Table 7.2: state-wise payment of royalty, DMF, NMET and other taxes, 2024-25 (coal), Rs crore."""
    g = grid(6, "tb7.2&3")
    cols = ["royalty_inr_crore", "dmf_inr_crore", "nmet_inr_crore", "cgst_inr_crore", "sgst_inr_crore", "igst_inr_crore",
            "cess_on_coal_inr_crore", "entry_tax_inr_crore", "corporate_income_tax_inr_crore", "dividend_inr_crore",
            "total_inr_crore"]
    hdr = [clean(v) for v in g[2]]
    assert hdr[2] == "Amount of Royalty Paid" and hdr[12] == "Total", hdr
    out = []
    for r in g[4:]:
        name = clean(r[1])
        if name.startswith("Table 7.3"):
            break
        if not name or name.startswith("("):
            continue
        out.append(dict(state_as_printed=name, year="2024-25", **{k: num(r[2 + i]) for i, k in enumerate(cols)}))
    df = pd.DataFrame(out)
    df.insert(0, "state_ut", df.state_as_printed.map(state))
    return save(df[["state_ut", "year"] + cols + ["state_as_printed"]], "ENG_coal-royalty-dmf-taxes_FY2024-25_STATES_MOC")


def royalty_3yr():
    """Table 7.7: state-wise royalty, DMF and NMET paid, CIL and non-CIL, 2022-23 to 2024-25, Rs crore."""
    g = grid(6, "tb7.7")
    years = [clean(v) for v in g[3][2:5]]
    out, cur = [], ""
    for r in g[5:]:
        if clean(r[0]):
            cur = clean(r[0])
        typ = clean(r[1])
        if not typ:
            continue
        for i, y in enumerate(years):
            out.append(dict(state_as_printed=cur, company_type=typ, year=y, royalty_inr_crore=num(r[2 + i]),
                            dmf_inr_crore=num(r[5 + i]), nmet_inr_crore=num(r[8 + i])))
    df = pd.DataFrame(out)
    df.insert(0, "state_ut", df.state_as_printed.map(state))
    return save(df[["state_ut", "company_type", "year", "royalty_inr_crore", "dmf_inr_crore", "nmet_inr_crore",
                    "state_as_printed"]], "ENG_coal-royalty-dmf-nmet_2022-23-to-2024-25_STATES_MOC")


def mines():
    """Table 12.2: state-wise number of coal and lignite mines (producing, non-producing, operational) on 31.03.2025."""
    g = grid(11, "tab12.2")
    out, fuel = [], ""
    groups = ["producing", "non_producing", "operational"]
    kinds = ["open_cast", "underground", "mixed", "total"]
    for r in g[4:]:
        if clean(r[0]):
            fuel = clean(r[0])
        if not clean(r[1]):
            continue
        rec = dict(state_as_printed=clean(r[1]), mineral=fuel.lower(), date="2025-03-31")
        for gi, gname in enumerate(groups):
            for ki, k in enumerate(kinds):
                rec[f"{gname}_{k}_count"] = num(r[2 + gi * 4 + ki])
        out.append(rec)
    df = pd.DataFrame(out)
    df.insert(0, "state_ut", df.state_as_printed.map(state))
    cols = ["state_ut", "mineral", "date"] + [c for c in df.columns if c.endswith("_count")] + ["state_as_printed"]
    return save(df[cols], "ENG_coal-lignite-mines_2025-03_STATES_MOC")


def port_imports():
    """Table 8.5: port-wise import of coal, coke and other coal products, 2024-25."""
    g = grid(7, "TB8.5")
    groups = ["coking_coal", "non_coking_coal", "total_coal", "coke_coal_products"]
    out = []
    for r in g[5:]:
        p = clean(r[0])
        if not p:
            continue
        rec = dict(state_ut="All India", port="Total" if p == "Total" else p, year="2024-25")
        for i, gname in enumerate(groups):
            rec[f"{gname}_mt"] = num(r[1 + 3 * i])
            rec[f"{gname}_inr_million"] = num(r[2 + 3 * i])
            rec[f"{gname}_usd_million"] = num(r[3 + 3 * i])
        out.append(rec)
    return save(pd.DataFrame(out), "ENG_coal-imports-by-port_FY2024-25_IN_MOC")


def main():
    coal_resources()
    save(year_panels(grid(2, "PT9"), "production_mt"), "ENG_coal-production_2015-16-to-2024-25_STATES_MOC")
    save(year_panels(grid(2, "PT10"), "production_mt"), "ENG_lignite-production_2015-16-to-2024-25_STATES_MOC")
    mine_type_production()
    # the last block of Table 4.7 also carries 1993-94 to 2013-14 for UP and West Bengal only, with "#REF!"
    # (broken formulas) for All India: only the table's own ten-year span is kept
    save(year_panels(grid(3, "dt7"), "despatch_mt", "2014-15"), "ENG_coal-despatch_2014-15-to-2024-25_STATES_MOC")
    despatch_by_mode()
    offtake_by_sector()
    source_destination()
    royalty_taxes()
    royalty_3yr()
    mines()
    port_imports()


if __name__ == "__main__":
    main()
