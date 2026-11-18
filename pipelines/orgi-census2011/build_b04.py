"""Census 2011 table B-04: main workers classified by age, industrial category and sex, every district of India.

Input:  _sources/orgi-census2011/raw/b04/orgi-census2011_b04-state-<code>_2011.xls  (fetch_b04.sh; 00 = India)
        _reference/geography.csv
Output: LAB_main-workers-by-industry_2011_STATES_ORGI_DIST/<same>.csv

One row per state or district x total/rural/urban x age group. The printed header gives NIC 2008 section
letters only (A, B, C, D & E, ...); column names add the standard NIC section titles (see README). State rows
are kept as `State total`; the India file is used only for the `All India` rows.
Run from the repo root.
"""
import glob
from pathlib import Path

import pandas as pd

RAW = "_sources/orgi-census2011/raw/b04"
GEO = "_reference/geography.csv"
NAME = "LAB_main-workers-by-industry_2011_STATES_ORGI_DIST"
# first column of each P/M/F triple -> name stem (header text as printed, plus the NIC 2008 section title)
GROUPS = {
    6: "main_workers_total",
    9: "a_cultivators", 12: "a_agricultural_labourers", 15: "a_plantation_livestock_forestry_fishing",
    18: "b_mining_quarrying", 21: "c_manufacturing_hhi", 24: "c_manufacturing_non_hhi",
    27: "d_e_electricity_gas_water_waste", 30: "f_construction", 33: "g_trade_repair_hhi", 36: "g_trade_repair_non_hhi",
    39: "h_transport_storage", 42: "i_accommodation_food", 45: "j_information_communication_hhi",
    48: "j_information_communication_non_hhi", 51: "k_to_m_finance_real_estate_professional",
    54: "n_to_o_administrative_public_administration", 57: "p_to_q_education_health",
    60: "r_to_u_other_services_hhi", 63: "r_to_u_other_services_non_hhi",
}
AGE_ORDER = ["Total", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-49", "50-59", "60-69",
             "70-79", "80+", "Age not stated"]


def read(f):
    d = pd.read_excel(f, header=None, dtype=str)
    # sanity check that the layout is the one GROUPS describes
    assert " ".join(str(d.iat[2, 18]).split()) == "B" and " ".join(str(d.iat[2, 27]).split()) == "D & E", f
    body = d[d[0].fillna("").str.strip().str.startswith("B01")]
    area = body[3].str.strip()
    out = pd.DataFrame({
        "state_census_code": body[1].str.strip().values,
        "district_census_code": body[2].str.strip().values,
        "area_name": area.values,
        "residence": body[4].str.strip().values,
        "age_group": body[5].str.strip().values,
    })
    for c, stem in GROUPS.items():
        for k, sex in enumerate(("persons", "males", "females")):
            out[f"{stem}_{sex}"] = pd.to_numeric(body[c + k].str.strip(), errors="raise").astype("int64").values
    return out


def main():
    geo = pd.read_csv(GEO, dtype=str, keep_default_na=False)
    dist = geo[(geo.level == "district") & (geo.census2011_district_code != "")].drop_duplicates("census2011_district_code").set_index("census2011_district_code")
    states = geo[geo.level == "state"].drop_duplicates("census2011_state_code").set_index("census2011_state_code")
    parts = []
    for f in sorted(glob.glob(f"{RAW}/*.xls*")):
        t = read(f)
        # India file (state code 00): keep only its India rows; its state rows repeat the state files
        t = t[t.state_census_code == "00"] if "-00_2011." in f else t
        parts.append(t)
    t = pd.concat(parts, ignore_index=True)
    is_dist = t.district_census_code.str.strip("0") != ""
    is_india = t.state_census_code == "00"
    st = t.state_census_code
    t.insert(0, "state_ut", ["All India" if i else (dist.at[c, "state_ut"] if d and c in dist.index else states.at[s, "state_ut"] if s in states.index else "")
                             for i, d, c, s in zip(is_india, is_dist, t.district_census_code, st)])
    t.insert(1, "lgd_state_code", ["" if i else (dist.at[c, "lgd_state_code"] if d and c in dist.index else states.at[s, "lgd_state_code"] if s in states.index else "")
                                   for i, d, c, s in zip(is_india, is_dist, t.district_census_code, st)])
    t.insert(2, "district", [(dist.at[c, "district"] if c in dist.index else a.split(" - ", 1)[-1].strip()) if d else ("" if i else "State total")
                             for i, d, c, a in zip(is_india, is_dist, t.district_census_code, t.area_name)])
    t.insert(3, "lgd_district_code", [dist.at[c, "lgd_district_code"] if d and c in dist.index else "" for d, c in zip(is_dist, t.district_census_code)])
    t["district_census_code"] = t.district_census_code.where(is_dist, "")
    t["district_census_name"] = [a.split(" - ", 1)[-1].strip() if d else "" for d, a in zip(is_dist, t.area_name)]
    t = t.drop(columns=["area_name"])
    cols = ["state_ut", "lgd_state_code", "state_census_code", "district", "lgd_district_code", "district_census_code",
            "district_census_name", "residence", "age_group"]
    t = t[cols + [c for c in t.columns if c not in cols]]
    unknown_age = set(t.age_group) - set(AGE_ORDER)
    assert not unknown_age, unknown_age
    t["_india"] = (t.state_ut == "All India").astype(int)  # totals last: districts, then State total, then All India
    t["_tot"] = (t.district == "State total").astype(int)
    t["_r"] = t.residence.map({"Total": 0, "Rural": 1, "Urban": 2})
    t["_a"] = t.age_group.map({a: i for i, a in enumerate(AGE_ORDER)})
    t = t.sort_values(["_india", "state_ut", "_tot", "district", "_r", "_a"]).drop(columns=["_india", "_tot", "_r", "_a"])
    Path(NAME).mkdir(exist_ok=True)
    t.to_csv(f"{NAME}/{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, t.shape, "districts:", t.loc[t.district_census_code != "", "district_census_code"].nunique(),
          "| unmatched census codes:", sorted(set(t.loc[(t.district_census_code != "") & (t.lgd_district_code == ""), "district"])))


if __name__ == "__main__":
    main()
