"""CEA India Fly Ash Year Book 2026 (data for FY 2025-26): plant-wise ash generation and utilisation.

Reads  _sources/cea-fly-ash/raw/cea-fly-ash_year-book_2026.pdf
Writes ENG_fly-ash-power-plants_FY2025-26_STATES_CEA  (Tables 5.1 to 5.17: one row per thermal power plant,
       17 states, with each state's "Grand Total" row)
Words are placed in columns by their x-position under the header; a plant's name or utility printed on two
lines is joined (lines are attached to the nearest row that has numbers).
Run from the repo root:  .venv/bin/python pipelines/cea-fly-ash/build_fly_ash.py
"""
import re
from pathlib import Path

import pandas as pd
import pdfplumber

PDF = "_sources/cea-fly-ash/raw/cea-fly-ash_year-book_2026.pdf"
NAME = "ENG_fly-ash-power-plants_FY2025-26_STATES_CEA"
COLS = ["s_no", "plant", "utility", "installed_capacity_mw", "state", "ash_generation_lmt", "ash_utilization_lmt",
        "ash_utilization_pct"]
HEAD = ["S.", "Plant", "Power", "Installed", "State", "Total", "Total", "Actual"]
NUM = re.compile(r"^-?\d[\d,]*\.?\d*$")


def lines_of(words):
    out = []
    for w in sorted(words, key=lambda w: (w["top"], w["x0"])):
        if out and abs(w["top"] - out[-1][0]["top"]) <= 2.5:
            out[-1].append(w)
        else:
            out.append([w])
    return [sorted(l, key=lambda w: w["x0"]) for l in out]


def parse_page(page):
    words = page.extract_words(x_tolerance=1.5)
    ls = lines_of(words)
    # header: the line holding "S." "Plant Name" "Power Utility" "Installed" "State" "Total" "Total" "Actual"
    hi = next(i for i, l in enumerate(ls) if [w["text"] for w in l][:1] == ["S."] and "Plant" in [w["text"] for w in l])
    hw = ls[hi]
    starts, k = [], 0
    for w in hw:
        if k < len(HEAD) and w["text"] == HEAD[k]:
            starts.append(w["x0"])
            k += 1
    if len(starts) != len(HEAD):
        raise SystemExit(f"page {page.page_number}: header not found ({[w['text'] for w in hw]})")
    # numbers are right-aligned under wide headers: column i spans from start[i] - 12 to start[i+1] - 12
    bounds = [s - 12 for s in starts[1:]]

    def col(w):
        x = w["x0"] if not NUM.match(w["text"]) else (w["x0"] + w["x1"]) / 2
        return sum(x >= b for b in bounds)
    body = [l for l in ls[hi + 1:] if not re.fullmatch(r"\(?(MW|LMT|%)\)?|Capacity|Generation|Utilization|\d{1,3}",
                                                          " ".join(w["text"] for w in l)) or any(col(w) >= 5 for w in l)]
    # rows anchored on lines with the ash generation figure (column 5)
    anchors, rest = [], []
    for l in body:
        if any(col(w) == 5 and NUM.match(w["text"]) for w in l):
            anchors.append(l)
        else:
            rest.append(l)
    rows = [[w for w in a] for a in anchors]
    tops = [a[0]["top"] for a in anchors]
    for l in rest:
        t = l[0]["top"]
        if t > tops[-1] + 20 or t < tops[0] - 20:
            continue  # page number or notes
        j = min(range(len(tops)), key=lambda i: abs(tops[i] - t))
        rows[j] += l
    recs = []
    for r in rows:
        r = [w for w in r if not re.fullmatch(r"\((MW|LMT|%)\)", w["text"])]  # header units under the header line
        allt = " ".join(w["text"] for w in sorted(r, key=lambda w: (round(w["top"]), w["x0"])))
        if "Grand" in allt and "Total" in allt:
            nums = [w["text"] for w in sorted(r, key=lambda w: w["x0"]) if NUM.match(w["text"])]
            if len(nums) != 3:
                raise SystemExit(f"page {page.page_number}: Grand Total row {allt!r}")
            recs.append(dict(zip(COLS, ["", "Grand Total", "", "", ""] + nums)))
            continue
        # right part (from the Installed Capacity column): capacity, state words, generation, utilisation, %
        right = sorted([w for w in r if w["x0"] >= bounds[2] - 5 or (NUM.match(w["text"]) and col(w) >= 3)],
                       key=lambda w: (w["x0"], w["top"]))
        nums = [w["text"] for w in right if NUM.match(w["text"])]
        state = " ".join(w["text"] for w in sorted(right, key=lambda w: (round(w["top"]), w["x0"])) if not NUM.match(w["text"]))
        if len(nums) != 4:
            raise SystemExit(f"page {page.page_number}: {len(nums)} numbers in {allt!r}")
        left = [w for w in r if w not in right]
        cells = [[], [], []]
        for w in sorted(left, key=lambda w: (round(w["top"]), w["x0"])):
            if re.fullmatch(r"\d{1,3}", w["text"]) and w["x0"] < bounds[0] + 15:
                cells[0].append(w["text"])  # serial number
            else:  # plant names sometimes start left of the "Plant Name" header: split only plant / utility
                cells[1 if w["x0"] < bounds[1] else 2].append(w["text"])
        txt = []
        for c in cells:
            s_ = ""
            for part in c:
                s_ = s_[:-1] + part if s_.endswith("-") and s_[-2:-1].isalpha() else (s_ + " " + part).strip()
            txt.append(s_)
        recs.append(dict(zip(COLS, txt + [nums[0], state] + nums[1:])))
    return recs


def main():
    pdf = pdfplumber.open(PDF)
    pages = [p for p in pdf.pages if re.search(r"Table 5\.\d+ Ash Generation and Utilization Data of", p.extract_text() or "")]
    out = []
    for p in pages:
        t = p.extract_text()
        m = re.search(r"Table (5\.\d+) Ash Generation and Utilization Data of (.+?) for the FY (\d{4}-\d\d)", t)
        recs = parse_page(p)
        for r in recs:
            r.update(table=m.group(1), table_state=m.group(2).strip(), year=m.group(3))
        print(p.page_number, m.group(1), m.group(2), len(recs), "rows")
        out += recs
    df = pd.DataFrame(out)
    df["state_ut"] = df.table_state
    df = df[["state_ut", "plant", "year", "s_no", "utility", "installed_capacity_mw", "state", "ash_generation_lmt",
             "ash_utilization_lmt", "ash_utilization_pct", "table"]]
    df = df.rename(columns={"state": "state_as_printed"})
    Path(NAME).mkdir(exist_ok=True)
    df.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, df.shape)
    return df


if __name__ == "__main__":
    main()
