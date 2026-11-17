# Coal despatch by mode of transport, All India, 2015-16 to 2024-25

Raw coal sent from mines by rail, road, conveyor belt, ropeway and merry-go-round (MGR, a dedicated rail loop to a power plant), in million tonnes. External = to consumers; internal = to the company's own washeries, plants and colliery use.

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 3, sheet "dt18", Table 4.18 "Mode Wise Despatch of Raw Coal (External & Internal) in India during last Ten Years"
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | State or UT (standard name); `All India` for the national total; blank for region, sub-total, central-sector and other rows that are not one state |
| `year` | Financial year (April to March) as printed |
| `external_rail_mt` | External despatch by rail, million tonnes |
| `external_road_mt` | External despatch by road, million tonnes |
| `external_belt_mt` | External despatch by conveyor belt, million tonnes |
| `external_rope_mt` | External despatch by ropeway, million tonnes |
| `external_mgr_mt` | External despatch by merry-go-round (MGR; printed "MGE" for internal), million tonnes |
| `external_other_mt` | External despatch by other modes, million tonnes |
| `external_total_mt` | External despatch by all modes (total), million tonnes |
| `internal_rail_mt` | Internal despatch by rail, million tonnes |
| `internal_road_mt` | Internal despatch by road, million tonnes |
| `internal_belt_mt` | Internal despatch by conveyor belt, million tonnes |
| `internal_rope_mt` | Internal despatch by ropeway, million tonnes |
| `internal_mgr_mt` | Internal despatch by merry-go-round (MGR; printed "MGE" for internal), million tonnes |
| `internal_other_mt` | Internal despatch by other modes, million tonnes |
| `internal_total_mt` | Internal despatch by all modes (total), million tonnes |
| `grand_total_mt` | External + internal, million tonnes |

## Notes

- Only the Quantity rows are taken; the Share % rows are computed from them.
- National only: the Coal Directory gives mode-wise despatch by company (Table 4.17), not by state.
- Checks: modes add up to each total; external + internal = grand total.
