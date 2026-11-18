#!/bin/sh
# Download Census 2011 B-04 (main workers classified by age, industrial category and sex) for India and every
# state/UT from the Census NADA catalog (36 files, about 20 MB). Catalog ids: raw/orgi-census2011_b04-catalog-ids_2011.tsv
# (found with the catalog search API, query "B-04", 18 Nov 2026; idno PC11_B04-<state code>, 00 = India).
# Run from the repo root:  sh pipelines/orgi-census2011/fetch_b04.sh
R=_sources/orgi-census2011/raw
OUT=$R/b04
mkdir -p "$OUT"
tail -n +2 "$R/orgi-census2011_b04-catalog-ids_2011.tsv" | while IFS="$(printf '\t')" read -r id idno title; do
  st=${idno##*-}
  page=$(curl -sL -m 60 -A "Mozilla/5.0" "https://censusindia.gov.in/nada/index.php/catalog/$id/related-materials")
  dl=$(printf '%s' "$page" | grep -oE "catalog/$id/download/[0-9]+" | head -1)
  name=$(printf '%s' "$page" | grep -oE '[A-Za-z0-9_-]+\.(xlsx|xls)' | head -1)
  ext=${name##*.}
  f="$OUT/orgi-census2011_b04-state-${st}_2011.${ext:-xls}"
  [ -s "$f" ] || curl -sL --retry 3 -m 300 -A "Mozilla/5.0" "https://censusindia.gov.in/nada/index.php/$dl" -o "$f"
  echo "$id $idno $name -> $f"
  sleep 0.3
done
