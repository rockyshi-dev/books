"""Write the shelf's home page from books.tsv (slug, repository, title, description per row)."""
import csv
import html
import os
import shutil
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
.book {{ display: flex; gap: 1.5rem; align-items: flex-start; padding: 1.25rem; margin: 0 0 1.25rem;
  border: 1px solid var(--line); border-radius: 8px; }}
.book img {{ flex: none; width: 150px; height: auto; border-radius: 4px; display: block; }}
.book h2 {{ font-size: 1.2rem; line-height: 1.35; margin: 0 0 .5rem; }}
.book h2 a {{ color: var(--accent); text-decoration: none; }}
.book p {{ margin: 0 0 1rem; color: var(--muted); font-size: .95rem; }}
.links a {{ display: inline-block; margin-right: .6rem; padding: .3rem .8rem; border: 1px solid var(--accent);
  border-radius: 6px; color: var(--accent); text-decoration: none; font-size: .9rem; }}
.links a:hover {{ background: var(--accent); color: var(--bg); }}
@media (max-width: 34rem) {{ .book {{ flex-direction: column; }} .book img {{ width: 55%; }} }}
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

CARD = (
    '<section class="book"><a href="{slug}/"><img src="{cover}" alt="Cover of {title}"></a>'
    '<div><h2><a href="{slug}/">{title}</a></h2><p>{desc}</p>'
    '<div class="links"><a href="{slug}/">Read online</a><a href="{code}">Code</a></div></div></section>'
)


def main(src, dst):
    cards = []
    out = os.path.dirname(dst)
    with open(src, newline="") as f:
        for row in csv.reader((l for l in f if not l.startswith("#") and l.strip()), delimiter="\t"):
            slug, _repo, title, desc, cover, code = row
            os.makedirs(os.path.join(out, os.path.dirname(cover)), exist_ok=True)
            shutil.copy(cover, os.path.join(out, cover))
            cards.append(CARD.format(slug=html.escape(slug), title=html.escape(title), desc=html.escape(desc),
                                     cover=html.escape(cover), code=html.escape(code)))
    with open(dst, "w") as f:
        f.write(PAGE.format(books="\n".join(cards)))


main(sys.argv[1], sys.argv[2])
