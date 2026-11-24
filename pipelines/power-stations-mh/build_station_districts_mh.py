"""Give each Maharashtra power station in the CEA tables a district (BNY), and write two district tables.

Input:  ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA   (CEA CO2 Baseline Database v22, station-wise)
        ENG_fly-ash-power-plants_FY2025-26_STATES_CEA                  (CEA Fly Ash Year Book 2026, plant-wise)
        ENG_power-plants_2021_STATES_WRI_DIST                          (WRI GPPD v1.3: coordinates -> district)
        _reference/geography.csv
Output: _reference/power-stations-maharashtra.csv                       (station -> district lookup)
        ENG_power-station-generation-co2_2017-18-to-2025-26_MH_BNY_DIST/<same>.csv
        ENG_fly-ash-power-stations_FY2025-26_MH_BNY_DIST/<same>.csv

District of a CEA station: the WRI plant of the same name (WRI took its Indian plant list from CEA, so names
match), whose district came from its coordinates. Where WRI has no plant of that name, or its 2011-era district
boundaries put a plant in the wrong current district (Palghar was split from Thane in 2014), the district is set
by hand below, with the reason. Fly-ash plant names are printed differently, so each is tied to its CEA CO2 station.

Run from the repo root:  python3 pipelines/power-stations-mh/build_station_districts_mh.py
"""
import csv
import re
from pathlib import Path

CO2 = "ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA"
ASH = "ENG_fly-ash-power-plants_FY2025-26_STATES_CEA"
WRI = "ENG_power-plants_2021_STATES_WRI_DIST"
LOOKUP = "_reference/power-stations-maharashtra.csv"
OUT_CO2 = "ENG_power-station-generation-co2_2017-18-to-2025-26_MH_BNY_DIST"
OUT_ASH = "ENG_fly-ash-power-stations_FY2025-26_MH_BNY_DIST"

# CEA station -> (district, reason). Used where WRI has no plant of that name or WRI's district is out of date.
HAND = {
    "DHANU": ("Palghar", "Dahanu TPS, Dahanu taluka; WRI says Thane (2011 boundaries, before Palghar was split off)"),
    "TARAPUR": ("Palghar", "Tarapur Atomic Power Station, Palghar taluka; WRI says Thane (2011 boundaries)"),
    "SURYA": ("Palghar", "Surya project (Dhamni dam), Vikramgad taluka; WRI says Thane (2011 boundaries)"),
    "SOLAPUR STPP": ("Solapur", "NTPC Solapur, Fatatewadi, Solapur South taluka; not in WRI"),
    "SHIRPUR": ("Dhule", "Shirpur Power, Shirpur taluka; not in WRI"),
    "DIMBE": ("Pune", "Dimbhe dam, Ambegaon taluka; not in WRI"),
    "NASHIK": ("Nashik", "Nashik TPS, Eklahare; WRI name NASIK"),
    "EMCO GMR WARORA TPP": ("Chandrapur", "GMR Warora, Warora taluka; WRI name GMR WARORA TPP"),
    "IEPL ,BELA TPP": ("Nagpur", "Ideal Energy, Bela, Umred taluka; WRI name IEPL  BELA TPP"),
}

# Extra notes for stations whose works span two districts (district kept from WRI's point)
SPANS = {
    "KOYNA COMPLEX": "Koyna dam and Koynanagar are in Satara; WRI's point is at the Pophali powerhouses in Ratnagiri",
    "GHATGHAR PSS": "upper dam in Akole taluka (Ahilyanagar); WRI's point is at the lower dam / powerhouse in Thane",
    "PENCH": "inter-state Pench project shared with Madhya Pradesh; WRI's point is in Nagpur",
}

# Fly-ash plant (as printed) -> CEA CO2 station
ASH_TO_STATION = {
    "MOUDA": "MOUDA STPS", "SOLAPUR": "SOLAPUR STPP", "CHANDRAPUR": "CHANDRAPUR_Coal", "KHAPARKHEDA": "K_KHEDA II",
    "KORADI": "KORADI", "NASHIK": "NASHIK", "PARAS": "PARAS", "PARLI": "PARLI", "BHUSAWAL": "BHUSAWAL",
    "TIRODA": "TIRORA TPP", "APL": "DHANU", "SHIRPUR POWER PVT LTD": "SHIRPUR", "RATNAGIRI": "JSW RATNAGIRI TPP",
    "AMRAVATI": "AMARAVATI TPP", "DHARIWAL INFRASTRUCTURE Ltd.": "DHARIWAL INF TPP",
    "GMR WARORA ENERGY LIMITED": "EMCO GMR WARORA TPP", "SAI WARDHA POWER Ltd. ,WARORA": "WARDHA WARORA(Sai Wardha Power)",
    "BELA TPS": "IEPL ,BELA TPP", "TROMBAY": "TROMBAY_Coal",
}
ASH_NOTES = {"APL": "Adani Electricity Mumbai's 500 MW plant = Dahanu TPS (CEA CO2 name DHANU)"}


def read(name):
    return list(csv.DictReader(open(Path(name) / f"{name}.csv", encoding="utf-8")))


def key(s):
    return re.sub(r"\s+", " ", s).strip().upper()


def write(path, cols, rows):
    Path(path).parent.mkdir(exist_ok=True, parents=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    geo = {g["district"]: g["lgd_district_code"] for g in csv.DictReader(open("_reference/geography.csv", encoding="utf-8"))
           if g["level"] == "district" and g["state_ut"] == "Maharashtra"}
    wri = {key(r["plant"]): r for r in read(WRI) if r["state_ut"] == "Maharashtra"}
    co2 = [r for r in read(CO2) if r["state_ut"] == "Maharashtra"]

    lookup = {}
    for st in sorted({r["station"] for r in co2}):
        if st in HAND:
            d, note = HAND[st]
            src = "hand"
        elif key(st) in wri:
            w = wri[key(st)]
            d, note, src = w["district"], f"WRI {w['gppd_idnr']} ({w['latitude']}, {w['longitude']}), {w['district_match']}", "wri_coordinates"
            if st in SPANS:
                note += f"; {SPANS[st]}"
        else:
            raise SystemExit(f"no district for CEA station {st!r}: add it to HAND")
        lookup[st] = {"station": st, "state_ut": "Maharashtra", "lgd_state_code": "27", "district": d,
                      "lgd_district_code": geo[d], "district_source": src, "note": note}
    write(LOOKUP, ["station", "state_ut", "lgd_state_code", "district", "lgd_district_code", "district_source", "note"],
          list(lookup.values()))

    # 1. station generation and CO2, with district
    keep = ["capacity_mw_2026_03_31", "sector", "owner", "type", "fuel_1", "fuel_2", "net_generation_gwh",
            "co2_emissions_t", "co2_intensity_t_per_mwh"]
    rows = []
    for r in co2:
        L = lookup[r["station"]]
        rows.append({"state_ut": "Maharashtra", "lgd_state_code": "27", "district": L["district"],
                     "lgd_district_code": L["lgd_district_code"], "station": r["station"], "year": r["year"],
                     **{k: r[k] for k in keep}})
    rows.sort(key=lambda r: (r["district"], r["station"], r["year"]))
    write(Path(OUT_CO2) / f"{OUT_CO2}.csv", list(rows[0]), rows)

    # 2. fly ash by coal plant, with district (state Grand Total row kept last)
    ash = [r for r in read(ASH) if r["state_ut"] == "Maharashtra"]
    out = []
    for r in ash:
        base = {k: r[k] for k in ["plant", "year", "utility", "installed_capacity_mw", "ash_generation_lmt",
                                  "ash_utilization_lmt", "ash_utilization_pct"]}
        if r["plant"] == "Grand Total":
            out.append({"state_ut": "Maharashtra", "lgd_state_code": "27", "district": "State total",
                        "lgd_district_code": "", "cea_co2_station": "", **base})
            continue
        st = ASH_TO_STATION[r["plant"]]
        L = lookup[st]
        out.append({"state_ut": "Maharashtra", "lgd_state_code": "27", "district": L["district"],
                    "lgd_district_code": L["lgd_district_code"], "cea_co2_station": st, **base})
    out.sort(key=lambda r: (r["district"] == "State total", r["district"], r["plant"]))
    write(Path(OUT_ASH) / f"{OUT_ASH}.csv", list(out[0]), out)
    print(f"{LOOKUP}: {len(lookup)} stations ({sum(v['district_source'] == 'hand' for v in lookup.values())} by hand)")
    print(f"{OUT_CO2}: {len(rows)} rows;  {OUT_ASH}: {len(out)} rows")


if __name__ == "__main__":
    main()
