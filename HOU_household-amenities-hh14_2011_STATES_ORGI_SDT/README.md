# Household amenities and assets by district and sub-district, India, 2011

The same 135 HH-14 indicators as [`HOU_household-amenities-hh14_2011_STATES_ORGI_DIST`](../HOU_household-amenities-hh14_2011_STATES_ORGI_DIST/), for every district **and sub-district (tehsil / taluk / mandal / block)** of India, total / rural / urban.

## Source

- **Data:** Office of the Registrar General & Census Commissioner, India (ORGI), Census of India 2011, Houselisting and Housing Census, table HH-14 "Percentage of households to total households by amenities and assets" (one file per district, `HLPCA-<state><district>-2011_H14_census.xlsx`)
- **Link:** https://censusindia.gov.in/nada/index.php/catalog (catalog ids 9236-9938, idno `PC11_HL14-<state>-<district>`; e.g. Nagpur: https://censusindia.gov.in/nada/index.php/catalog/9803)
- **Downloaded:** 18 Nov 2026
- **Original files:** 640 files, about 550 MB, not committed (too large); `_sources/orgi-census2011/raw/hl14/` after running the fetch script. Catalog ids: [`_sources/orgi-census2011/raw/orgi-census2011_hl14-catalog-ids_2011.tsv`](../_sources/orgi-census2011/raw/orgi-census2011_hl14-catalog-ids_2011.tsv)
- **Scripts:** [`pipelines/orgi-census2011/fetch_hl14.sh`](../pipelines/orgi-census2011/fetch_hl14.sh), [`build_hl14.py`](../pipelines/orgi-census2011/build_hl14.py) (writes this table and its district-only twin)

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code` | State/UT by today's name and LGD code (from [`_reference/geography.csv`](../_reference/geography.csv), via the Census 2011 district code) |
| `state_census_code` | Census 2011 state code |
| `district`, `lgd_district_code` | District by its current name and LGD code (from [`_reference/geography.csv`](../_reference/geography.csv)); blank LGD code for Mahe and Yanam (Puducherry regions LGD does not list as districts) |
| `district_census_code`, `district_census_name` | Census 2011 district code and name |
| `area_level` | `district` or `sub-district` |
| `subdistrict`, `subdistrict_census_code` | Sub-district (tehsil) name and Census 2011 code; blank on district rows |
| `residence` | `Total`, `Rural` or `Urban` |
| `house_condition_<use>_<condition>_pct` | Households by condition of the census house (`good`, `livable`, `dilapidated`, `total`), for all houses (`total`), houses used only as residence (`residence`) and residence-cum-other use, % of households |
| `roof_*_pct`, `wall_*_pct`, `floor_*_pct` | Households by predominant material of roof / wall / floor, % (e.g. `roof_g_i_metal_asbestos_sheets_pct`, `roof_grass_thatch_bamboo_wood_mud_etc_pct`, `roof_concrete_pct`) |
| `dwelling_rooms_*_pct`, `household_size_*_pct`, `married_couples_*_pct` | Households by number of dwelling rooms, persons, married couples, % |
| `ownership_owned_pct`, `ownership_rented_pct`, `ownership_any_others_pct` | Ownership of the house, % |
| `drinking_water_source_*_pct` | Main source of drinking water (treated / untreated tap water, wells, handpump, tubewell, spring, river, tank, other), % |
| `drinking_water_location_within_premises_pct`, `_near_premises_pct`, `_away_pct` | Location of the drinking water source, % |
| `lighting_*_pct` | Main source of lighting (electricity, kerosene, solar, other oil, any other, none), % |
| `latrine_within_premises_total_pct` and `latrine_flush_*`, `latrine_pit_*`, `latrine_night_soil_open_drain_pct`, `latrine_service_*` | Households with a latrine within the premises, and by type, % |
| `latrine_none_within_premises_total_pct`, `latrine_none_public_latrine_pct`, `latrine_none_open_pct` | Households without a latrine within the premises, and what they use instead, % |
| `bathing_*_pct`, `waste_water_*_pct` | Bathing facility within premises (bathroom / enclosure without roof / none); waste water outlet (closed / open / no drainage), % |
| `cooking_fuel_*_pct` | Fuel used for cooking (fire-wood, crop residue, cowdung cake, coal, kerosene, LPG/PNG, electricity, biogas, other, no cooking), % |
| `kitchen_*_pct` | Cooking inside / outside the house, with or without a kitchen, % |
| `banking_services_availed_pct` | Households availing banking services, % |
| `assets_*_pct` | Households with radio, TV, computer (with / without internet), phone (landline / mobile / both), bicycle, two-wheeler, car, all of TV-computer-phone-vehicle, none of these, % |
| `house_structure_*_pct` | Type of structure: permanent, semi-permanent, temporary (total, serviceable, non-serviceable), unclassifiable, % |

## Notes

- **2011 geography.** Rows are the 640 districts of Census 2011 (and their sub-districts). Districts created later (e.g. Palghar from Thane) are inside their 2011 parent. State and district names and LGD codes are today's: a 2011 Andhra Pradesh district now in Telangana has `state_ut` = Telangana; `state_census_code` keeps the 2011 state.
- Fully urban districts (e.g. Mumbai, Mumbai Suburban, Chennai, Kolkata, Hyderabad) have no `Rural` row; a few fully rural ones have no `Urban` row.
- Values are percentages as printed (one decimal). A category group adds up to 100 within rounding.
- The same files also have town, ward and village rows; these are not converted yet.
- [`HOU_household-amenities-hh14_2011_MH_ORGI_DIST`](../HOU_household-amenities-hh14_2011_MH_ORGI_DIST/) and `_SDT` (Maharashtra only) are the same data for one state, kept because they were published first.
- Checks (18 Nov 2026): 17,046 rows (1,908 district + 15,138 sub-district rows); no duplicate keys (`district_census_code`, `area_level`, `subdistrict_census_code`, `residence`); all values 0-100.
