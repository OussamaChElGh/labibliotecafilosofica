// Imágenes para compartir de cada frase (1080×1080) a partir de build/frases.json,
// que escribe lectura_completa.py. Uso: node frases.mjs
import { readFileSync, mkdirSync, existsSync, readdirSync, unlinkSync } from 'node:fs'
import { join } from 'node:path'
import { createRequire } from 'node:module'

const { chromium } = createRequire(import.meta.url)('playwright')
const manifest = 'build/frases.json'
if (!existsSync(manifest)) { console.warn('Falta build/frases.json: ejecuta antes python lectura_completa.py'); process.exit(0) }
const cards = JSON.parse(readFileSync(manifest, 'utf8'))
const font = (name, type) => `data:font/${type};base64,${readFileSync(join('public/fonts', name)).toString('base64')}`
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]))
const css = `
@font-face{font-family:'Caslon Display';src:url('${font('libre-caslon-display.ttf', 'ttf')}')}
@font-face{font-family:Inter;src:url('${font('inter.woff2', 'woff2')}');font-weight:100 900}
@font-face{font-family:Fraunces;src:url('${font('fraunces.woff2', 'woff2')}');font-weight:100 900}
*{margin:0;box-sizing:border-box}
html,body{width:1080px;height:1080px;overflow:hidden}
body{color:#f7f4ee;font-family:Inter,sans-serif;display:flex;flex-direction:column;justify-content:center;padding:120px 112px;position:relative}
body::before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 30% 25%,#ffffff1f,transparent 60%),linear-gradient(180deg,transparent 50%,#00000059)}
body::after{content:"";position:absolute;inset:36px;border:2px solid #c8a96a99}
blockquote{position:relative;font-family:'Caslon Display',serif;line-height:1.16;letter-spacing:-.01em}
.q{color:#c8a96a}
.by{position:relative;margin-top:56px;color:#c8a96a;font-size:26px;letter-spacing:8px;text-transform:uppercase}
.work{position:relative;margin-top:12px;font-family:Fraunces,serif;font-style:italic;font-size:28px;opacity:.85}
.brand{position:absolute;left:112px;right:112px;bottom:76px;display:flex;justify-content:space-between;font-size:17px;letter-spacing:5px;opacity:.75}`
const size = n => n < 60 ? 76 : n < 110 ? 62 : n < 170 ? 52 : 44
mkdirSync('public/frases/img', { recursive: true })
const browser = await chromium.launch()
const page = await browser.newPage({ viewport: { width: 1080, height: 1080 } })
for (const card of cards) {
  await page.setContent(`<!doctype html><meta charset="utf-8"><style>${css}body{background:${card.color}}</style>
<blockquote style="font-size:${size(card.text.length)}px"><span class="q">«</span>${esc(card.text)}<span class="q">»</span></blockquote>
<div class="by">${esc(card.by)}</div><div class="work">${esc(card.work)}</div>
<div class="brand"><span>LA BIBLIOTECA FILOSÓFICA</span><span>labibliotecafilosofica.com</span></div>`, { waitUntil: 'load' })
  await page.evaluate(() => document.fonts.ready)
  await page.screenshot({ path: join('public/frases/img', `${card.id}.jpg`), type: 'jpeg', quality: 82 })
}
await browser.close()
// Quitar imágenes de frases que ya no existen.
const ids = new Set(cards.map(card => `${card.id}.jpg`))
for (const file of readdirSync('public/frases/img')) if (!ids.has(file)) unlinkSync(join('public/frases/img', file))
console.log(`${cards.length} imágenes de frases generadas`)
