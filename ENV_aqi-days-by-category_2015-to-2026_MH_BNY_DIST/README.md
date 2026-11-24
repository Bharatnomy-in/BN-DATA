# Air quality days by district, Maharashtra, 2015 to 2026

Per Maharashtra district and year: how many city-days the CPCB daily AQI bulletin put the district's monitored cities in each AQI category, the share of city-days with AQI above 100, and the mean and highest AQI. Pooled by Bharatnomy over the cities of each district.

## Source

- **Data:** Central Pollution Control Board (CPCB), National Air Quality Index daily bulletins (4 pm)
- **Built from:** [`ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY`](../ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY/) and the city-to-district lookup [`_reference/aqi-cities-maharashtra.csv`](../_reference/aqi-cities-maharashtra.csv)
- **Link:** https://cpcb.nic.in/AQI_Bulletin.php
- **Downloaded:** 28 Oct 2026 (bulletins); counted 24 Nov 2026
- **Script:** [`pipelines/cpcb-aqi/build_aqi_days_district_mh.py`](../pipelines/cpcb-aqi/build_aqi_days_district_mh.py)

## How it is computed

A city-day is one bulletin city on one day. Each city is assigned to one district (lookup above, made by hand). Counts are summed over the district's cities, so Thane, with up to eight bulletin cities, has up to eight city-days per date. `city_days_aqi_above_100_pct` = `city_days_aqi_above_100` / `city_days_reported` x 100. `aqi_mean` is the mean over all city-days.

## Columns

| Column | Meaning |
|---|---|
| `state_ut`, `lgd_state_code` | Maharashtra, 27 |
| `district`, `lgd_district_code` | Current LGD district name and code |
| `year` | Calendar year |
| `cities` | Bulletin cities counted, `; `-separated |
| `city_days_reported` | City-days in the bulletin that year |
| `city_days_good` ... `city_days_severe` | City-days in each AQI category as printed: Good (0-50), Satisfactory (51-100), Moderate (101-200), Poor (201-300), Very Poor (301-400), Severe (401-500) |
| `city_days_aqi_above_100` | City-days with AQI above 100 (Moderate or worse), counted from the AQI value |
| `city_days_aqi_above_100_pct` | Share of reported city-days with AQI above 100, % |
| `aqi_mean`, `aqi_highest` | Mean and highest AQI over the city-days |

## Notes

- Only districts with a bulletin city appear: 9 districts from 2015-16 (Mumbai, Mumbai Suburban, Thane, Pune, Nagpur, Nashik, Solapur, Chandrapur, Chhatrapati Sambhajinagar), about 25 from 2023. A missing district-year means no monitor in the bulletin, not clean air.
- 2015 starts on 1 May, 2026 ends on 27 Oct: both are part years.
- The bulletin city `Mumbai` covers stations in both Mumbai and Mumbai Suburban districts and is counted in both, so the two rows are identical.
- `Navi Mumbai` and `Belapur` are counted in Thane (most of the Navi Mumbai area); `Virar` and `Boisar` in Palghar (carved from Thane in 2014).
- `Aurangabad`: the bulletin printed the name without a state until it started adding `(Bihar)` on 6 May 2022. Plain `Aurangabad` is counted as Chhatrapati Sambhajinagar before that date, or on days when `Aurangabad (Bihar)` also appears; 13 other plain-label days are left out as ambiguous. The bulletin has no Maharashtra Aurangabad in 2023-2025.
- Checks (24 Nov 2026): 154 rows (district x year), no duplicate keys; category city-days add up to `city_days_reported` in every row; shares within 0-100.
