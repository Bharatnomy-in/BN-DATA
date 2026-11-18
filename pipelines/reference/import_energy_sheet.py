"""Add the Energy variable sheet (Energy_combined.xlsx: tabs LPG, Coal, Electricity) to _reference/variables-draft.csv.

Each sheet row becomes one draft row: sheet `energy_lpg` / `energy_coal` / `energy_electricity`, `sno` = row order,
`variable_name` = first line of the "Variable definition" cell (exactly as written), `definition` = the rest,
`sheet_unit` / `sheet_sources` blank (the energy sheet has none). Where each variable ended up is recorded in WHERE
below. Existing energy rows are replaced; climate rows are left as they are.
The sheet is kept outside the repo; pass its path (default: ../Energy_combined.xlsx next to the repo).

Run from the repo root:  python3 pipelines/reference/import_energy_sheet.py [path/to/Energy_combined.xlsx]
Then:                     python3 pipelines/reference/build_variables.py && python3 tools/build_catalog.py
"""
import csv
import sys
from pathlib import Path

import openpyxl

SHEET = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("../Energy_combined.xlsx")
DRAFT = Path("_reference/variables-draft.csv")
TABS = {"LPG": "energy_lpg", "Coal": "energy_coal", "Electricity": "energy_electricity"}

GR = "CEA General Review 2025 (data 2023-24)"
PPAC = "PPAC LPG Profile Report H1 FY 2026-27"
CD = "Coal Directory of India 2024-25 (Ministry of Coal)"
CO2 = "CEA CO2 Baseline Database v22"
HH14 = "HOU_household-amenities-hh14_2011_STATES_ORGI_DIST"  # all districts of India (18 Nov 2026)
NOCITY = "State level only; no city or district figures"


def w(dataset="", column="", unit="", geo="", freq="", first="", last="", used="", tried="", status="not found", reason=""):
    return dict(dataset=dataset, column=column, unit=unit, geo_level=geo, frequency=freq, earliest_period=first,
                latest_period=last, source_used=used, sources_tried=tried, status=status, reason=reason)


WHERE = {
    # ------------------------------------------------------------------ LPG
    ("energy_lpg", 1): w("ENG_lpg-bottling-plants_2026-10_STATES_PPAC", "bottling_plants_count; bottling_capacity_tmtpa", "count; thousand tonnes per annum",
                         "STATE", "half-yearly (latest only)", "2026-10-01", "2026-10-01", PPAC, "PPAC", "partial", NOCITY + "; plant locations not given"),
    ("energy_lpg", 2): w(tried="PPAC city gas distribution table", reason="PNGRB list of authorised geographical areas and their companies not taken yet; PPAC's table has connections by state group, not companies"),
    ("energy_lpg", 3): w("ENG_lpg-distributors_2001-to-2026_STATES_PPAC", "distributors_count", "count", "STATE", "annual", "2001", "2026-08-01",
                         "PPAC LPG distributors table (also by category in ENG_lpg-distributors-by-category_2026-10_STATES_PPAC)", "PPAC", "partial", NOCITY),
    ("energy_lpg", 4): w("ENG_lpg-active-domestic-customers_2026-10_STATES_PPAC", "active_domestic_customers_lakh", "lakh connections", "STATE",
                         "half-yearly (latest only)", "2026-10-01", "2026-10-01", PPAC, "PPAC", "partial", NOCITY),
    ("energy_lpg", 5): w("ENG_pmuy-connections_2026-10_STATES_PPAC", "pmuy_connections_count", "count", "STATE", "half-yearly (latest only)",
                         "2026-10-01", "2026-10-01", PPAC, "PPAC", "partial", NOCITY),
    ("energy_lpg", 6): w(tried="PPAC LPG Profile Report; PPAC web tables", reason="Coverage per 100 households is not in PPAC's current report or tables; could be computed from active connections and Census household counts"),
    ("energy_lpg", 7): w("ENG_png-connections-cng-stations_2025-01-to-2026-07_STATES_PPAC", "png_domestic_count", "count", "STATE", "irregular",
                         "2025-01-31", "2026-07-31", "PPAC city gas distribution table", "PPAC", "partial", "By state or group of states (licence areas); no city figures"),
    ("energy_lpg", 8): w("ENG_png-connections-cng-stations_2025-01-to-2026-07_STATES_PPAC", "png_commercial_count; png_industrial_count", "count", "STATE",
                         "irregular", "2025-01-31", "2026-07-31", "PPAC city gas distribution table", "PPAC", "partial", "By state or group of states (licence areas); no city figures"),
    ("energy_lpg", 9): w("ENG_lpg-domestic-sales_2026-04-to-2026-09_STATES_PPAC", "packed_domestic_sales_tmt", "thousand tonnes", "STATE", "half-yearly (latest only)",
                         "2026-04", "2026-09", PPAC, "PPAC", "partial", NOCITY + "; one half-year"),
    ("energy_lpg", 10): w(tried="PPAC LPG Profile Report; PPAC state-wise sales table", reason="State-wise commercial (19 kg) LPG sales not published in these; only auto LPG and non-domestic customer counts"),
    ("energy_lpg", 11): w(tried="PPAC LPG Profile Report", reason="Refills per consumer not published by state in the current report"),
    ("energy_lpg", 12): w(tried="PPAC LPG Profile Report", reason="PMUY refill rate not published by state in the current report"),
    ("energy_lpg", 13): w(tried="PPAC prices page", reason="PPAC links to IOCL's metro-city prices only; no Nagpur price series taken"),
    ("energy_lpg", 14): w(tried="PPAC prices page", reason="Commercial cylinder prices: IOCL metro-city prices only; not taken"),
    ("energy_lpg", 15): w(reason="City gas company tariffs (Nagpur: licence holder's website) not taken"),
    ("energy_lpg", 16): w(tried="PPAC subsidy page", reason="Per-cylinder PMUY subsidy is a notified rate (MoPNG press releases), not a dataset; not taken"),
    ("energy_lpg", 17): w(HH14, "cooking_fuel_lpg_png_pct; cooking_fuel_electricity_pct; cooking_fuel_biogas_pct", "% of households", "DIST", "one-off", "2011", "2011",
                          "Census 2011 HH-14", "Census 2011 HH-14; NFHS-5", "partial", "Census 2011 only (all districts); clean fuel = sum of the LPG/PNG, electricity and biogas columns; NFHS-5 not reachable (rchiips.org)"),
    ("energy_lpg", 18): w(HH14, "cooking_fuel_lpg_png_pct", "% of households", "DIST", "one-off", "2011", "2011", "Census 2011 HH-14", "Census 2011 HH-14", "partial", "Census 2011 only (all districts)"),
    ("energy_lpg", 19): w(HH14, "cooking_fuel_fire_wood_pct; cooking_fuel_crop_residue_pct; cooking_fuel_cowdung_cake_pct", "% of households", "DIST", "one-off", "2011", "2011",
                          "Census 2011 HH-14", "Census 2011 HH-14", "partial", "Census 2011 only (all districts)"),
    ("energy_lpg", 20): w(tried="MoSPI HCES 2023-24", reason="HCES unit-level data not taken yet"),
    # ------------------------------------------------------------------ Coal
    ("energy_coal", 1): w("ENG_coal-resources_2005-to-2025_STATES_MOC", "proved_mt; indicated_mt; inferred_mt; total_mt", "million tonnes", "STATE", "annual",
                          "2022-04-01", "2025-04-01", CD + " Table 2.2", "Ministry of Coal", "found", ""),
    ("energy_coal", 2): w("ENG_coal-lignite-mines_2025-03_STATES_MOC", "producing_open_cast_count; producing_underground_count; producing_total_count", "count", "STATE",
                          "annual (latest only)", "2025-03-31", "2025-03-31", CD + " Table 12.2", "Ministry of Coal", "partial", "By type of mine; split by owner (Table 12.8) not taken yet"),
    ("energy_coal", 3): w("ENG_coal-production_2015-16-to-2024-25_STATES_MOC", "production_mt", "million tonnes", "STATE", "annual", "2015-16", "2024-25",
                          CD + " Table 3.9", "Ministry of Coal", "found", ""),
    ("energy_coal", 4): w("ENG_lignite-production_2015-16-to-2024-25_STATES_MOC", "production_mt", "million tonnes", "STATE", "annual", "2015-16", "2024-25",
                          CD + " Table 3.10", "Ministry of Coal", "found", ""),
    ("energy_coal", 5): w("ENG_coal-despatch-by-mode_2015-16-to-2024-25_IN_MOC", "external_rail_mt; external_road_mt; external_belt_mt; external_mgr_mt; grand_total_mt",
                          "million tonnes", "IN", "annual", "2015-16", "2024-25", CD + " Table 4.18 (state totals in ENG_coal-despatch_2014-15-to-2024-25_STATES_MOC)",
                          "Ministry of Coal", "partial", "Mode-wise only for All India (and by company); state despatch totals without mode"),
    ("energy_coal", 6): w("ENG_coal-offtake-by-sector_FY2024-25_IN_MOC", "power_utility_mt; steel_coke_oven_cokeries_mt; cement_mt; sponge_iron_mt; bricks_mt; other_mt",
                          "million tonnes", "IN", "annual (latest only)", "2024-25", "2024-25", CD + " Table 4.20", "Ministry of Coal", "partial",
                          "By coal company (WCL serves Maharashtra), not by state; state-to-state flows in ENG_coal-despatch-source-destination_FY2024-25_STATES_MOC"),
    ("energy_coal", 7): w("ENG_coal-imports-by-port_FY2024-25_IN_MOC", "total_coal_mt", "million tonnes", "IN", "annual (latest only)", "2024-25", "2024-25",
                          CD + " Table 8.5", "Ministry of Coal", "partial", "By port; ports are not assigned to states in the source"),
    ("energy_coal", 8): w("ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA", "station; capacity_mw_2026_03_31; fuel_1", "MW", "STATE", "annual",
                          "2017-18", "2025-26", CO2, "CEA", "partial", "Every coal station with state and capacity; no district or coordinates"),
    ("energy_coal", 9): w("ENG_power-plant-fuel-use_FY2023-24_STATES_CEA", "coal_000_t", "thousand tonnes", "STATE", "annual (latest only)", "2023-24", "2023-24",
                          GR + " Table 7.1", "CEA General Review; CEA fuel consumption report", "partial", "State totals; plant-wise coal use (General Review Table 7.7) not taken yet"),
    ("energy_coal", 10): w(tried="CEA daily coal stock report", reason="CEA daily coal stock reports (plant-wise days of stock) not taken yet"),
    ("energy_coal", 11): w("ENG_fly-ash-power-plants_FY2025-26_STATES_CEA", "ash_generation_lmt; ash_utilization_lmt; ash_utilization_pct", "lakh tonnes; %", "STATE",
                           "annual (latest only)", "2025-26", "2025-26", "CEA Fly Ash Year Book 2026", "CEA", "found", "Plant-wise (196 plants)"),
    ("energy_coal", 12): w(reason="No official list of coal-using factories by city found (CPCB/MPCB industry lists not taken)"),
    ("energy_coal", 13): w(reason="Brick kiln counts by district not found from an official no-login source"),
    ("energy_coal", 14): w(HH14, "cooking_fuel_coal_lignite_charcoal_pct", "% of households", "DIST", "one-off", "2011", "2011", "Census 2011 HH-14", "Census 2011 HH-14", "partial", "Census 2011 only (all districts)"),
    ("energy_coal", 15): w(tried="CPCB daily AQI bulletins", reason="Annual PM2.5 / PM10 averages by city not taken; the repo has the city AQI (ENV_aqi-daily_*), not particulate concentrations"),
    ("energy_coal", 16): w("ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA", "co2_emissions_t; net_generation_gwh", "tonnes CO2", "STATE", "annual",
                           "2017-18", "2025-26", CO2, "CEA", "found", "Station-wise; pick the stations near the city by name"),
    ("energy_coal", 17): w(tried="Coal Directory of India 2024-25", reason="No state-wise employment table in the Coal Directory (only output per man-shift)"),
    ("energy_coal", 18): w("ENG_coal-royalty-dmf-nmet_2022-23-to-2024-25_STATES_MOC", "dmf_inr_crore", "Rs crore", "STATE", "annual", "2022-23", "2024-25",
                           CD + " Table 7.7", "Ministry of Coal", "partial", "DMF paid by coal companies; spending (Ministry of Mines PMKKKY portal) not taken"),
    ("energy_coal", 19): w("ENG_coal-royalty-dmf-nmet_2022-23-to-2024-25_STATES_MOC", "royalty_inr_crore", "Rs crore", "STATE", "annual", "2022-23", "2024-25",
                           CD + " Table 7.7 (2024-25 detail in ENG_coal-royalty-dmf-taxes_FY2024-25_STATES_MOC)", "Ministry of Coal", "found", ""),
    # ------------------------------------------------------------------ Electricity
    ("energy_electricity", 1): w("ENG_installed-capacity_2026-09_STATES_CEA", "coal_mw; lignite_mw; gas_mw; diesel_mw; nuclear_mw; hydro_mw; res_mnre_mw; grand_total_mw",
                                 "MW", "STATE", "monthly (latest only)", "2026-09", "2026-09", "CEA installed capacity report (Excel)", "CEA", "found",
                                 "Capacity supplying the state, including allocated shares of central stations"),
    ("energy_electricity", 2): w("ENG_renewable-capacity_2024-03_STATES_CEA", "solar_mw; wind_mw; small_hydro_mw; bio_power_total_mw; total_re_mw", "MW", "STATE",
                                 "annual (latest only)", "2024-03-31", "2024-03-31", GR + " Table 3.11 (MNRE data)", "CEA General Review; MNRE", "found", ""),
    ("energy_electricity", 3): w("ENG_co2-emissions-power-plants_2017-18-to-2025-26_STATES_CEA", "station; type; fuel_1; capacity_mw_2026_03_31", "MW", "STATE", "annual",
                                 "2017-18", "2025-26", CO2, "CEA", "partial", "All thermal, hydro and nuclear stations with state; no location; solar and wind plants not listed"),
    ("energy_electricity", 4): w(tried="MNRE rooftop solar portal", reason="City-wise rooftop solar (PM Surya Ghar portal) is a JavaScript dashboard; not taken"),
    ("energy_electricity", 5): w(tried="CEA SubStations report", reason="CEA lists new substations only; locations of existing substations not published as data"),
    ("energy_electricity", 6): w("ENG_peak-demand_2013-01-to-2026-08_STATES_CEA", "peak_demand_mw; peak_met_mw", "MW", "STATE", "monthly", "2013-01", "2026-08",
                                 "CEA Peak Power Supply Position reports", "CEA", "found", ""),
    ("energy_electricity", 7): w("ENG_energy-supply-position_2013-01-to-2026-08_STATES_CEA", "energy_requirement_mu; energy_supplied_mu", "MU (GWh)", "STATE", "monthly",
                                 "2013-01", "2026-08", "CEA Energy Power Supply Position reports", "CEA", "found", "61 months missing (CEA posted generation reports in their place)"),
    ("energy_electricity", 8): w("ENG_energy-supply-position_2013-01-to-2026-08_STATES_CEA", "energy_not_supplied_mu; energy_not_supplied_pct; surplus_deficit_mu; surplus_deficit_pct",
                                 "MU; %", "STATE", "monthly", "2013-01", "2026-08", "CEA Energy and Peak Power Supply Position reports (MW shortage in ENG_peak-demand_*)",
                                 "CEA", "found", "61 months missing in the energy series"),
    ("energy_electricity", 9): w(tried="Grid-India / SLDC", reason="Hourly state demand is on Grid-India and SLDC (MSLDC) dashboards; not taken"),
    ("energy_electricity", 10): w(tried="CEA General Review Table 8.2", reason="General Review Table 8.2 (transformers by state, not 33/11 kV substations by city) not taken yet"),
    ("energy_electricity", 11): w(tried="National Power Portal", reason="Hours of supply (NPP / DISCOM reports) not taken"),
    ("energy_electricity", 12): w(tried="", reason="SAIFI/SAIDI are in DISCOM regulatory filings (MERC), not a public dataset"),
    ("energy_electricity", 13): w(tried="", reason="Smart meter progress is on the RDSS / National Smart Grid Mission dashboard; not taken"),
    ("energy_electricity", 14): w("ENG_td-losses_FY2023-24_STATES_CEA", "td_losses_pct; td_losses_gwh", "%; GWh", "STATE", "annual (latest only)", "2023-24", "2023-24",
                                  GR + " Table 6.4", "CEA General Review; PFC report on performance of power utilities", "partial", "T&D losses, not AT&C; PFC's AT&C table not taken yet"),
    ("energy_electricity", 15): w("ENG_consumers-connected-load_2024-03_STATES_CEA", "domestic_consumers; commercial_consumers; industrial_lv_mv_consumers; agriculture_consumers; total_consumers",
                                  "count", "STATE", "annual (latest only)", "2024-03-31", "2024-03-31", GR + " Table 10", "CEA General Review", "found", NOCITY),
    ("energy_electricity", 16): w("ENG_electricity-sales-by-category_FY2023-24_STATES_CEA", "domestic_gwh; commercial_gwh; industrial_lv_mv_gwh; industrial_hv_gwh; agriculture_gwh; total_sold_gwh",
                                  "GWh (MU)", "STATE", "annual (latest only)", "2023-24", "2023-24", GR + " Table 9.3", "CEA General Review", "found", NOCITY),
    ("energy_electricity", 17): w("ENG_consumers-connected-load_2024-03_STATES_CEA", "domestic_load_kw; commercial_load_kw; industrial_lv_mv_load_kw; agriculture_load_kw; total_load_kw",
                                  "kW", "STATE", "annual (latest only)", "2024-03-31", "2024-03-31", GR + " Table 10", "CEA General Review", "found", NOCITY),
    ("energy_electricity", 18): w("ENG_per-capita-consumption_FY2023-24_STATES_CEA", "per_capita_consumption_kwh", "kWh per person", "STATE", "annual (latest only)",
                                  "2023-24", "2023-24", GR + " Table 9.9", "CEA General Review", "found", ""),
    ("energy_electricity", 19): w(tried="CEA Tariff & Duty report", reason="CEA's Tariff & Duty of Electricity Supply report (PDF) not taken yet"),
    ("energy_electricity", 20): w(HH14, "lighting_electricity_pct", "% of households", "DIST", "one-off", "2011", "2011", "Census 2011 HH-14", "Census 2011 HH-14",
                                  "partial", "Census 2011 (all districts); electricity as main source of lighting"),
    ("energy_electricity", 21): w(tried="MoSPI HCES 2023-24", reason="HCES unit-level data not taken yet"),
    ("energy_electricity", 22): w(tried="Vahan dashboard", reason="Vahan is a JavaScript dashboard; not taken"),
    ("energy_electricity", 23): w("ENG_grid-emission-factor_2016-17-to-2025-26_IN_CEA", "weighted_avg_grid_emission_rate_incl_re_captive_t_per_mwh; weighted_avg_emission_rate_t_per_mwh",
                                  "t CO2 per MWh", "IN", "annual", "2016-17", "2025-26", CO2, "CEA", "partial", "National grid only; no state supply-mix factor published"),
    ("energy_electricity", 24): w(reason="Not published; can be estimated from ENG_peak-demand_* (monthly) and CLM_temperature-indices_* or CLM_heat-indicators-nagpur_*"),
}


def main():
    with open(DRAFT, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        fields, rows = list(r.fieldnames), [x for x in r if not x["sheet"].startswith("energy_")]
    wb = openpyxl.load_workbook(SHEET, data_only=True)
    new = []
    for tab, sheet in TABS.items():
        ws = wb[tab]
        n = 0
        for stage, cell in ws.iter_rows(min_row=2, values_only=True):
            if not cell:
                continue
            n += 1
            name, _, definition = str(cell).strip().partition("\n")
            row = {k: "" for k in fields}
            row.update(sheet=sheet, sno=str(n), variable_name=name.strip(), definition=f"{definition.strip()} ({stage.strip()})")
            if (sheet, n) not in WHERE:
                raise SystemExit(f"no WHERE entry for {sheet} #{n}: {name}")
            row.update(WHERE[(sheet, n)])
            new.append(row)
    extra = set(WHERE) - {(r["sheet"], int(r["sno"])) for r in new}
    if extra:
        raise SystemExit(f"WHERE entries without a sheet row: {sorted(extra)}")
    with open(DRAFT, "w", newline="", encoding="utf-8") as f:
        w_ = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w_.writeheader()
        w_.writerows(rows + new)
    by = {}
    for r in new:
        by[r["status"]] = by.get(r["status"], 0) + 1
    print(f"{len(new)} energy sheet rows written ({by})")


if __name__ == "__main__":
    main()
