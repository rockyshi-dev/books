# Books

The shelf behind https://book.rockyshi.dev. Each row of `books.tsv` is one book: its path under the site, the GitHub
repository it is built from, its title and a one-line description. `build.sh` clones every repository, runs its
`tools/build_site.sh` (MkDocs) and places the result at `/<slug>/`, next to a home page that lists the books.
The site is rebuilt on every push here and once a day, so a book's latest `main` appears within a day; run the
workflow by hand to publish sooner.

A book whose repository is private is cloned over ssh with a read-only deploy key: the private half is the
secret `SHELF_DEPLOY_KEY` of this repository, the public half is registered as a deploy key on the book's repository.

To add a book, append a row to `books.tsv`. The book's `mkdocs.yml` sets `site_url` to
`https://book.rockyshi.dev/<slug>/`.
