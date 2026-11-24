"""ODF Plus village status by district, all states (SBM-G dashboard, Ministry of Jal Shakti).

Input:  _sources/mojs-sbmg/raw/mojs-sbmg_states-dashboard_<date>.html   (saved by fetch_dashboard.sh)
        _reference/geography.csv                                        (LGD and Census 2011 codes)
Output: WAT_odf-plus-villages_2022-to-2026_STATES_MOJS_DIST/<same>.csv

The page embeds one JavaScript object per district (array `markersDistrict`) and prints a state-wise table.
Both carry two snapshots: "As on 1st April 2022" and "As on <page date>". In the district objects the
fields without a suffix are the 2022 snapshot and the fields ending `1Sep2022` are the current snapshot
(checked against the printed state table: the district sums match it exactly; see check_odf_plus.py).

Run from the repo root:  python3 pipelines/mojs-sbmg/build_odf_plus.py
"""
import csv
import html
import re
import sys
from pathlib import Path

RAW = sorted(Path("_sources/mojs-sbmg/raw").glob("mojs-sbmg_states-dashboard_*.html"))[-1]
PAGE_DATE = RAW.stem.rsplit("_", 1)[1]
NAME = "WAT_odf-plus-villages_2022-to-2026_STATES_MOJS_DIST"
OLD_DATE = "2022-04-01"

COLS = ["state_ut", "lgd_state_code", "district", "lgd_district_code", "sbm_district_code", "date",
        "total_villages", "odf_plus_villages", "odf_plus_aspiring_villages", "odf_plus_rising_villages",
        "odf_plus_model_villages", "odf_plus_villages_pct", "odf_plus_model_villages_pct"]

# field names in the district objects: (2022 snapshot, current snapshot)
FIELDS = {
    "odf_plus_villages": ("TotalStarVillage", "NoOfTotalodfplusVillage1Sep2022"),
    "odf_plus_aspiring_villages": ("NoOfOneStarVillage", "NoOfOneStarVillage1Sep2022"),
    "odf_plus_rising_villages": ("NoOfThreeStarVillage", "NoOfThreeStarVillage1Sep2022"),
    "odf_plus_model_villages": ("NoOfFiveStarVillage", "NoOfFiveStarVillage1Sep2022"),
    "odf_plus_villages_pct": ("TotalStarVillagePer", "TotalStarVillagePer1Sep2022"),
    "odf_plus_model_villages_pct": ("TotalModeVillagePer", "TotalModelVillagePer1Sep2022"),
}


STATE_VARIANTS = {"A & N Islands": "35", "D & N Haveli and Daman & Diu": "38"}


def norm(s):
    return re.sub(r"[^a-z]", "", s.lower())


def page():
    return RAW.read_text(encoding="utf-8", errors="ignore")


def district_objects(s):
    i = s.find("var markersDistrict")
    j = s.find("];", i)
    return [dict(re.findall(r'"(\w+)"\s*:\s*\'([^\']*)\'', o)) for o in re.findall(r"\{[^{}]*\}", s[i:j])]


def state_table(s):
    """Rows of the printed state-wise table: lgd_state_code -> {column: (2022, current)}."""
    i = s.find("States/UTs Wise ODF Plus Status")
    t = s[i:s.find("</table>", i)]
    out = {}
    for r in re.findall(r"<tr[^>]*>(.*?)</tr>", t, re.S):
        c = [re.sub(r"\s+", " ", re.sub("<[^>]+>", "", x)).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)]
        if len(c) != 10 or not c[1].isdigit():
            continue
        m = re.search(r"\((\d+)\)$", c[0])
        key = m.group(1) if m else "All India"
        last = lambda v: v.split()[-1]  # current cells read "+<added today> <value>"
        out[key] = {"label": c[0], "total_villages": c[1],
                    "odf_plus_villages": (c[2], last(c[3])), "odf_plus_model_villages": (c[4], last(c[5])),
                    "odf_plus_rising_villages": (c[6], last(c[7])), "odf_plus_aspiring_villages": (c[8], last(c[9]))}
    return out


def main():
    s = page()
    geo = list(csv.DictReader(open("_reference/geography.csv", encoding="utf-8")))
    states = {g["lgd_state_code"]: g["state_ut"] for g in geo if g["level"] == "state"}
    # the page's STCODE11 is SBM's own state code (Ladakh 38, Andhra Pradesh 37, ...): match states by name
    state_by_name = {norm(v): k for k, v in states.items() if k}
    state_by_name.update({norm(a): g["lgd_state_code"] for g in geo if g["level"] == "state" and g["lgd_state_code"]
                          for a in g["aliases"].split(";") if a.strip()})
    state_by_name.update({norm(k): v for k, v in STATE_VARIANTS.items()})
    dists = [g for g in geo if g["level"] == "district"]
    by_c11 = {(g["lgd_state_code"], g["census2011_district_code"]): g for g in dists if g["census2011_district_code"]}
    by_name = {}
    for g in dists:
        for n in [g["district"], g["census2011_name"], *g["aliases"].split(";")]:
            if n.strip():
                by_name.setdefault((g["lgd_state_code"], norm(n)), g)

    rows, log = [], []
    for o in district_objects(s):
        o["STNAME"], o["dtname"] = html.unescape(o["STNAME"]), html.unescape(o["dtname"]).strip()
        st = state_by_name[norm(o["STNAME"])]
        g = by_name.get((st, norm(o["dtname"])))
        how = "name"
        c11 = by_c11.get((st, o["dtcode11"]))
        if c11 and (g is None or g is c11):
            g, how = c11, "census2011_code"
        if g is None:
            log.append(f"no LGD match: {o['STNAME']} / {o['dtname']} ({o['dtcode11']})")
        elif how == "name":
            log.append(f"name match: {o['STNAME']} / {o['dtname']} ({o['dtcode11']}) -> {g['district']} ({g['lgd_district_code']})")
        for k, date in ((0, OLD_DATE), (1, PAGE_DATE)):
            r = {"state_ut": states[st], "lgd_state_code": st, "district": o["dtname"],
                 "lgd_district_code": g["lgd_district_code"] if g else "", "sbm_district_code": o["dtcode11"],
                 "date": date, "total_villages": o["TotalVillages"]}
            for col, f in FIELDS.items():
                r[col] = o[f[k]]
            rows.append(r)

    # published totals: State total per state and All India, from the printed table
    tab = state_table(s)
    for key, t in tab.items():
        st_name = "All India" if key == "All India" else states[key]
        for k, date in ((0, OLD_DATE), (1, PAGE_DATE)):
            r = {"state_ut": st_name, "lgd_state_code": "" if key == "All India" else key,
                 "district": "All India" if key == "All India" else "State total", "lgd_district_code": "",
                 "sbm_district_code": "", "date": date, "total_villages": t["total_villages"],
                 "odf_plus_villages_pct": "", "odf_plus_model_villages_pct": ""}
            for col in ("odf_plus_villages", "odf_plus_aspiring_villages", "odf_plus_rising_villages", "odf_plus_model_villages"):
                r[col] = t[col][k]
            rows.append(r)

    def key(r):
        tot = r["district"] in ("State total", "All India")
        return (r["state_ut"] == "All India", r["state_ut"], tot, r["district"], r["date"])

    rows.sort(key=key)
    out = Path(NAME) / f"{NAME}.csv"
    out.parent.mkdir(exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    Path("_sources/mojs-sbmg/match_log.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"{out}: {len(rows)} rows; {sum('no LGD' in x for x in log)} unmatched, "
          f"{sum('name match' in x for x in log)} name matches (see _sources/mojs-sbmg/match_log.txt)")


if __name__ == "__main__":
    sys.exit(main())
