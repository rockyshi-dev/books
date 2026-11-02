"""Write the shelf's home page from books.tsv (slug, repository, title, description per row)."""
import csv
import html
import sys

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Books by Rocky Shi</title>
<style>
:root {{ --bg: #fff; --fg: #1d1f23; --muted: #5b616b; --line: #d9dce1; --accent: #2b6cb0; }}
@media (prefers-color-scheme: dark) {{
  :root {{ --bg: #16181c; --fg: #e6e8eb; --muted: #9aa1ab; --line: #2c3037; --accent: #7fb2ee; }}
}}
body {{ margin: 0; background: var(--bg); color: var(--fg);
  font: 17px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif; }}
main {{ max-width: 46rem; margin: 0 auto; padding: 3rem 1rem; }}
h1 {{ font-size: 1.8rem; margin: 0 0 .25rem; }}
.sub {{ color: var(--muted); margin: 0 0 2.5rem; }}
a.book {{ display: block; padding: 1.1rem 1.25rem; margin: 0 0 1rem; border: 1px solid var(--line);
  border-radius: 8px; color: inherit; text-decoration: none; }}
a.book:hover {{ border-color: var(--accent); }}
a.book strong {{ display: block; font-size: 1.15rem; color: var(--accent); }}
a.book span {{ color: var(--muted); font-size: .95rem; }}
footer {{ margin-top: 3rem; color: var(--muted); font-size: .9rem; }}
footer a {{ color: var(--muted); }}
</style>
</head>
<body>
<main>
<h1>Books</h1>
<p class="sub">Hands-on guides by Rocky Shi, with the code and the measurements behind them.</p>
{books}
<footer><a href="https://rockyshi.dev">Blog</a> &middot; <a href="https://github.com/rockyshi-dev">GitHub</a></footer>
</main>
</body>
</html>
"""

CARD = '<a class="book" href="{slug}/"><strong>{title}</strong><span>{desc}</span></a>'


def main(src, dst):
    cards = []
    with open(src, newline="") as f:
        for row in csv.reader((l for l in f if not l.startswith("#") and l.strip()), delimiter="\t"):
            slug, _repo, title, desc = row
            cards.append(CARD.format(slug=html.escape(slug), title=html.escape(title), desc=html.escape(desc)))
    with open(dst, "w") as f:
        f.write(PAGE.format(books="\n".join(cards)))


main(sys.argv[1], sys.argv[2])
