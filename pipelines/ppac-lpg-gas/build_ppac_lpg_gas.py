"""PPAC (Petroleum Planning & Analysis Cell): LPG and city gas tables by state.

Reads  _sources/ppac-lpg-gas/raw/
       ppac-lpg-gas_lpg-profile-report_H1-FY2026-27.pdf  (LPG Profile Report H1 FY 2026-27, Nov 2026: Tables 2-12
                                                         and the distributor table printed as "Figure 40")
       ppac-lpg-gas_lpg-distributors_2026.xlsx           (state-wise LPG distributors of PSU OMCs, 2001 to 2026)
       ppac-lpg-gas_cgd-network_2026.xlsx                (PNG connections and CNG stations by PNGRB area group)
Writes one folder per table (TABLES below, plus distributors() and cgd()).
Run from the repo root:  .venv/bin/python pipelines/ppac-lpg-gas/build_ppac_lpg_gas.py
"""
import re
from pathlib import Path

import openpyxl
import pandas as pd
import pdfplumber

RAW = "_sources/ppac-lpg-gas/raw/"
PDF = RAW + "ppac-lpg-gas_lpg-profile-report_H1-FY2026-27.pdf"
NUM = r"-?\d[\d,]*(?:\.\d+)?"
STATES = """Andaman & Nicobar Islands|Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chandigarh|Chhattisgarh|Dadra & Nagar Haveli and Daman & Diu|Delhi|Goa|Gujarat|Haryana|Himachal Pradesh|Jammu & Kashmir|Jharkhand|Karnataka|Kerala|Ladakh|Lakshadweep|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Puducherry|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal|All India""".split("|")
CANON = {s.lower(): s for s in STATES}
CANON.update({"keralam": "Kerala", "dadra & nagar haveli & daman & diu": "Dadra & Nagar Haveli and Daman & Diu",
              "dadra & nagar haveli and daman & diu": "Dadra & Nagar Haveli and Daman & Diu",
              "dadra & nagar haveli": "Dadra & Nagar Haveli", "daman & diu": "Daman & Diu",
              "telangana-#": "Telangana", "telangana-": "Telangana", "chattisgarh": "Chhattisgarh",
              "chhattisgrah": "Chhattisgarh", "national capital territory of delhi (ut)": "Delhi",
              "ut of jammu and kashmir": "Jammu & Kashmir", "ut of jammu & kashmir": "Jammu & Kashmir",
              "dadra & nagar haveli (ut)": "Dadra & Nagar Haveli", "daman & diu (ut)": "Daman & Diu"})

# (table id as printed, folder, page, value columns, date, period)
TABLES = [
    ("Table 2", "ENG_lpg-bottling-plants_2026-10_STATES_PPAC", 10, ["bottling_plants_count", "bottling_capacity_tmtpa"], "2026-10-01", ""),
    ("Table 3", "ENG_lpg-tankage_2026-10_STATES_PPAC", 12, ["tankage_tmt"], "2026-10-01", ""),
    ("Figure 40", "ENG_lpg-distributors-by-category_2026-10_STATES_PPAC", 15,
     ["sheheri_vitrak_count", "rurban_vitrak_count", "gramin_vitrak_count", "durgam_kshetriya_vitrak_count", "total_count"], "2026-10-01", ""),
    ("Table 4", "ENG_lpg-domestic-sales_2026-04-to-2026-09_STATES_PPAC", 17, ["packed_domestic_sales_tmt"], "", "2026-04 to 2026-09"),
    ("Table 5", "ENG_auto-lpg-stations-sales_2026-04-to-2026-09_STATES_PPAC", 19, ["auto_lpg_stations_count", "auto_lpg_sales_t"], "2026-10-01", "2026-04 to 2026-09"),
    ("Table 6", "ENG_lpg-active-domestic-customers_2026-10_STATES_PPAC", 22, ["active_domestic_customers_lakh"], "2026-10-01", ""),
    ("Table 7", "ENG_lpg-new-enrolments_2026-04-to-2026-09_STATES_PPAC", 24, ["cylinder_14_2kg_lakh", "cylinder_5kg_lakh", "total_lakh"], "", "2026-04 to 2026-09"),
    ("Table 8", "ENG_lpg-dbc-enrolments_2026-04-to-2026-09_STATES_PPAC", 26, ["cylinder_14_2kg_lakh", "cylinder_5kg_lakh", "total_lakh"], "", "2026-04 to 2026-09"),
    ("Table 9", "ENG_lpg-non-domestic-customers_2026-10_STATES_PPAC", 28, ["non_domestic_customers_lakh"], "2026-10-01", ""),
    ("Table 10", "ENG_lpg-waiting-list_2026-10_STATES_PPAC", 30, ["waiting_list_count"], "2026-10-01", ""),
    ("Table 11", "ENG_lpg-scheme-beneficiaries_2026-10_STATES_PPAC", 32,
     ["state_govt_scheme_count", "oil_company_csr_count", "pmuy_count"], "2026-10-01", ""),
    ("Table 12", "ENG_pmuy-connections_2026-10_STATES_PPAC", 34, ["pmuy_connections_count"], "2026-10-01", ""),
]


def canon(s):
    s = re.sub(r"\s+", " ", s.replace(" and ", " & ")).strip(" *#")
    return CANON.get(s.lower(), "")


def region_or_state(label):
    if re.match(r"(?i)sub total", label):
        return ""
    return canon(label)


def report_table(pdf, tid, name, page, cols, date, period):
    text = pdf.pages[page - 1].extract_text()
    assert text.lstrip().startswith(tid), (tid, text[:80])
    lines = [l.strip() for l in text.split("\n")]
    row = re.compile(rf"^(.*?[A-Za-z&)\]*#\s])\s*((?:{NUM}\s+){{{len(cols) - 1}}}{NUM})$")
    start = next(i for i, l in enumerate(lines) if l.startswith("Chandigarh"))
    out = []
    for i in range(start, len(lines)):
        l = lines[i]
        m = row.match(l)
        if m:
            label = m.group(1).strip()
            vals = m.group(2).split()
            out.append([label, vals])
            if label.startswith("All India"):
                break
            continue
        if out and (out[-1][0].rstrip().endswith(("&", "and")) or l in ("DIU", "Diu", "Daman & Diu")):
            out[-1][0] = out[-1][0] + " " + l  # label wrapped onto the next line
            continue
        if not out or re.fullmatch(r"(Vitrak|\(Figures in MT\))", l):
            continue
        raise SystemExit(f"{tid}: line not understood: {l!r}")
    recs = []
    for label, vals in out:
        mark = re.findall(r"\*+|#", label)
        clean = re.sub(r"\s*(\*+|#)\s*$", "", label).strip()
        rec = dict(state_ut=region_or_state(clean), system=clean)
        if date:
            rec["date"] = date
        if period:
            rec["period"] = period
        rec.update({c: v.replace(",", "") for c, v in zip(cols, vals)})
        rec["source_marks"] = f"system:{''.join(mark)}" if mark else ""
        recs.append(rec)
    df = pd.DataFrame(recs)
    if not df.source_marks.any():
        df = df.drop(columns="source_marks")
    return save(df, name)


def save(df, name):
    Path(name).mkdir(exist_ok=True)
    df.to_csv(f"{name}/{name}.csv", index=False, lineterminator="\n")
    print(name, df.shape)
    return df


def distributors():
    ws = openpyxl.load_workbook(RAW + "ppac-lpg-gas_lpg-distributors_2026.xlsx", data_only=True)["Distributors "]
    g = [list(r) for r in ws.iter_rows(values_only=True)]
    hdr = g[6]
    assert str(hdr[0]).strip() == "State", hdr[:3]
    dates = []
    for v in hdr[1:]:
        s = str(v).strip()
        if re.fullmatch(r"\d{4}", s):
            dates.append((s, ""))
        elif re.fullmatch(r"01\.08\.2026 \(P\)", s):
            dates.append(("2026-08-01", "provisional"))
        else:
            raise SystemExit(f"distributors: header {s!r}")
    out = []
    for r in g[7:]:
        lab = str(r[0] or "").strip()
        if not lab or lab.startswith(("Source", "#")):
            continue
        for (d, flag), v in zip(dates, r[1:]):
            out.append(dict(state_ut=region_or_state(lab), system=lab, as_on=d,
                            distributors_count="" if v is None else str(v), source_flag=flag,
                            source_marks="system:#" if lab.endswith("#") else ""))
    df = pd.DataFrame(out)
    # blank cells: Ladakh before it became a UT (2019); none elsewhere
    blank = (df.distributors_count == "") & (df.source_flag == "")
    df.loc[blank & df.system.str.strip().eq("LADAKH"), "source_flag"] = "not_applicable"
    df.loc[blank & ~df.system.str.strip().eq("LADAKH"), "source_flag"] = "not_available"
    return save(df, "ENG_lpg-distributors_2001-to-2026_STATES_PPAC")


def cgd():
    wb = openpyxl.load_workbook(RAW + "ppac-lpg-gas_cgd-network_2026.xlsx", data_only=True)
    out = []
    for sheet in wb.sheetnames:
        g = [list(r) for r in wb[sheet].iter_rows(values_only=True)]
        title_row = next(r for r in g if any(isinstance(c, str) and "Status of PNG connections" in c for c in r))
        c0 = next(j for j, c in enumerate(title_row) if isinstance(c, str) and "Status of PNG" in c)
        title = title_row[c0]
        d = re.search(r"as on (\d\d)\.(\d\d)\.(\d{4})", str(title))
        assert d, title
        date = f"{d.group(3)}-{d.group(2)}-{d.group(1)}"
        for n, r in enumerate(g, start=1):
            lab = str(r[c0] or "").strip()
            if not lab or lab.startswith(("State/UT", "Note", "22.")) or not isinstance(r[c0 + 1], (int, float)):
                continue
            out.append(dict(state_ut="All India" if lab == "Grand Total" else canon(lab), area_group=lab, date=date,
                            cng_stations_count=r[c0 + 1], png_domestic_count=r[c0 + 2],
                            png_commercial_count=r[c0 + 3], png_industrial_count=r[c0 + 4], source_flag="provisional",
                            sheet=sheet.strip(), source_row=n))  # "Haryana" appears twice in the Jan 2025 sheet
    df = pd.DataFrame(out).sort_values(["date", "area_group"], key=lambda s: s.map(lambda v: (v == "Grand Total", v)))
    return save(df, "ENG_png-connections-cng-stations_2025-01-to-2026-07_STATES_PPAC")


def main():
    pdf = pdfplumber.open(PDF)
    for t in TABLES:
        report_table(pdf, *t)
    distributors()
    cgd()


if __name__ == "__main__":
    main()
