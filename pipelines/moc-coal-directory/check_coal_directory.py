"""Checks for the Coal Directory 2024-25 tables (run from the repo root after build_coal_directory.py).

For every table: duplicate keys, state names, numbers parse, negatives. Printed totals recomputed:
states vs All India, Gondwana states vs "Total Gondwana", CIL + non-CIL vs Total, open cast + underground vs total,
port rows vs Total, company rows vs Total CIL / Grand Total, source-destination rows vs each destination's Total.
Differences above rounding are listed, never corrected.
"""
import pandas as pd

STATES = set("""Andaman & Nicobar Islands|Andhra Pradesh|Arunachal Pradesh|Assam|Bihar|Chandigarh|Chhattisgarh|Dadra & Nagar Haveli and Daman & Diu|Delhi|Goa|Gujarat|Haryana|Himachal Pradesh|Jammu & Kashmir|Jharkhand|Karnataka|Kerala|Ladakh|Lakshadweep|Madhya Pradesh|Maharashtra|Manipur|Meghalaya|Mizoram|Nagaland|Odisha|Puducherry|Punjab|Rajasthan|Sikkim|Tamil Nadu|Telangana|Tripura|Uttar Pradesh|Uttarakhand|West Bengal|All India|Dadra & Nagar Haveli|Daman & Diu""".split("|"))


def load(n):
    d = pd.read_csv(f"{n}/{n}.csv", dtype=str, keep_default_na=False)
    num = [c for c in d.columns if c.endswith(("_mt", "_inr_crore", "_count", "_inr_million", "_usd_million"))]
    v = d[num].replace("", None).apply(pd.to_numeric, errors="coerce")
    return d, num, v


def basic(n, keys):
    d, num, v = load(n)
    print(f"\n== {n}: {d.shape[0]} rows x {d.shape[1]} cols")
    print("  duplicate keys:", int(d.duplicated(keys).sum()), "| bad state_ut:", sorted(set(d.state_ut) - STATES - {""}),
          "| non-numeric:", int((v.isna() & (d[num] != "")).sum().sum()), "| negatives:", int((v < 0).sum().sum()),
          "| blank cells:", int((d[num] == "").sum().sum()))
    return d, num, v


def compare(label, got, want, tol):
    bad = [(k, round(a, 3), round(b, 3)) for k, a, b in zip(got.index, got, want) if pd.notna(b) and abs(a - b) > tol]
    print(f"  {label}: {len(bad)} differences over {tol}", bad[:6])


def states_vs_total(d, v, by, cols, tol=0.01):
    for c in cols:
        sub = d.state_ut.ne("All India") & d.state_ut.ne("")
        got = v[sub].groupby([d.loc[sub, b] for b in by])[c].sum()
        want = v[d.state_ut == "All India"].set_index([d.loc[d.state_ut == "All India", b] for b in by])[c]
        compare(f"states summed vs All India [{c}]", got.reindex(want.index).fillna(0), want, tol)


d, num, v = basic("ENG_coal-resources_2005-to-2025_STATES_MOC", ["state_as_printed", "coalfield_type", "date"])
print("  proved + indicated + inferred = total, rows off by > 0.05:",
      int(((v.proved_mt.fillna(0) + v.indicated_mt.fillna(0) + v.inferred_mt.fillna(0) - v.total_mt).abs() > 0.05).sum()))
for typ, tot in (("Gondwana", "Total Gondwana"), ("Tertiary", "Total Tertiary")):
    m = (d.coalfield_type == typ) & d.state_ut.ne("") & d.state_ut.ne("All India")
    got = v[m].groupby(d.loc[m, "date"]).total_mt.sum()
    t = d.state_as_printed.str.replace("\n", " ").eq(tot)
    want = v[t].set_index(d.loc[t, "date"]).total_mt
    compare(f"{typ} states vs '{tot}' (dates in both)", got.reindex(want.index).fillna(0), want, 0.5)

for n, col in (("ENG_coal-production_2015-16-to-2024-25_STATES_MOC", "production_mt"),
               ("ENG_lignite-production_2015-16-to-2024-25_STATES_MOC", "production_mt"),
               ("ENG_coal-despatch_2014-15-to-2024-25_STATES_MOC", "despatch_mt")):
    d, num, v = basic(n, ["state_ut", "year"])
    states_vs_total(d, v, ["year"], [col])

d, num, v = basic("ENG_coal-production-by-mine-type_2021-22-to-2024-25_STATES_MOC", ["state_ut", "year"])
print("  open cast + underground = total, rows off by > 0.002:",
      int(((v.open_cast_mt.fillna(0) + v.underground_mt.fillna(0) - v.total_mt).abs() > 0.002).sum()))
states_vs_total(d, v, ["year"], ["total_mt"])

d, num, v = basic("ENG_coal-despatch-by-mode_2015-16-to-2024-25_IN_MOC", ["year"])
for side in ("external", "internal"):
    parts = [c for c in num if c.startswith(side) and not c.endswith("total_mt")]
    print(f"  {side} modes = {side} total, rows off by > 0.01:", int(((v[parts].fillna(0).sum(axis=1) - v[f"{side}_total_mt"]).abs() > 0.01).sum()))
print("  external + internal = grand total, rows off by > 0.01:",
      int(((v.external_total_mt + v.internal_total_mt - v.grand_total_mt).abs() > 0.01).sum()))

d, num, v = basic("ENG_coal-offtake-by-sector_FY2024-25_IN_MOC", ["company"])
sec = [c for c in num if c not in ("total_despatch_mt", "colliery_own_consumption_mt", "colliery_staff_mt", "total_offtake_mt")]
print("  sectors = total despatch, rows off by > 0.01:", int(((v[sec].fillna(0).sum(axis=1) - v.total_despatch_mt).abs() > 0.01).sum()))
print("  company labels:", " | ".join(d.company))

d, num, v = basic("ENG_coal-despatch-source-destination_FY2024-25_STATES_MOC", ["state_ut", "destination_as_printed", "source_state"])
m = d.source_state.ne("All India")
got = v[m].groupby(d.loc[m, "destination_as_printed"]).despatch_mt.sum()
want = v[~m].set_index(d.loc[~m, "destination_as_printed"]).despatch_mt
compare("sources summed vs each destination's Total", got.reindex(want.index).fillna(0), want, 0.01)

d, num, v = basic("ENG_coal-royalty-dmf-taxes_FY2024-25_STATES_MOC", ["state_ut"])
states_vs_total(d, v, ["year"], [c for c in num])
parts = [c for c in num if c != "total_inr_crore"]
print("  items = total, rows off by > 0.01:", int(((v[parts].fillna(0).sum(axis=1) - v.total_inr_crore).abs() > 0.01).sum()))

d, num, v = basic("ENG_coal-royalty-dmf-nmet_2022-23-to-2024-25_STATES_MOC", ["state_as_printed", "company_type", "year"])
for c in num:
    k = ["state_as_printed", "year"]
    parts = d.company_type.isin(["CIL", "Non-CIL"])
    got = v[parts].groupby([d.loc[parts, x] for x in k])[c].sum(min_count=1)
    tot = d.company_type == "Total"
    want = v[tot].set_index([d.loc[tot, x] for x in k])[c]
    compare(f"CIL + Non-CIL vs Total [{c}]", got.reindex(want.index).fillna(0), want, 0.01)
    t2 = tot & d.state_ut.ne("All India")
    got = v[t2].groupby(d.loc[t2, "year"])[c].sum()
    want = v[tot & d.state_ut.eq("All India")].set_index(d.loc[tot & d.state_ut.eq("All India"), "year"])[c]
    compare(f"state Totals vs All India Total [{c}]", got.reindex(want.index), want, 0.01)

d, num, v = basic("ENG_coal-lignite-mines_2025-03_STATES_MOC", ["state_ut", "mineral"])
for c in num:
    for mineral in ("coal", "lignite"):
        m = d.mineral.eq(mineral)
        got = v[m & d.state_ut.ne("All India")][c].sum()
        want = v[m & d.state_ut.eq("All India")][c].iloc[0]
        if abs(got - want) > 0 and pd.notna(want):
            print(f"  {mineral} states vs All India [{c}]: {got} vs {want}")
for g in ("producing", "non_producing", "operational"):
    parts = [f"{g}_{k}_count" for k in ("open_cast", "underground", "mixed")]
    print(f"  {g}: OC + UG + mixed = total, rows off:", int((v[parts].fillna(0).sum(axis=1) != v[f"{g}_total_count"]).sum()))

d, num, v = basic("ENG_coal-imports-by-port_FY2024-25_IN_MOC", ["port"])
t = d.port == "Total"
got = v[~t].sum()
compare("ports summed vs Total", got, v[t].iloc[0], 0.01)
