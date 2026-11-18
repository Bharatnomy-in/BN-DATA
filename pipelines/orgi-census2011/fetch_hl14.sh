#!/bin/sh
# Download Census 2011 HL-14 (percentage of households by amenities and assets) for every district of
# India from the Census NADA catalog (640 files, about 0.8 GB; too large to commit, so raw/hl14/ is
# git-ignored). Catalog ids: raw/orgi-census2011_hl14-catalog-ids_2011.tsv (found with the catalog
# search API, queries "HLPCA" and "amenities and assets", 18 Nov 2026; idno PC11_HL14-<state>-<district>).
# Run from the repo root:  sh pipelines/orgi-census2011/fetch_hl14.sh
R=_sources/orgi-census2011/raw
OUT=$R/hl14
mkdir -p "$OUT"
fetch_one() {
  id=$1; idno=$2
  dist=${idno##*-}
  f="$OUT/orgi-census2011_hl14-district-${dist}_2011.xlsx"
  [ -s "$f" ] && return 0
  page=$(curl -sL -m 60 -A "Mozilla/5.0" "https://censusindia.gov.in/nada/index.php/catalog/$id/related-materials")
  dl=$(printf '%s' "$page" | grep -oE "catalog/$id/download/[0-9]+" | head -1)
  [ -z "$dl" ] && { echo "NO LINK $id $idno"; return 0; }
  curl -sL --retry 3 -m 300 -A "Mozilla/5.0" "https://censusindia.gov.in/nada/index.php/$dl" -o "$f.part" && mv "$f.part" "$f"
  echo "$id $idno -> $f"
}
export OUT; export -f fetch_one 2>/dev/null || true
tail -n +2 "$R/orgi-census2011_hl14-catalog-ids_2011.tsv" | cut -f1,2 | while IFS="$(printf '\t')" read -r id idno; do
  fetch_one "$id" "$idno" &
  # at most 6 downloads at a time
  while [ "$(jobs -r | wc -l)" -ge 6 ]; do sleep 0.2; done
done
wait
