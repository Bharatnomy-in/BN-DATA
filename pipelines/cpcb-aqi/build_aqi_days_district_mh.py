"""Yearly AQI summary per Maharashtra district, pooled over the district's bulletin cities (BNY).

Input:  ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY/<same>.csv   (CPCB daily bulletins, one row per city per day)
        _reference/aqi-cities-maharashtra.csv                    (bulletin city -> district lookup, made by hand)
Output: ENV_aqi-days-by-category_2015-to-2026_MH_BNY_DIST/<same>.csv

A "city-day" is one city on one bulletin day. Counts are summed over the district's cities, so a district
with three monitored cities has up to three city-days per date. Shares are city-days over city-days reported.
Run from the repo root:  python3 pipelines/cpcb-aqi/build_aqi_days_district_mh.py
"""
from pathlib import Path

import pandas as pd

SRC = "ENV_aqi-daily_2015-to-2026_STATES_CPCB_CITY"
XW = "_reference/aqi-cities-maharashtra.csv"
NAME = "ENV_aqi-days-by-category_2015-to-2026_MH_BNY_DIST"
CATS = {"Good": "city_days_good", "Satisfactory": "city_days_satisfactory", "Moderate": "city_days_moderate",
        "Poor": "city_days_poor", "Very Poor": "city_days_very_poor", "Severe": "city_days_severe"}
BIHAR_LABEL_FROM = "2022-05-06"  # first day the bulletin prints "Aurangabad (Bihar)"


def main():
    d = pd.read_csv(Path(SRC) / f"{SRC}.csv", dtype={"aqi": float})
    # Bulletins printed some names in lower case in mid-2026: match case-insensitively.
    xw = pd.read_csv(XW, dtype=str, keep_default_na=False)
    canon = {c.lower(): c for c in xw.city}
    canon.update({"pimpri chinchwad": "Pimpri-Chinchwad"})
    d["city_key"] = d.city.str.lower().map(canon)
    # Plain "Aurangabad": Maharashtra before the bulletin started naming Bihar's, or when both appear that day.
    bihar_days = set(d.loc[d.city.str.lower() == "aurangabad (bihar)", "date"])
    plain = d.city == "Aurangabad"
    keep_plain = (d.date < BIHAR_LABEL_FROM) | d.date.isin(bihar_days)
    dropped = int((plain & ~keep_plain).sum())
    d = d[d.city_key.notna() & ~(plain & ~keep_plain)].copy()
    d = d.merge(xw.drop(columns="note"), left_on="city_key", right_on="city", suffixes=("_printed", ""))
    d["year"] = d.date.str[:4]
    keys = ["state_ut", "lgd_state_code", "district", "lgd_district_code", "year"]
    g = d.groupby(keys)
    out = pd.DataFrame({"cities": g.city.agg(lambda s: "; ".join(sorted(set(s)))),
                        "city_days_reported": g.size()})
    cat = pd.crosstab([d[k] for k in keys], d.air_quality).rename(columns=CATS)
    for c in CATS.values():
        out[c] = cat[c] if c in cat else 0
    out["city_days_aqi_above_100"] = g.aqi.apply(lambda s: int((s > 100).sum()))
    out["city_days_aqi_above_100_pct"] = (100 * out.city_days_aqi_above_100 / out.city_days_reported).round(1)
    out["aqi_mean"] = g.aqi.mean().round(1)
    out["aqi_highest"] = g.aqi.max().astype("Int64")
    out = out.reset_index().sort_values(["district", "year"])
    Path(NAME).mkdir(exist_ok=True)
    out.to_csv(Path(NAME) / f"{NAME}.csv", index=False, lineterminator="\n")
    print(NAME, out.shape, "| plain Aurangabad days dropped as ambiguous:", dropped)
    print("unmatched MH-looking names:", sorted(set(pd.read_csv(Path(SRC) / f"{SRC}.csv", usecols=["city"]).city) - set(d.city_printed))[:0])


if __name__ == "__main__":
    main()
