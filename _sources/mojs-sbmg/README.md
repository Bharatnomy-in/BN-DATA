# Swachh Bharat Mission (Grameen) dashboard

Ministry of Jal Shakti, Department of Drinking Water and Sanitation. https://sbm.gov.in/sbmgdashboard/statesdashboard.aspx

- `raw/mojs-sbmg_states-dashboard_<date>.html`: the states dashboard page as served on that date (saved by `pipelines/mojs-sbmg/fetch_dashboard.sh`).
- `match_log.txt`: dashboard districts matched to LGD codes by name rather than by Census 2011 code.

Tables built from it:

- [`WAT_odf-plus-villages_2022-to-2026_STATES_MOJS_DIST`](../../WAT_odf-plus-villages_2022-to-2026_STATES_MOJS_DIST/): ODF Plus village status by district (state-wise table and embedded district data).

Not taken: the dashboard's asset counters (state/national totals only), GP/village search pages (one query per village).
