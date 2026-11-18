"""Census 2011 table HH-14 (percentage of households by amenities and assets) for every district of India:
district and sub-district rows, all 135 indicators, total / rural / urban.

Input:  _sources/orgi-census2011/raw/hl14/orgi-census2011_hl14-district-<census code>_2011.xlsx  (fetch_hl14.sh)
        _reference/geography.csv
Output: HOU_household-amenities-hh14_2011_STATES_ORGI_DIST/<same>.csv   (district rows)
        HOU_household-amenities-hh14_2011_STATES_ORGI_SDT/<same>.csv    (district and sub-district rows)

The header parsing is shared with build_hl14_mh.py (Maharashtra only, kept for its published tables).
State and district names and LGD codes come from geography.csv by Census 2011 district code; districts
geography.csv cannot place keep their Census name and get blank LGD codes (never guessed).
Town, ward and village rows of the same files are not converted. Run from the repo root.
"""
import glob
import sys
from multiprocessing import Pool
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from build_hl14_mh import column_names  # noqa: E402

RAW = "_sources/orgi-census2011/raw/hl14"
GEO = "_reference/geography.csv"
NAME_DIST = "HOU_household-amenities-hh14_2011_STATES_ORGI_DIST"
NAME_SDT = "HOU_household-amenities-hh14_2011_STATES_ORGI_SDT"


def read_file(f):
    s = pd.read_excel(f, header=None, dtype=str)
    names = column_names(s)
    body = s.iloc[7:]
    body = body[body[0].notna() & body[0].str.strip().str.isdigit()]
    area = body[8].str.strip()
    # District and sub-district rows only: town code (col 6) is blank or all zeros
    keep = area.str.startswith(("District - ", "Sub-Dist - ")) & (body[6].fillna("").str.strip().str.strip("0") == "")
    body, area = body[keep], area[keep]
    meta = pd.DataFrame({
        "state_census_code": body[1].str.strip().values,
        "district_census_code": body[2].str.strip().values,
        "district_census_name": body[3].str.strip().values,
        "area_level": ["district" if a.startswith("District") else "sub-district" for a in area],
        "subdistrict": [a.split(" - ", 1)[1].strip() if a.startswith("Sub-Dist") else "" for a in area],
        "subdistrict_census_code": [t.strip() if t.strip().strip("0") else "" for t in body[4].fillna("")],
        "residence": body[9].str.strip().values,
    })
    vals = pd.DataFrame({name: pd.to_numeric(body[c].str.strip(), errors="raise").values for c, name in names.items()})
    return names, pd.concat([meta, vals], axis=1)


def main():
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    dist_geo = geo[(geo.level == "district") & (geo.census2011_district_code != "")].drop_duplicates("census2011_district_code").set_index("census2011_district_code")
    state_geo = geo[geo.level == "state"].drop_duplicates("census2011_state_code").set_index("census2011_state_code")
    files = sorted(glob.glob(f"{RAW}/*.xlsx"))
    with Pool(8) as pool:
        results = pool.map(read_file, files)
    names = results[0][0]
    for f, (n, _) in zip(files, results):
        assert n == names, f"{f}: header differs"
    out = pd.concat([r[1] for r in results], ignore_index=True)

    def lookup(code, col, fallback=""):
        return dist_geo.at[code, col] if code in dist_geo.index else fallback

    codes = out.district_census_code
    unmatched = sorted(set(codes) - set(dist_geo.index))
    out.insert(0, "state_ut", [lookup(c, "state_ut", state_geo.at[s, "state_ut"] if s in state_geo.index else "")
                               for c, s in zip(codes, out.state_census_code)])
    out.insert(1, "lgd_state_code", [lookup(c, "lgd_state_code", state_geo.at[s, "lgd_state_code"] if s in state_geo.index else "")
                                     for c, s in zip(codes, out.state_census_code)])
    out.insert(2, "district", [lookup(c, "district", n) for c, n in zip(codes, out.district_census_name)])
    out.insert(3, "lgd_district_code", [lookup(c, "lgd_district_code") for c in codes])
    order = {"Total": 0, "Rural": 1, "Urban": 2}
    out["_o"] = out.residence.map(order)
    out["_l"] = (out.area_level == "sub-district").astype(int)
    out = out.sort_values(["state_ut", "district", "_l", "subdistrict_census_code", "_o"]).drop(columns=["_o", "_l"])
    for name, df in ((NAME_SDT, out), (NAME_DIST, out[out.area_level == "district"].drop(columns=["area_level", "subdistrict", "subdistrict_census_code"]))):
        Path(name).mkdir(exist_ok=True)
        df.to_csv(Path(name) / f"{name}.csv", index=False, lineterminator="\n")
        print(name, df.shape)
    print("files:", len(files), "| census districts not in geography.csv:", unmatched)


if __name__ == "__main__":
    main()
