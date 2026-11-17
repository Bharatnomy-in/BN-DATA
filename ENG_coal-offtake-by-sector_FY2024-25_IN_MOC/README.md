# Coal off-take by consuming sector and coal company, 2024-25

Raw coal sent by each coal company to power plants, steel, cement, sponge iron, bricks and other users, in million tonnes.

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 3, sheet "dt20", Table 4.20 "Company Wise Off-take of Raw Coal to Different Priority Sectors during 2024-25"
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `company` | Coal company as printed (ECL, BCCL, CCL, NCL, WCL, SECL, MCL, NEC are Coal India subsidiaries; `Total CIL`, `Total Public`, `Total Private` are totals) |
| `year` | Financial year (April to March) as printed |
| `power_utility_mt` | Power (utility), million tonnes |
| `power_captive_mt` | Power (captive) |
| `direct_feed_mt` | Direct feed |
| `steel_coke_oven_cokeries_mt` | Steel (coke oven plants & cokeries) |
| `steel_boilers_mt` | Steel (boilers) |
| `cement_mt` | Cement |
| `fertilisers_mt` | Fertilisers |
| `sponge_iron_mt` | Sponge iron |
| `other_basic_metal_mt` | Other basic metal (aluminium etc.) |
| `chemical_mt` | Chemical |
| `pulp_paper_mt` | Pulp & paper |
| `textiles_rayons_mt` | Textiles & rayons |
| `bricks_mt` | Bricks |
| `other_mt` | Other |
| `total_despatch_mt` | Total despatch |
| `colliery_own_consumption_mt` | Colliery own consumption |
| `colliery_staff_mt` | Colliery staff |
| `total_offtake_mt` | Total off-take |

## Notes

- All quantities in million tonnes. Blank cells are blank in the source (nil).
- By company, not by state: **WCL (Western Coalfields) mines are in Maharashtra and Madhya Pradesh and supply the Nagpur region.**
- Checks: sectors add up to total despatch in every row.
