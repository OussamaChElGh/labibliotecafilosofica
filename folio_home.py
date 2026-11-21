"""Home-only editorial scene. All discovery links render without JavaScript."""
import json
from pathlib import Path
from html import escape


def render_showcase():
    books = json.loads(Path(__file__).with_name('folio-books.json').read_text(encoding='utf-8'))
    philosophy = {0, 2, 4, 7, 9, 12, 14, 16, 18, 21, 23, 24, 27, 29, 31}
    cards = []
    for i in range(12):
        b = books[i]
        category = 'Filosofía' if i in philosophy else 'Literatura'
        cards.append(f'''<li class="edition-card" data-edition-category="{category}">
        <a class="edition-cover" href="{b['href']}" data-preview-book="{i}"><img src="{b['cover']}" alt="Portada de {escape(b['title'])}" width="384" height="576" loading="lazy"><span>Ver de cerca ↗</span></a>
        <div class="edition-meta"><span>{category}</span><span>{i+1:02d}</span></div>
        <h3><a href="{b['href']}">{escape(b['title'])}</a></h3><p>{escape(b['author'])}</p>
        <div class="edition-actions"><button type="button" data-preview-book="{i}" hidden>Vista rápida</button><a href="{b['href']}">Abrir ficha ↗</a></div></li>''')
    return f'''<section class="edition-section" id="seleccion"><div class="edition-heading"><div><p class="eyebrow">Una selección para explorar</p><h2>Libros que abren caminos.</h2></div>
    <div class="edition-filters" role="group" aria-label="Filtrar selección de libros" hidden><button type="button" aria-pressed="true" data-edition-filter="Todas">Todos</button><button type="button" aria-pressed="false" data-edition-filter="Filosofía">Filosofía</button><button type="button" aria-pressed="false" data-edition-filter="Literatura">Literatura</button></div></div>
    <p class="edition-count" role="status">12 libros en esta selección</p><ul class="edition-grid">{''.join(cards)}</ul><a class="edition-all" href="/biblioteca/">Explorar el catálogo completo <span>↗</span></a></section>
    <section class="reading-room" id="sala-de-lectura"><header><p class="eyebrow">Un momento para las ideas</p><h2>La sala de lectura.</h2><p>Tres puertas de entrada. Lee una introducción y sigue hacia el artículo completo.</p></header>
    <div class="room-layout"><div class="room-atmosphere"><img src="/folio-assets/reading-room.jpg" alt="Una lectora junto a una lámpara en una biblioteca" width="1376" height="768" loading="lazy"><p class="eyebrow">Elige por dónde empezar</p>
    <nav aria-label="Introducciones disponibles"><a href="/que-es-filosofia/" data-room-select="0">01 <span>La primera pregunta</span> ↗</a><a href="/la-republica-platon/" data-room-select="1">02 <span>Imaginar una ciudad justa</span> ↗</a><a href="/descartes-discurso-del-metodo-pdf/" data-room-select="2">03 <span>Aprender a dudar</span> ↗</a></nav></div>
    <div class="room-reader"><div class="room-toolbar"><span>Introducción editorial</span><div hidden data-room-controls><button type="button" data-reader-size="-1" aria-label="Reducir tamaño del texto">A−</button><button type="button" data-reader-size="1" aria-label="Aumentar tamaño del texto">A+</button><button type="button" data-reader-tone aria-pressed="false">Papel oscuro</button></div></div>
    <article class="room-paper" aria-live="polite"><p class="eyebrow" data-room-author>Una primera orientación</p><h3 data-room-title>¿Qué es la filosofía?</h3><p data-room-text>La filosofía es la práctica de examinar las preguntas fundamentales sobre la realidad, el conocimiento, la acción y la vida buena mediante razones, conceptos y argumentos.</p><span class="room-rule" aria-hidden="true"></span><p class="room-note">Una introducción de La Biblioteca Filosófica. No es un fragmento del libro.</p></article><a class="room-continue" data-room-link href="/que-es-filosofia/">Continuar la lectura <span>↗</span></a></div></div></section>
    <dialog class="book-preview" aria-labelledby="preview-title"><button class="preview-close" type="button" aria-label="Cerrar vista rápida">×</button><div class="preview-layout"><img data-preview-cover alt="" width="384" height="576"><div><p class="eyebrow">En nuestra biblioteca</p><h2 id="preview-title"></h2><p data-preview-author></p><p class="preview-context">Consulta la ficha para conocer la obra, sus ideas y las fuentes de lectura disponibles.</p><div class="preview-actions"><a data-preview-link class="button" href="/biblioteca/">Abrir ficha ↗</a><button type="button" data-preview-save aria-pressed="false">Guardar libro</button></div><p class="preview-device">Guardado en este navegador, sin cuenta.</p><p data-preview-status role="status"></p><a class="preview-library" href="/mi-biblioteca/">Ir a Mi biblioteca ↗</a></div></div></dialog>'''


def render_home():
    books = json.loads(Path(__file__).with_name('folio-books.json').read_text(encoding='utf-8'))
    covers = ''.join(
        f'<li><a href="{b["href"]}" data-book="{i}"><img src="{b["cover"]}" '
        f'alt="" width="384" height="576" {"fetchpriority=high" if i == 0 else "loading=lazy"}>'
        f'<span>{escape(b["title"])}</span><small>{escape(b["author"])}</small></a></li>'
        for i, b in enumerate(books))
    return f'''<section class="folio-hero" aria-labelledby="folio-title">
    <div class="folio-heading"><p class="folio-kicker">UN LUGAR PARA LEER Y PENSAR</p>
    <h1 id="folio-title"><span>La Biblioteca</span><em>Filosófica</em></h1>
    <div class="folio-intro"><p>Libros, autores e ideas para leer y pensar.<small>Explora filosofía, literatura y rutas de lectura con contexto.</small></p>
    <a class="folio-cta" href="/biblioteca/">Explorar la biblioteca <span aria-hidden="true">↗</span></a></div></div>
    <div class="folio-stage" aria-hidden="true"></div>
    <div class="folio-shelf"><ul aria-label="Selección de libros">{covers}</ul></div>
    <div class="folio-bottom"><a class="folio-route" href="/rutas/introduccion-a-la-filosofia/">Una ruta para empezar <span aria-hidden="true">↗</span></a>
    <div class="folio-selection" hidden><span>En el estante</span><a href="{books[0]['href']}">{books[0]['title']} <small>— {books[0]['author']}</small> ↗</a></div>
    <button class="folio-pause" type="button" hidden aria-pressed="false">Pausar animación</button>
    <a class="folio-scroll" href="#descubrir">Sigue explorando <span aria-hidden="true">↓</span></a></div>
    </section>
    <section class="folio-discover" id="descubrir"><div><p class="eyebrow">Tu próxima página</p><h2>¿Qué te gustaría leer?</h2></div>
    <form action="/biblioteca/" role="search"><label class="sr" for="folio-query">Título, autor o tema</label><input id="folio-query" name="q" type="search" placeholder="Un título, un autor, una pregunta…"><button type="submit" aria-label="Buscar en la biblioteca">↗</button></form>
    <nav aria-label="Explorar la biblioteca"><a href="/libros-pdf-gratis/">Libros</a><a href="/libros-pdf-gratis/autores/">Autores</a><a href="/historia/">Historia de las ideas</a><a href="/colecciones/">Colecciones</a><a href="/que-es-filosofia/">Qué es la filosofía</a></nav></section>'''
