#!/bin/bash
# Build the shelf: out/index.html plus one MkDocs site per row of books.tsv under out/<slug>/.
#   ./build.sh
set -euo pipefail
cd "$(dirname "$0")"
rm -rf out work && mkdir -p out work
python3 tools/make_index.py books.tsv out/index.html
while IFS=$'\t' read -r slug repo title blurb cover code; do
  [[ -z "$slug" || "$slug" == \#* ]] && continue
  # A public book is cloned over https. A private one is cloned over ssh with the deploy key the workflow writes
  # to $SHELF_KEY (the secret SHELF_DEPLOY_KEY); each private book registers that key as a read-only deploy key.
  if ! GIT_TERMINAL_PROMPT=0 git clone -q --depth 1 "https://github.com/$repo.git" "work/$slug" 2>/dev/null; then
    [[ -n "${SHELF_KEY:-}" ]] || { echo "cannot clone $repo and no deploy key is set" >&2; exit 1; }
    GIT_SSH_COMMAND="ssh -i $SHELF_KEY -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new" \
      git clone -q --depth 1 "git@github.com:$repo.git" "work/$slug"
  fi
  (cd "work/$slug" && pip install -q -r tools/site-requirements.txt && tools/build_site.sh)
  mv "work/$slug/site" "out/$slug"
done < books.tsv
touch out/.nojekyll
echo "shelf built in out/"
