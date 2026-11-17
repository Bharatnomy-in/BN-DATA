# Ministry of Coal, Coal Directory of India 2024-25

The Coal Controller's Organisation's yearly statistics on coal and lignite: resources, production, despatch and off-take by sector, stocks, prices, royalty and taxes, imports and exports, washeries, coal blocks and mines. Published as one Excel file per chapter (and a 14 MB PDF of the whole book).

- **Link:** https://coal.gov.in/major-statistics/coal-statistics (no login; the `/en/` version of the page does not list the files)
- **Downloaded:** 17 Nov 2026
- **`raw/`:** `moc-coal-directory_chapter-01_2024-25.xlsx` ... `chapter-11` (the site's `cdchap1.xlsx` ... `cdchap11.xlsx`). Chapter numbers of the files differ from the table numbers inside (file 2 holds chapter 3 tables, etc.)
- **Scripts:** [`pipelines/moc-coal-directory/build_coal_directory.py`](../../pipelines/moc-coal-directory/build_coal_directory.py), [`check_coal_directory.py`](../../pipelines/moc-coal-directory/check_coal_directory.py)

## Tables taken

| File / sheet | Table | Folder |
|---|---|---|
| 01 / 2.2 | 2.2 State-wise geological resources of coal | [`ENG_coal-resources_2005-to-2025_STATES_MOC`](../../ENG_coal-resources_2005-to-2025_STATES_MOC/) |
| 02 / PT9 | 3.9 State-wise raw coal production, ten years | [`ENG_coal-production_2015-16-to-2024-25_STATES_MOC`](../../ENG_coal-production_2015-16-to-2024-25_STATES_MOC/) |
| 02 / PT10 | 3.10 State-wise lignite production, ten years | [`ENG_lignite-production_2015-16-to-2024-25_STATES_MOC`](../../ENG_lignite-production_2015-16-to-2024-25_STATES_MOC/) |
| 02 / PT25 | 3.25 State-wise production by type of mine | [`ENG_coal-production-by-mine-type_2021-22-to-2024-25_STATES_MOC`](../../ENG_coal-production-by-mine-type_2021-22-to-2024-25_STATES_MOC/) |
| 03 / dt7 | 4.7 State-wise raw coal despatch, ten years | [`ENG_coal-despatch_2014-15-to-2024-25_STATES_MOC`](../../ENG_coal-despatch_2014-15-to-2024-25_STATES_MOC/) |
| 03 / dt18 | 4.18 Mode-wise despatch, All India | [`ENG_coal-despatch-by-mode_2015-16-to-2024-25_IN_MOC`](../../ENG_coal-despatch-by-mode_2015-16-to-2024-25_IN_MOC/) |
| 03 / dt20 | 4.20 Company-wise off-take to priority sectors | [`ENG_coal-offtake-by-sector_FY2024-25_IN_MOC`](../../ENG_coal-offtake-by-sector_FY2024-25_IN_MOC/) |
| 03 / dt21 | 4.21 Despatch from source state to destination state | [`ENG_coal-despatch-source-destination_FY2024-25_STATES_MOC`](../../ENG_coal-despatch-source-destination_FY2024-25_STATES_MOC/) |
| 06 / tb7.2&3 | 7.2 State-wise royalty, DMF, NMET and taxes, 2024-25 | [`ENG_coal-royalty-dmf-taxes_FY2024-25_STATES_MOC`](../../ENG_coal-royalty-dmf-taxes_FY2024-25_STATES_MOC/) |
| 06 / tb7.7 | 7.7 State-wise royalty, DMF, NMET, three years | [`ENG_coal-royalty-dmf-nmet_2022-23-to-2024-25_STATES_MOC`](../../ENG_coal-royalty-dmf-nmet_2022-23-to-2024-25_STATES_MOC/) |
| 07 / TB8.5 | 8.5 Port-wise imports of coal and coke | [`ENG_coal-imports-by-port_FY2024-25_IN_MOC`](../../ENG_coal-imports-by-port_FY2024-25_IN_MOC/) |
| 11 / tab12.2 | 12.2 State-wise number of coal and lignite mines | [`ENG_coal-lignite-mines_2025-03_STATES_MOC`](../../ENG_coal-lignite-mines_2025-03_STATES_MOC/) |

## Not taken yet

About 120 other sheets: lignite resources (2.6), field-, depth- and grade-wise resources, exploration, company-wise and grade-wise production and despatch, monthly series, pit-head stocks (chapter 4 file), pit-head values and prices (chapter 5 file), company-wise royalty, import/export by country and month, steel plants and washeries, captive blocks, world coal statistics, and mines by company and owner (12.1, 12.3-12.9). Some sheets are leftovers from older editions (names ending `_Revised`, `del`, `word calculation`); check the title row before using them.
