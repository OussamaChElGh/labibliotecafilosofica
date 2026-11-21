// Genera las imágenes de portada de cada lectura completa a partir del SVG
// que escribe lectura_completa.py:
//   public/leer/<slug>/portada.png  (1000×1500, para descargar o compartir)
//   public/leer/<slug>/social.png   (1200×630, vista previa de enlaces y redes)
// Uso: node portadas.mjs   (después de python lectura_completa.py)
import { readFileSync, readdirSync, existsSync } from 'node:fs'
import { join, resolve } from 'node:path'
import { createRequire } from 'node:module'

const { chromium } = createRequire(import.meta.url)('playwright')
const ROOT = resolve('.')
// Las fuentes van incrustadas: una página creada con setContent no puede leer file://.
const font = (name, type) => `data:font/${type};base64,${readFileSync(join(ROOT, 'public/fonts', name)).toString('base64')}`
const COLORS = { verde: '#143a2c', burdeos: '#4a1820', azul: '#16233b', ocre: '#4f3615', negro: '#161015' }
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]))

const fontCss = `
@font-face{font-family:'Caslon Display';src:url('${font('libre-caslon-display.ttf', 'ttf')}')}
@font-face{font-family:Inter;src:url('${font('inter.woff2', 'woff2')}');font-weight:100 900}
@font-face{font-family:Fraunces;src:url('${font('fraunces.woff2', 'woff2')}');font-weight:100 900}
*{margin:0;box-sizing:border-box}`

const coverPage = svg => `<!doctype html><meta charset="utf-8"><style>${fontCss}
body{font-family:'Caslon Display',Fraunces,Inter}
html,body{width:600px;height:900px;overflow:hidden}svg{display:block;width:600px;height:900px}</style>${svg}`

const socialPage = (svg, meta) => {
  const bg = COLORS[meta.cover?.color] || meta.cover?.color || COLORS.verde
  const size = meta.title.length > 22 ? 64 : meta.title.length > 14 ? 78 : 96
  return `<!doctype html><meta charset="utf-8"><style>${fontCss}
html,body{width:1200px;height:630px;overflow:hidden}
body{background:${bg};color:#f7f4ee;font-family:Inter,sans-serif;display:flex;align-items:center;gap:64px;padding:0 80px 0 96px;position:relative}
body::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 28% 45%,#ffffff1c,transparent 55%),linear-gradient(90deg,transparent 40%,#0000004d)}
body::after{content:"";position:absolute;inset:22px;border:1.5px solid #c8a96a88;pointer-events:none}
.cover{position:relative;flex:none;width:340px;height:510px;border-radius:3px 8px 8px 3px;overflow:hidden;box-shadow:-5px 0 0 #0004 inset,0 30px 60px -20px #000,0 4px 10px #0008}
.cover svg{display:block;width:100%;height:100%}
.text{position:relative;display:flex;flex-direction:column;gap:20px}
.brand{font-size:15px;letter-spacing:5px;opacity:.8}
.author{color:#c8a96a;font-size:22px;letter-spacing:7px;margin-top:10px}
h1{font-family:'Caslon Display',Fraunces,serif;font-weight:400;font-size:${size}px;line-height:1.02}
.tr{font-family:Fraunces,serif;font-style:italic;font-size:24px;opacity:.85}
.cta{display:flex;align-items:center;gap:18px;margin-top:14px;font-size:18px}
.cta b{background:#c8a96a;color:#1a1410;border-radius:999px;padding:12px 24px;font-weight:600}
.cta span{opacity:.75}</style>
<div class="cover">${svg}</div>
<div class="text"><div class="brand">LA BIBLIOTECA FILOSÓFICA</div>
<div class="author">${esc(meta.author.toUpperCase())}</div><h1>${esc(meta.title)}</h1>
<div class="tr">Traducción de ${esc(meta.translator)}</div>
<div class="cta"><b>Léelo gratis online</b><span>${meta.chapters.length} capítulos · con marcapáginas</span></div></div>`
}

const browser = await chromium.launch()
const page = await browser.newPage()
let count = 0
for (const file of readdirSync('textos').filter(f => f.endsWith('.json')).sort()) {
  const meta = JSON.parse(readFileSync(join('textos', file), 'utf8'))
  const dir = join('public/leer', meta.slug)
  const index = join(dir, 'index.html')
  if (!existsSync(index)) { console.warn(`Falta ${index}: ejecuta antes python lectura_completa.py`); continue }
  const svg = readFileSync(index, 'utf8').match(/<svg class="book-cover-art"[\s\S]*?<\/svg>/)?.[0]
  if (!svg) { console.warn(`Sin portada en ${index}`); continue }
  const shots = [
    [coverPage(svg), 600, 900, 5 / 3, 'portada.png'],
    [socialPage(svg, meta), 1200, 630, 1, 'social.png'],
    [coverPage(svg), 600, 900, 2 / 3, 'portada-ficha.jpg'],  // 400×600, para fichas y tarjetas
  ]
  for (const [html, width, height, scale, name] of shots) {
    await page.setViewportSize({ width, height })
    await page.emulateMedia({ reducedMotion: 'reduce' })
    await page.setContent(html, { waitUntil: 'load' })
    await page.evaluate(() => document.fonts.ready)
    // deviceScaleFactor solo se fija al crear la página, así que se escala con CSS zoom.
    if (scale !== 1) {
      await page.setViewportSize({ width: Math.round(width * scale), height: Math.round(height * scale) })
      await page.addStyleTag({ content: `html{zoom:${scale}}` })
      await page.evaluate(() => document.fonts.ready)
    }
    const jpeg = name.endsWith('.jpg')
    await page.screenshot({ path: join(dir, name), type: jpeg ? 'jpeg' : 'png', ...(jpeg ? { quality: 86 } : {}) })
  }
  count++
}
await browser.close()
console.log(`${count} portadas generadas`)
