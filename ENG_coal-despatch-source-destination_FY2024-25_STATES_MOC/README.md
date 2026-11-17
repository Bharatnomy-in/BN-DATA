# Coal despatched from each producing state to each receiving state, 2024-25

Where each state's coal comes from: raw coal sent from the mines of a source state to a destination state, in million tonnes.

## Source

- **Data:** Ministry of Coal (Coal Controller's Organisation), *Coal Directory of India 2024-25*, Excel chapter files
- **Table taken from:** Chapter 3, sheet "dt21", Table 4.21 "Raw Coal Despatch Source State to Destination State in India during 2024-25"
- **Link:** https://coal.gov.in/major-statistics/coal-statistics
- **Downloaded:** 17 Nov 2026 (original in [`_sources/moc-coal-directory/raw/`](../_sources/moc-coal-directory/raw/) (11 chapter files))
- **Script:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../pipelines/moc-coal-directory/build_coal_directory.py); checks in `check_coal_directory.py`

## Columns

| Column | Meaning |
|---|---|
| `state_ut` | Destination state (standard name); `All India` for the total row |
| `lgd_state_code` | State/UT code in the Local Government Directory (LGD), from [`_reference/geography.csv`](../_reference/geography.csv). Blank for All India and for old units LGD no longer lists |
| `source_state` | Source state (where the coal was mined); `All India` = the destination's total from all sources |
| `year` | Financial year (April to March) as printed |
| `despatch_mt` | Raw coal despatched, million tonnes |
| `destination_as_printed` | Destination as printed |
| `source_state_as_printed` | Source as printed |

## Notes

- The source matrix (destinations in rows, source states in columns) is stored long; blank matrix cells (no coal from that state) are left out.
- The "Share %" column is left out.
- Checks: sources add up to each destination's total.
- **Nagpur / Maharashtra:** filter `state_ut` = `Maharashtra`.
- `lgd_state_code` added on 17 Nov 2026 from the LGD directory (see [`_reference/README.md`](../_reference/README.md)). LGD codes identify today's state or district; for years before a split (Telangana 2014, Ladakh 2019, new districts) the same code covers a larger area than it does now.
