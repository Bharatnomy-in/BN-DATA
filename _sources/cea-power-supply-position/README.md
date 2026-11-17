# CEA Power Supply Position reports (peak and energy)

Original files for [`ENG_peak-demand_2013-01-to-2026-08_STATES_CEA/`](../../ENG_peak-demand_2013-01-to-2026-08_STATES_CEA/) and [`ENG_energy-supply-position_2013-01-to-2026-08_STATES_CEA/`](../../ENG_energy-supply-position_2013-01-to-2026-08_STATES_CEA/).

- **Link:** https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1003&subSubHeadingId=10011&title=Power%20Supply%20Position%20-%20Peak&lang=en (no login)
- **Downloaded:** 12 Nov 2026
- **`raw/`:** [`cea-psp_peak_file-list.tsv`](raw/cea-psp_peak_file-list.tsv) (month and CEA file id of each report, from the page above). The 164 monthly PDFs (`cea-psp_peak_YYYY-MM.pdf`, about 50 MB) are not committed: run `sh pipelines/cea/fetch_psp_peak.sh` from the repo root to download them. The 2015-09 file is empty on CEA's server.
- **Scripts:** [`pipelines/cea/fetch_psp_peak.sh`](../../pipelines/cea/fetch_psp_peak.sh), [`pipelines/cea/build_psp_peak.py`](../../pipelines/cea/build_psp_peak.py)
- **Energy reports** (added 17 Nov 2026): https://cea.nic.in/reports/dashboardView?headingId=107&subHeadingId=1003&subSubHeadingId=10010&title=Power%20Supply%20Position%20-%20Energy&lang=en . [`raw/cea-psp_energy_file-list.tsv`](raw/cea-psp_energy_file-list.tsv) lists the 164 files; the PDFs (`cea-psp_energy_YYYY-MM.pdf`, about 56 MB) are not committed: run `sh pipelines/cea/fetch_psp_energy.sh`. 61 of the files listed for 2014-05 to 2020-03 are generation reports, not energy reports (list in the dataset README).
- **Scripts (energy):** [`pipelines/cea/fetch_psp_energy.sh`](../../pipelines/cea/fetch_psp_energy.sh), [`pipelines/cea/build_psp_energy.py`](../../pipelines/cea/build_psp_energy.py), [`pipelines/cea/check_psp_energy.py`](../../pipelines/cea/check_psp_energy.py)
