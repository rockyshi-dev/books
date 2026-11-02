#!/bin/bash
# Build the shelf: out/index.html plus one MkDocs site per row of books.tsv under out/<slug>/.
#   ./build.sh
set -euo pipefail
cd "$(dirname "$0")"
rm -rf out work && mkdir -p out work
python3 tools/make_index.py books.tsv out/index.html
while IFS=$'\t' read -r slug repo title blurb; do
  [[ -z "$slug" || "$slug" == \#* ]] && continue
  git clone -q --depth 1 "https://github.com/$repo.git" "work/$slug"
  (cd "work/$slug" && pip install -q -r tools/site-requirements.txt && tools/build_site.sh)
  mv "work/$slug/site" "out/$slug"
done < books.tsv
touch out/.nojekyll
echo "shelf built in out/"
