from pathlib import Path
from lxml import html
from html import escape
import json, shutil

base = Path('outputs/biblioteca-vercel/public')
out = base / 'diseno-v0'
out.mkdir(exist_ok=True)
assets = out / 'assets'
assets.mkdir(exist_ok=True)
shutil.copyfile(base/'wp-content/uploads/2023/07/logo-comprs.png', assets/'logo-original.png')
prefix = '/diseno-v0/'
home = html.parse(str(base/'index.html'))
catalog = html.parse(str(base/'libros-pdf-gratis/index.html'))
book = html.parse(str(base/'la-republica-platon/index.html'))
def render(el): return html.tostring(el, encoding='unicode')
def search():
    return '<form class="search" action="/biblioteca/" role="search"><input type="hidden" name="scope" value="pdf"><label class="sr" for="query">Título, autor o tema</label><input id="query" name="q" type="search" placeholder="¿Qué te gustaría leer?"><button type="submit">Buscar <span aria-hidden="true">↗</span></button></form>'
def link(path):
    return prefix+'libros/' if path=='/libros-pdf-gratis/' else prefix+'la-republica/' if path=='/la-republica-platon/' else path
def books(nodes):
    items=[]
    for li in nodes:
        a=li.xpath('.//a')[0]; imgs=li.xpath('.//img'); titles=li.xpath('.//h2')
        if not imgs or not titles: continue
        title=' '.join(titles[0].itertext()).replace('[PDF]','').strip(' -')
        items.append(f'<article class="book"><a href="{link(a.get("href"))}"><div class="cover"><img src="{escape(imgs[0].get("src"))}" alt="" loading="lazy"></div><h3>{escape(title)}</h3><span class="book-link">Ver la obra <span aria-hidden="true">↗</span></span></a></article>')
    return '<div class="books">'+''.join(items)+'</div>'
picks=home.xpath('//section[contains(@class,"journal")]//ul/li')
booklist=books(picks)
cover=book.xpath('//figure[contains(@class,"featured")]//img/@src')[0]
def shell(title,content,active):
    tabs=''.join(f'<a {"aria-current=page" if key==active else ""} href="{prefix}{path}">{name}</a>' for key,path,name in [('home','','Portada'),('catalog','libros/','Catálogo'),('book','la-republica/','Ficha de libro')])
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{title} · Muestra de diseño</title><link rel="stylesheet" href="{prefix}editorial.css"><script defer src="{prefix}editorial.js"></script><script>window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};</script><script defer src="/_vercel/insights/script.js"></script></head><body>
<a class="skip" href="#contenido">Saltar al contenido</a><div class="review"><span>Muestra de diseño · v0</span><nav aria-label="Vistas de la muestra">{tabs}</nav></div>
<header class="header wrap"><a class="identity" href="{prefix}"><img src="{prefix}assets/logo-original.png" alt=""><span>La Biblioteca<br>Filosófica</span></a><nav aria-label="Principal"><a href="{prefix}libros/">Libros</a><a href="/historia/">Historia</a><a href="/libros-pdf-gratis/autores/">Autores</a><a href="/articulos/">Artículos</a></nav><a class="header-action" href="{prefix}libros/#query">Explorar biblioteca ↗</a></header>
<main id="contenido">{content}</main><footer><div class="wrap footer"><div><span class="footer-name">La Biblioteca Filosófica</span><p>Libros, ideas y otras formas de mirar.</p></div><a href="{prefix}libros/">Explorar libros ↗</a></div></footer>
<details class="tweaks"><summary>Tweaks</summary><div><strong>Composición de la muestra</strong><label for="layout">Dirección visual</label><select id="layout"><option value="editorial">Editorial · recomendada</option><option value="quiet">Lectura tranquila</option><option value="expressive">Más expresiva</option></select><label for="density">Espaciado</label><select id="density"><option value="comfortable">Cómodo</option><option value="compact">Compacto</option></select><p>Estos controles solo pertenecen a la muestra.</p></div></details></body></html>'''

homepage=f'''<section class="opening"><div class="wrap opening-grid"><div class="opening-copy"><span class="kicker">Un lugar para leer y pensar</span><h1>Las grandes ideas<br>empiezan con<br><em>una página.</em></h1><p>Explora obras, descubre pensadores y encuentra tu próxima pregunta.</p>{search()}<div class="topics"><span>Empieza por</span><a href="/libros-pdf-gratis/autores/platon/">Platón</a><a href="/libros-pdf-gratis/autores/albert-camus/">Camus</a><a href="/estoicismo/">Estoicismo</a></div></div><a class="featured-book" href="{prefix}la-republica/"><span class="edition-label">Una conversación que sigue abierta</span><img src="{cover}" alt="Portada de La República, de Platón"><div><span>Platón</span><h2>La República</h2><p>La justicia. La educación. La ciudad ideal.</p><span class="round-arrow" aria-hidden="true">↗</span></div></a></div></section>
<nav class="library-paths wrap" aria-label="Explorar por interés"><a href="{prefix}libros/"><span>Leer</span><strong>La biblioteca</strong><b>↗</b></a><a href="/historia/"><span>Comprender</span><strong>Historia de las ideas</strong><b>↗</b></a><a href="/libros-pdf-gratis/autores/"><span>Conocer</span><strong>Sus protagonistas</strong><b>↗</b></a></nav>
<section class="wrap section"><div class="section-title"><h2>Un buen lugar<br>para empezar.</h2><div><p>Clásicos de la colección para abrir<br>nuevas conversaciones.</p><a class="text-link" href="{prefix}libros/">Explorar todos los libros ↗</a></div></div>{booklist}</section>
<section class="history"><div class="wrap history-grid"><div><span class="kicker">Historia de la filosofía</span><h2>Cada idea tiene<br>una historia.</h2><p>Recorre las épocas y descubre cómo una pregunta conduce a la siguiente.</p><a class="pill" href="/historia/">Recorrer la historia ↗</a></div><ol><li><a href="/historia-filosofia-en-la-antiguedad/"><small>Los orígenes</small><span>Antigüedad</span><b>↗</b></a></li><li><a href="/la-filosofia-medieval/"><small>Fe y razón</small><span>Edad Media</span><b>↗</b></a></li><li><a href="/historia-filosofia-renacimiento-y-filosofia-moderna/"><small>Una nueva mirada</small><span>Modernidad</span><b>↗</b></a></li></ol></div></section>'''

sections=catalog.xpath('//ul[@class="subsections"]/li/a')
side=''.join(f'<a href="{escape(a.get("href"))}"><span>{escape(a.text or "")}</span><span aria-hidden="true">↗</span></a>' for a in sections)
catalogpage=f'''<section class="catalog-intro wrap"><p class="breadcrumb"><a href="{prefix}">Inicio</a> / Biblioteca</p><div class="catalog-heading"><h1>Libros PDF.<br><em>Ideas sin prisa.</em></h1><div><p>Encuentra una obra por autor, género o tema. La próxima lectura empieza aquí.</p>{search()}</div></div></section><div class="catalog-layout wrap"><aside class="categories"><h2>Explora la colección</h2>{side}</aside><section class="catalog-results"><div class="section-title"><div><span class="kicker">Selección de la biblioteca</span><h2>Obras para descubrir</h2></div></div>{booklist}<div class="more-note"><p>Esta muestra presenta seis obras para valorar el diseño del catálogo.</p><a class="text-link" href="/libros-pdf-gratis/">Abrir el catálogo completo ↗</a></div></section></div>'''

download=book.xpath('//div[@class="book-detail"]//a[@class="button"]/@href')[0]
paragraph=book.xpath('//div[@class="entry"]/p[normalize-space()]')[0]
bookpage=f'''<section class="wrap detail"><p class="breadcrumb"><a href="{prefix}">Inicio</a> / <a href="{prefix}libros/">Libros</a> / Platón</p><div class="detail-grid"><div class="detail-art"><img src="{cover}" alt="Portada de La República, de Platón"></div><div class="detail-copy"><a class="author" href="/libros-pdf-gratis/autores/platon/">Platón ↗</a><h1>La República</h1><p class="book-deck">La justicia, la educación y la ciudad ideal: entra en uno de los grandes diálogos de la filosofía.</p><dl><div><dt>Autor</dt><dd>Platón</dd></div><div><dt>Recurso enlazado</dt><dd>PDF</dd></div></dl><a class="pill" href="{escape(download)}">Abrir el PDF <span aria-hidden="true">↗</span></a><p class="destination">Enlace externo · Universidad de Murcia</p><a class="text-link" href="#sinopsis">Leer la sinopsis ↓</a></div></div><div class="reading-layout" id="sinopsis"><aside><span class="kicker">En esta obra</span><a href="#sinopsis">Sinopsis</a><a href="/la-republica-platon/#seccion-12">El mito de la caverna ↗</a><a href="/la-republica-platon/#seccion-18">Justicia y política ↗</a><a href="/la-republica-platon/">Artículo completo ↗</a></aside><section><h2>Una pregunta que<br>atraviesa los siglos.</h2>{render(paragraph)}<a class="text-link" href="/la-republica-platon/">Seguir leyendo el análisis ↗</a></section></div></section><section class="wrap section related"><div class="section-title"><h2>Sigue la conversación.</h2><a class="text-link" href="/libros-pdf-gratis/autores/platon/">Más obras de Platón ↗</a></div>{books(picks[1:3])}</section>'''
for route,title,content,active in [('', 'Portada',homepage,'home'),('libros','Libros PDF',catalogpage,'catalog'),('la-republica','La República',bookpage,'book')]:
    target=out/route; target.mkdir(exist_ok=True)
    (target/'index.html').write_text(shell(title,content,active),encoding='utf-8')
print('Muestra v0: tres páginas conectadas; contenido y recursos locales reutilizados.')
