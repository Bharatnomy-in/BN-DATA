# Main workers by industry, age and sex, every district of India, 2011

Number of main workers (people who worked 6 months or more in the year) in each industry, by age group and sex, total / rural / urban, for every district, state and India. Census 2011 table B-04. Its **mining and quarrying** column is the closest district-level count of the coal-mining workforce (see Notes), and **electricity, gas and water** covers power-plant and utility jobs.

## Source

- **Data:** Office of the Registrar General & Census Commissioner, India (ORGI), Census of India 2011, table B-04 "Main workers classified by age, industrial category and sex" (one file per state/UT plus India, `DDW-B04-<state>00.xls`)
- **Link:** https://censusindia.gov.in/nada/index.php/catalog (catalog ids 43036-43071, idno `PC11_B04-<state>`; e.g. Jharkhand: https://censusindia.gov.in/nada/index.php/catalog/43056)
- **Downloaded:** 18 Nov 2026
- **Original files:** [`_sources/orgi-census2011/raw/b04/`](../_sources/orgi-census2011/raw/b04/) (36 files, 15 MB); catalog ids in [`raw/orgi-census2011_b04-catalog-ids_2011.tsv`](../_sources/orgi-census2011/raw/orgi-census2011_b04-catalog-ids_2011.tsv)
- **Scripts:** [`pipelines/orgi-census2011/fetch_b04.sh`](../pipelines/orgi-census2011/fetch_b04.sh), [`build_b04.py`](../pipelines/orgi-census2011/build_b04.py)

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code` | District rows: today's state and LGD code (from [`_reference/geography.csv`](../_reference/geography.csv)). `State total` rows: the state **as in 2011** (see Notes). `All India` row: blank code |
| `state_census_code` | Census 2011 state code (`00` = India) |
| `district`, `lgd_district_code` | District by today's name and LGD code; `State total` for the state's published total, blank on the India row. LGD code blank for Mahe and Yanam (Puducherry regions LGD does not list as districts) |
| `district_census_code`, `district_census_name` | Census 2011 district code and name as printed |
| `residence` | `Total`, `Rural` or `Urban` |
| `age_group` | `Total`, `5-9`, `10-14`, ... `70-79`, `80+`, `Age not stated` |
| `main_workers_total_*` | All main workers |
| `a_cultivators_*`, `a_agricultural_labourers_*`, `a_plantation_livestock_forestry_fishing_*` | NIC section A: agriculture, split as the Census prints it |
| `b_mining_quarrying_*` | NIC section B: mining and quarrying (coal and lignite, crude oil and gas, metal ores, stone, sand, other minerals) |
| `c_manufacturing_hhi_*`, `c_manufacturing_non_hhi_*` | NIC section C: manufacturing, in household industry (HHI) and outside it |
| `d_e_electricity_gas_water_waste_*` | NIC sections D and E: electricity, gas, steam and air conditioning supply; water supply, sewerage and waste management |
| `f_construction_*` | NIC section F |
| `g_trade_repair_hhi_*`, `g_trade_repair_non_hhi_*` | NIC section G: wholesale and retail trade, repair of motor vehicles, HHI / non-HHI |
| `h_transport_storage_*`, `i_accommodation_food_*` | NIC sections H and I |
| `j_information_communication_hhi_*`, `j_information_communication_non_hhi_*` | NIC section J, HHI / non-HHI (as printed) |
| `k_to_m_finance_real_estate_professional_*` | NIC sections K to M: finance and insurance, real estate, professional, scientific and technical |
| `n_to_o_administrative_public_administration_*` | NIC sections N and O: administrative and support services; public administration and defence |
| `p_to_q_education_health_*` | NIC sections P and Q |
| `r_to_u_other_services_hhi_*`, `r_to_u_other_services_non_hhi_*` | NIC sections R to U: arts, other services, households as employers, extra-territorial bodies, HHI / non-HHI |

Every count has three columns: `_persons`, `_males`, `_females`.

## Notes

- **Mining is not coal alone.** The Census does not split section B by mineral at district level. In the coal belt (e.g. Dhanbad 83,813 mining workers, 15.3% of all main workers; Chandrapur, Karimnagar, Barddhaman, Korba, Angul, Singrauli) it is mostly coal; elsewhere it can be stone, sand, iron ore or oil (e.g. Pakur, 10.2%, is mainly stone quarrying; Jodhpur is sandstone). Cuddalore's is mostly Neyveli lignite.
- **Main workers only.** Marginal workers (less than 6 months' work) are not in this table, so it understates seasonal and informal mining work.
- **The printed header gives only section letters** (A, B, C, D & E, ...); the column names add the standard NIC 2008 section titles.
- **2011 geography.** District rows are the 640 districts of 2011 with today's names, LGD codes and states, so a 2011 Andhra Pradesh district now in Telangana has `state_ut` = Telangana. `State total` rows are the 35 states/UTs of 2011 as published: the Andhra Pradesh total includes today's Telangana, Jammu & Kashmir includes Ladakh, and Dadra & Nagar Haveli and Daman & Diu are separate. Add up district rows by `lgd_state_code` for today's states. Districts created after 2011 are inside their parent (e.g. 2011 Barddhaman is shown as Purba Bardhaman, but it includes today's Paschim Bardhaman, the Raniganj-Asansol coalfield).
- Checks (18 Nov 2026): 28,392 rows = (640 districts + 35 states + India) x Total/Rural/Urban x 14 age groups, minus places with no rural or urban population; no duplicate keys; no negative counts; persons = males + females everywhere; the industry columns add up to `main_workers_total` exactly in every row; rural + urban = total; age groups add up to `Total`; districts add up to their `State total` and the states to `All India` exactly. India: 362,611,115 main workers, of whom 1,801,326 in mining and quarrying and 1,866,613 in electricity, gas and water.
