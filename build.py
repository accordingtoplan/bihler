"""Build prototype V1: index.html plus one page per project in projekte/.

Inlines the original Bihler logo. Project data from data.js, images from img/.
"""
import os, re, json, html
os.chdir(os.path.dirname(os.path.abspath(__file__)))

src = open('index.src.html').read()
logo = open('logo-inline.svg').read()

P = json.loads(re.search(r'window\.PROJECTS=(.*?);\n', open('data.js').read(), re.S).group(1))
css = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
fonts = re.search(r'(<link rel="preconnect".*?display=swap">)', src, re.S).group(1)
word = logo.replace('viewBox="0 0 127 85"', 'viewBox="0 0 127 59"')
open('index.html', 'w').write(src.replace('%%LOGO%%', logo).replace('%%WORD%%', word))

# one footer for every page: taken from index.src.html, links pointed back at the homepage
footer = re.search(r'<footer.*?</footer>', src, re.S).group(0).replace('%%WORD%%', word)
footer = footer.replace('href="#top"', 'href="../index.html"').replace('href="#', 'href="../index.html#').replace('href="projekte/', 'href="')
e = html.escape
yr = lambda p: (re.search(r'\d{4}', p['facts'].get('Fertigstellung', '')) or [''])[0]
img = lambda i: '../' + i

os.makedirs('projekte', exist_ok=True)
for f in os.listdir('projekte'):
    if f.endswith('.html'):
        os.remove(os.path.join('projekte', f))

def card(q):
    meta = f'<b>{e(q["name"])}</b><span>{e(q["facts"].get("Ort", ""))}</span><span>{yr(q)}</span>'
    return (f'<a class="card" href="{q["id"]}.html"><div class="ph"><img src="{img(q["imgs"][0])}" alt="{e(q["name"])}" loading="lazy"></div>'
            f'<h3>{e(q["head"])}</h3><div class="meta">{meta}</div></a>')

def page(p, i):
    same = [q for q in P if q['sector'] == p['sector'] and q['id'] != p['id'] and q['privat'] == p['privat']]
    more = (same + [q for q in P if q not in same and q['id'] != p['id']])[:5]
    nxt = P[(i + 1) % len(P)]
    first, rest = p['imgs'][0], p['imgs'][1:]
    story = ''.join(f'<p>{e(t)}</p>' for t in p['body'])
    facts = ''.join(f'<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in p['facts'].items())
    gal = ''.join(f'<img src="{img(x)}" alt="{e(p["name"])}" loading="lazy">' for x in rest)
    kind = f'{p["sector"]} · {"Privat" if p["privat"] else "Objekt"}'
    where = ' · '.join(x for x in (p['facts'].get('Ort', ''), yr(p)) if x)
    return f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(p["name"])} · Bihler</title>
{fonts}
<style>{css}</style>
</head>
<body>
<header class="top in">
  <div class="top-l">
    <a class="pill" href="../index.html#projekte">Projekte</a>
    <a class="pill hide-s" href="../index.html#stuhlarchiv">Stuhlarchiv</a>
    <a class="pill hide-s" href="../index.html#haus">Haus</a>
  </div>
  <a class="logo" href="../index.html" aria-label="Bihler Möbelkonzepte">{logo}</a>
  <div class="top-r">
    <a class="pill hide-s" href="../index.html#usm">USM Shop</a>
    <a class="pill dark" href="../index.html#leistung">Beratung buchen</a>
  </div>
</header>
<main class="pp">
  <section class="pp-hero in">
    <a class="pill" href="../index.html#projekte">Alle Projekte</a>
    <span class="small">{e(kind)}</span>
    <h1 class="pp-h">{e(p["head"])}</h1>
    <p class="pp-name">{e(p["name"])}</p>
  </section>
  <section class="feature" aria-label="{e(p["name"])}">
    <img src="{img(first)}" alt="{e(p["name"])}">
    <div class="feature-top in"><span>{e(p["sector"])}</span><span>{e(where)}</span></div>
  </section>
  <section class="pp-body in">
    <div class="story">{story}</div>
    <dl class="facts">{facts}</dl>
  </section>
  <section class="pp-gal in">{gal}</section>
  <section class="sec in">
    <div class="sh"><h2>Weitere Projekte. <span class="g">{e(p["sector"])}</span></h2><a class="pill" href="../index.html#projekte">Alle Projekte</a></div>
    <div class="grid">{"".join(card(q) for q in more)}</div>
  </section>
  <div class="in"><a class="pp-next" href="{nxt["id"]}.html"><span class="small">Nächstes Projekt</span><span class="h">{e(nxt["head"])}</span><span class="pill dark">{e(nxt["name"])}</span></a></div>
</main>
{footer}
<a class="float" href="../index.html#leistung"><i></i><span><small>Beratung</small>Termin buchen</span></a>
</body>
</html>
'''

for i, p in enumerate(P):
    open(os.path.join('projekte', p['id'] + '.html'), 'w').write(page(p, i))
print('built index +', len(P), 'project pages')
