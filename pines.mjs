// Pines verticales para Pinterest (1000×1500) y el CSV de subida en bloque.
//   public/pinterest/<nombre>.jpg   imágenes publicadas en la web (Pinterest las lee por URL)
//   build/pinterest.csv             para Pinterest → Crear → Crear pines en bloque
// Uso: node pines.mjs   (después de python lectura_completa.py, que escribe build/portadas/<slug>.svg)
//      PINES_INICIO=2026-11-24 node pines.mjs   primer día del calendario (por defecto, mañana)
// Usa Microsoft Edge, como portadas.mjs. Los tableros del CSV deben existir en Pinterest con ese nombre exacto.
import { readFileSync, readdirSync, existsSync, mkdirSync, writeFileSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { createRequire } from 'node:module'

const { chromium } = createRequire(import.meta.url)('playwright')
const BASE = 'https://labibliotecafilosofica.com'
const OUT = 'public/pinterest'
const BOARDS = {
  cuentos: 'Cuentos cortos en inglés',
  japones: 'Aprender japonés gratis',
  libros: 'Libros clásicos para leer online gratis',
}
const COLORS = { verde: '#143a2c', burdeos: '#4a1820', azul: '#16233b', ocre: '#4f3615', negro: '#161015' }
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]))
const dataUri = (path, type) => `data:${type};base64,${readFileSync(path).toString('base64')}`
const font = (name, type) => dataUri(join('public/fonts', name), `font/${type}`)
const LOGO = dataUri('public/img/logo-portada.png', 'image/png')
const inlineImages = svg => svg.replace(/href="(\/(?:leer|img)\/[^"]+\.(jpg|png))"/g, (_, url, ext) =>
  `href="${dataUri(join('public', url), ext === 'png' ? 'image/png' : 'image/jpeg')}"`)

const css = bg => `<style>
@font-face{font-family:'Caslon Display';src:url('${font('libre-caslon-display.ttf', 'ttf')}')}
@font-face{font-family:Inter;src:url('${font('inter.woff2', 'woff2')}');font-weight:100 900}
@font-face{font-family:Fraunces;src:url('${font('fraunces.woff2', 'woff2')}');font-weight:100 900}
*{box-sizing:border-box;margin:0}
body{width:1000px;height:1500px;background:${bg};color:#f7f4ee;font-family:Inter,sans-serif;position:relative;overflow:hidden}
body:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 50% 22%,#ffffff12,transparent 60%),radial-gradient(circle at 50% 100%,#0006,transparent 55%)}
.frame{position:absolute;inset:34px;border:2px solid #c8a96a;pointer-events:none}.frame:after{content:"";position:absolute;inset:10px;border:1px solid #c8a96a99}
.wrap{position:absolute;inset:80px 84px;display:flex;flex-direction:column;align-items:center;text-align:center}
.brand{display:flex;flex-direction:column;align-items:center;gap:10px;font-size:17px;letter-spacing:.32em;color:#e8dcc0}
.brand img{width:66px}
.eyebrow{font-size:27px;letter-spacing:.24em;text-transform:uppercase;color:#c8a96a;margin-top:44px}
h1{font-family:'Caslon Display',Georgia,serif;font-weight:400;line-height:1.02;letter-spacing:-.01em}
.author{font-family:Fraunces,serif;font-style:italic;font-size:44px;opacity:.9}
.badge{display:inline-block;border:3px solid #c8a96a;color:#c8a96a;border-radius:999px;padding:16px 40px;font-size:36px;font-weight:600;letter-spacing:.06em}
.text{font-family:Fraunces,serif;font-size:42px;line-height:1.38;opacity:.92}
.cta{margin-top:auto;background:#c8a96a;color:#1a1410;border-radius:999px;padding:30px 64px;font-size:40px;font-weight:700}
.url{margin-top:24px;font-size:27px;letter-spacing:.08em;opacity:.75}
.cover{width:590px;filter:drop-shadow(0 30px 40px #000a)}.cover svg{display:block;width:100%;height:auto;border-radius:3px 8px 8px 3px}
ul{list-style:none;padding:0;text-align:left;width:100%}li{font-size:40px;line-height:1.3;padding:22px 0;border-bottom:1px solid #c8a96a55}li b{color:#c8a96a;font-weight:700}
</style>`
const brand = `<div class="brand"><img src="${LOGO}" alt="">LA BIBLIOTECA FILOSÓFICA</div>`
const page = (bg, inner) => `<!doctype html><html lang="es"><head><meta charset="utf-8">${css(bg)}</head><body><div class="frame"></div><div class="wrap">${inner}</div></body></html>`
const fit = (text, max, min, perChar) => Math.max(min, Math.min(max, Math.round(perChar / Math.max(8, text.length))))

const pins = []
const books = readdirSync('textos').filter(f => f.endsWith('.json')).sort()
  .map(f => JSON.parse(readFileSync(join('textos', f), 'utf8'))).filter(m => m.slug && m.chapters)

// 1. Un pin por cuento en inglés: nivel, título, autor y resumen en español.
const cuentos = books.find(m => m.slug === 'cuentos-cortos-en-ingles')
if (cuentos) {
  for (const ch of cuentos.chapters) {
    const m = ch.summary.match(/^Nivel ([^·]+) · (.+?), (\d{4})\. (.+)$/)
    if (!m) continue
    const [, level, author, year, summary] = m
    const title = ch.title.replace(/ \([^)]*\)$/, '')
    pins.push({
      name: `cuento-${ch.slug}`, board: BOARDS.cuentos, link: `${BASE}/leer/${cuentos.slug}/${ch.slug}/`,
      title: `${title} (${author}): cuento corto en inglés para leer gratis · nivel ${level.trim()}`,
      description: `Lee «${title}» de ${author} (${year}) completo en inglés, gratis y online. Nivel orientativo ${level.trim()}, con resumen en español: ${summary} Cuentos cortos en inglés para aprender y practicar el idioma.`,
      html: page(COLORS.azul, `${brand}<div class="eyebrow">Cuentos cortos en inglés</div>
        <div class="badge" style="margin-top:70px">Nivel ${esc(level.trim())}</div>
        <h1 style="font-size:${fit(title, 150, 86, 2300)}px;margin-top:56px">${esc(title)}</h1>
        <div class="author" style="margin-top:26px">${esc(author)} · ${year}</div>
        <p class="text" style="margin-top:60px">${esc(summary)}</p>
        <div class="cta">Léelo gratis en inglés</div><div class="url">labibliotecafilosofica.com</div>`),
    })
  }
}

// 2. Japonés: recursos gratuitos y por dónde empezar.
const JAPON = `${BASE}/libros-pdf-gratis-aprender-japones/`
pins.push({
  name: 'japones-recursos-gratis', board: BOARDS.japones, link: JAPON,
  title: 'Libros y PDF gratis para aprender japonés (oficiales y legales)',
  description: 'Los mejores recursos gratis para aprender japonés: los libros Irodori en PDF de la Fundación Japón, el curso en español de NHK, la guía de gramática de Tae Kim y las preguntas oficiales del JLPT. Con su nivel y por dónde empezar.',
  html: page(COLORS.burdeos, `${brand}<div class="eyebrow">Aprender japonés</div>
    <h1 style="font-size:122px;margin-top:44px">Libros y PDF gratis</h1><div class="author" style="margin-top:20px">solo recursos oficiales y legales</div>
    <ul style="margin-top:56px"><li><b>Irodori</b> · 4 libros en PDF, A1-B1</li><li><b>NHK</b> · curso en español con PDF y MP3</li>
    <li><b>Tae Kim</b> · gramática completa</li><li><b>Minato</b> · cursos en línea</li><li><b>JLPT</b> · preguntas oficiales N5-N1</li></ul>
    <div class="cta">Ver los recursos</div><div class="url">labibliotecafilosofica.com</div>`),
})
pins.push({
  name: 'japones-por-donde-empezar', board: BOARDS.japones, link: `${JAPON}#por-donde-empezar`,
  title: 'Cómo empezar a aprender japonés gratis: 5 pasos',
  description: 'Un orden sencillo para aprender japonés desde cero sin pagar: hiragana y katakana, un curso base (Irodori o NHK en español), la gramática de Tae Kim, vídeos de Erin y las preguntas de ejemplo del JLPT N5.',
  html: page(COLORS.burdeos, `${brand}<div class="eyebrow">Japonés desde cero</div>
    <h1 style="font-size:118px;margin-top:44px">Por dónde empezar</h1><div class="author" style="margin-top:20px">5 pasos, todo gratis</div>
    <ul style="margin-top:56px"><li><b>1.</b> Hiragana y katakana</li><li><b>2.</b> Un curso base: Irodori o NHK</li>
    <li><b>3.</b> Gramática con Tae Kim</li><li><b>4.</b> Escucha con los vídeos de Erin</li><li><b>5.</b> Mide tu nivel: JLPT N5</li></ul>
    <div class="cta">Ver el plan completo</div><div class="url">labibliotecafilosofica.com</div>`),
})

// 3. Un pin por libro con lectura completa: su portada de la colección.
for (const meta of books) {
  if (meta.slug === 'cuentos-cortos-en-ingles') continue
  const svgPath = join('build/portadas', `${meta.slug}.svg`)
  if (!existsSync(svgPath)) continue
  const ficha = meta.ficha || {}
  const unit = ficha.unidad || 'capítulos'
  const route = meta.book_route || `/leer/${meta.slug}/`
  const genero = ficha.genero ? `${ficha.genero}` : 'Libro'
  pins.push({
    name: `libro-${meta.slug}`, board: BOARDS.libros, link: BASE + route,
    title: `${meta.title} de ${meta.author}: libro completo para leer online gratis`.slice(0, 100),
    description: `Lee «${meta.title}» de ${meta.author} completo, gratis y online, dividido en ${meta.chapters.length} ${unit}, con resumen y PDF para descargar.${ficha.tema ? ` ${genero} sobre ${ficha.tema}.` : ''} Texto de dominio público.`.slice(0, 500),
    html: page(COLORS[(meta.cover || {}).color] || COLORS.verde, `${brand}
      <div class="cover" style="margin-top:40px">${inlineImages(readFileSync(svgPath, 'utf8'))}</div>
      <div class="eyebrow" style="margin-top:44px">Libro completo · ${meta.chapters.length} ${esc(unit)} · PDF gratis</div>
      <div class="cta">Léelo gratis online</div><div class="url">labibliotecafilosofica.com</div>`),
  })
}

// Imágenes.
mkdirSync(OUT, { recursive: true })
const browser = await chromium.launch({ channel: process.env.NAVEGADOR || 'msedge' })
const tab = await browser.newPage({ viewport: { width: 1000, height: 1500 } })
for (const pin of pins) {
  await tab.setContent(pin.html, { waitUntil: 'load' })
  await tab.evaluate(() => document.fonts.ready)
  await tab.screenshot({ path: join(OUT, `${pin.name}.jpg`), type: 'jpeg', quality: 84 })
}
await browser.close()

// CSV para la subida en bloque: tres pines al día, alternando tableros, a las 10:00, 15:00 y 20:00.
const start = process.env.PINES_INICIO ? new Date(process.env.PINES_INICIO + 'T00:00:00Z') : new Date(Date.now() + 864e5)
const order = []
const queues = Object.values(BOARDS).map(b => pins.filter(p => p.board === b))
while (queues.some(q => q.length)) for (const q of queues) if (q.length) order.push(q.shift())
const hours = [9, 14, 19]  // UTC (10:00, 15:00 y 20:00 en España peninsular en invierno)
const cell = v => `"${String(v).replace(/"/g, '""')}"`
const rows = [['Title', 'Media URL', 'Pinterest board', 'Thumbnail', 'Description', 'Link', 'Publish date', 'Keywords']]
order.forEach((pin, i) => {
  const date = new Date(start.getTime() + Math.floor(i / 3) * 864e5)
  date.setUTCHours(hours[i % 3], 0, 0, 0)
  rows.push([pin.title.slice(0, 100), `${BASE}/pinterest/${pin.name}.jpg`, pin.board, '', pin.description.slice(0, 500), pin.link,
    date.toISOString().slice(0, 19), ''])
})
mkdirSync('build', { recursive: true })
writeFileSync('build/pinterest.csv', '﻿' + rows.map(r => r.map(cell).join(',')).join('\r\n') + '\r\n')
console.log(`${pins.length} pines · build/pinterest.csv · ${Math.ceil(order.length / 3)} días`)
