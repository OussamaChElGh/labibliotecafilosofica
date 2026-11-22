// Modo libro y marcapáginas para las lecturas completas de /leer/.
// El marcapáginas se guarda solo en este navegador (localStorage), sin cuenta.
(() => {
  const STORE = 'biblioteca.lectura.v1'
  const MODE = 'biblioteca.lectura.modo'
  const SAVED = 'biblioteca.saved-books.v1'
  const ROUTE = /^\/leer\/[\w-]+\/([\w-]+\/)?$/
  const root = document.documentElement

  const readAll = () => {
    try {
      const data = JSON.parse(localStorage.getItem(STORE) || '{}')
      return data && typeof data === 'object' && !Array.isArray(data) ? data : {}
    } catch { return {} }
  }
  const writeAll = data => { try { localStorage.setItem(STORE, JSON.stringify(data)) } catch {} }
  const getMode = () => { try { return localStorage.getItem(MODE) || 'libro' } catch { return 'libro' } }
  const setMode = value => { try { localStorage.setItem(MODE, value) } catch {} }
  const percent = value => Math.max(0, Math.min(100, Math.round(value * 100)))

  // "Seguir leyendo" en el índice de la obra.
  const continueBox = document.querySelector('[data-continue-book]')
  if (continueBox) {
    const mark = readAll()[continueBox.dataset.continueBook]
    if (mark && ROUTE.test(mark.route || '')) {
      const text = document.createElement('p')
      text.append('Seguir leyendo: ')
      const strong = document.createElement('strong')
      strong.textContent = String(mark.chapterTitle || '')
      text.append(strong, ` · ${percent(mark.progress)} % leído`)
      const bar = document.createElement('div'); bar.className = 'continue-bar'
      const fill = document.createElement('span'); fill.style.width = percent(mark.progress) + '%'; bar.append(fill)
      const link = document.createElement('a'); link.className = 'button'; link.href = mark.route; link.textContent = 'Continuar ↗'
      continueBox.append(text, bar, link); continueBox.hidden = false
    }
  }

  const book = document.querySelector('.book')
  if (!book) return
  const viewport = book.querySelector('.book-viewport')
  const flow = book.querySelector('.book-flow')
  const data = book.dataset
  const route = location.pathname

  // Controles.
  const sheen = document.createElement('div'); sheen.className = 'book-sheen'; viewport.append(sheen)
  const zonePrev = Object.assign(document.createElement('button'), { className: 'book-zone prev', type: 'button', textContent: '‹' })
  const zoneNext = Object.assign(document.createElement('button'), { className: 'book-zone next', type: 'button', textContent: '›' })
  zonePrev.setAttribute('aria-label', 'Página anterior'); zoneNext.setAttribute('aria-label', 'Página siguiente')
  viewport.append(zonePrev, zoneNext)
  const controls = document.createElement('div'); controls.className = 'book-controls'
  const btnPrev = Object.assign(document.createElement('button'), { type: 'button', textContent: '← Anterior' })
  const btnNext = Object.assign(document.createElement('button'), { type: 'button', textContent: 'Siguiente →' })
  const status = document.createElement('div'); status.className = 'book-status'; status.setAttribute('aria-live', 'polite')
  const statusText = document.createElement('div')
  const progress = document.createElement('div'); progress.className = 'book-progress'
  const progressFill = document.createElement('span'); progress.append(progressFill)
  status.append(statusText, progress)
  controls.append(btnPrev, status, btnNext)
  const note = document.createElement('p'); note.className = 'book-bookmark-note'
  const toggle = Object.assign(document.createElement('button'), { className: 'book-mode-toggle', type: 'button' })
  book.after(controls, note, toggle)

  let page = 0, pages = 1, perView = 2, step = 0, enabled = false

  // Índice de la obra: en modo libro, panel lateral con salto a una página del capítulo.
  const index = document.querySelector('.chapter-index')
  const panel = index && index.querySelector('.chapter-index-panel')
  const jump = document.createElement('form'); jump.className = 'chapter-jump'; jump.hidden = true
  const jumpLabel = document.createElement('label')
  const jumpInput = Object.assign(document.createElement('input'), { type: 'number', min: 1, inputMode: 'numeric' })
  const jumpTotal = document.createElement('span')
  jumpLabel.append('Ir a la página ', jumpInput); jump.append(jumpLabel, jumpTotal, Object.assign(document.createElement('button'), { type: 'submit', textContent: 'Ir' }))
  if (panel) panel.prepend(jump)
  jump.addEventListener('submit', event => {
    event.preventDefault()
    const target = Math.max(1, Math.min(pages, Number(jumpInput.value) || 1)) - 1
    const old = page; page = clampPage(target); render(true, page - old)
    index.open = false
    book.scrollIntoView({ block: 'center' })
  })
  if (index) {
    document.addEventListener('keydown', event => { if (event.key === 'Escape' && index.open) { index.open = false; index.querySelector('summary').focus() } })
    document.addEventListener('click', event => { if (enabled && index.open && !index.contains(event.target)) index.open = false })
  }

  const measure = () => {
    const style = getComputedStyle(viewport)
    const innerW = viewport.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight)
    perView = innerW >= 820 ? 2 : 1
    book.classList.toggle('is-spread', perView === 2)
    const gap = perView === 2 ? parseFloat(getComputedStyle(root).getPropertyValue('--book-gap')) || 96 : parseFloat(style.paddingLeft) * 2
    const colW = perView === 2 ? (innerW - gap) / 2 : innerW
    flow.style.columnWidth = colW + 'px'
    flow.style.columnGap = gap + 'px'
    flow.style.columnCount = 'auto'
    step = colW + gap
    flow.classList.add('is-instant'); flow.style.transform = 'none'
    pages = Math.max(1, Math.round((flow.scrollWidth + gap) / step))
  }

  const views = () => Math.ceil(pages / perView)
  const clampPage = p => Math.max(0, Math.min(p - (p % perView), (views() - 1) * perView))
  const ratio = () => views() > 1 ? (page / perView) / (views() - 1) : 1
  const bookProgress = () => Number(data.progressStart) + Number(data.progressSpan) * ratio()

  const save = () => {
    const all = readAll()
    all[data.book] = { route, bookRoute: data.bookRoute, bookTitle: data.bookTitle, chapterTitle: data.chapterTitle,
      chapter: Number(data.chapter), chapters: Number(data.chapters), position: ratio(), progress: bookProgress(), updated: Date.now() }
    writeAll(all)
    // Leer un libro lo añade a «Mi biblioteca»: la ficha y la lectura son la misma entrada.
    try {
      const saved = JSON.parse(localStorage.getItem(SAVED) || '[]')
      if (Array.isArray(saved) && /^\/[\w%\-/.]+\/$/.test(data.bookRoute || '') && !saved.includes(data.bookRoute)) {
        localStorage.setItem(SAVED, JSON.stringify([...saved, data.bookRoute]))
      }
    } catch {}
  }

  const render = (animate, direction) => {
    flow.classList.toggle('is-instant', !animate)
    flow.style.transform = `translateX(${-page * step}px)`
    if (animate && direction) {
      viewport.classList.remove('turn-next', 'turn-prev'); void viewport.offsetWidth
      viewport.classList.add(direction > 0 ? 'turn-next' : 'turn-prev')
    }
    const first = page + 1, last = Math.min(pages, page + perView)
    statusText.innerHTML = ''
    const strong = document.createElement('strong')
    strong.textContent = first === last ? `Página ${first}` : `Páginas ${first}–${last}`
    statusText.append(strong, ` de ${pages} · Capítulo ${data.chapter} de ${data.chapters} · ${percent(bookProgress())} % del libro`)
    progressFill.style.width = percent(bookProgress()) + '%'
    const atStart = page === 0, atEnd = page + perView >= pages
    btnPrev.disabled = atStart && !data.prev
    btnNext.disabled = atEnd && !data.next
    btnPrev.textContent = atStart && data.prev ? '← Capítulo anterior' : '← Anterior'
    btnNext.textContent = atEnd && data.next ? 'Capítulo siguiente →' : 'Siguiente →'
    zonePrev.disabled = btnPrev.disabled; zoneNext.disabled = btnNext.disabled
    note.textContent = 'Marcapáginas guardado automáticamente en este navegador.'
    jumpInput.max = pages; jumpInput.value = first; jumpTotal.textContent = `de ${pages}`
    save()
  }

  const go = delta => {
    if (!enabled) return
    const target = page + delta * perView
    if (target < 0) { if (data.prev) location.href = data.prev + '#final'; return }
    if (target >= pages) { if (data.next) { const all = readAll(); all[data.book] = { ...all[data.book], route: data.next, position: 0 }; writeAll(all); location.href = data.next } return }
    page = clampPage(target); render(true, delta)
  }

  const pageOf = element => {
    const flowLeft = flow.getBoundingClientRect().left
    return Math.floor((element.getBoundingClientRect().left - flowLeft + 1) / step)
  }

  const enable = startRatio => {
    root.classList.add('book-on'); enabled = true; jump.hidden = false
    toggle.textContent = 'Cambiar a lectura continua'
    measure()
    if (location.hash === '#final') page = clampPage(pages - 1)
    else page = clampPage(Math.round(startRatio * (views() - 1)) * perView)
    render(false)
    if (startRatio > 0 || location.hash === '#final') book.scrollIntoView({ block: 'center' })
  }
  const disable = () => {
    enabled = false; root.classList.remove('book-on'); jump.hidden = true
    flow.style.transform = ''; flow.style.columnWidth = ''; flow.style.columnGap = ''; flow.style.columnCount = ''
    toggle.textContent = 'Cambiar a modo libro'
    note.textContent = ''
  }

  toggle.addEventListener('click', () => {
    if (enabled) { setMode('continuo'); disable() } else { setMode('libro'); enable(0) }
  })
  btnPrev.addEventListener('click', () => go(-1)); btnNext.addEventListener('click', () => go(1))
  zonePrev.addEventListener('click', () => go(-1)); zoneNext.addEventListener('click', () => go(1))

  document.addEventListener('keydown', event => {
    if (!enabled || event.altKey || event.ctrlKey || event.metaKey || /input|textarea|select/i.test(event.target.tagName)) return
    if (['ArrowRight', 'PageDown'].includes(event.key) || (event.key === ' ' && !event.shiftKey)) { event.preventDefault(); go(1) }
    if (['ArrowLeft', 'PageUp'].includes(event.key) || (event.key === ' ' && event.shiftKey)) { event.preventDefault(); go(-1) }
  })

  let startX = null, startY = null
  viewport.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') { startX = e.clientX; startY = e.clientY } })
  viewport.addEventListener('pointerup', e => {
    if (startX === null) return
    const dx = e.clientX - startX, dy = e.clientY - startY; startX = null
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.3) go(dx < 0 ? 1 : -1)
  })

  // Enlaces a notas dentro del libro: saltar a la página de la nota.
  flow.addEventListener('click', event => {
    const link = event.target.closest('a[href^="#"]')
    if (!link || !enabled) return
    const target = document.getElementById(decodeURIComponent(link.hash.slice(1)))
    if (!target || !flow.contains(target)) return
    event.preventDefault()
    const old = page; page = clampPage(pageOf(target)); render(true, page - old)
  })

  // Repaginar cuando cambia el tamaño, la letra o la tipografía, sin perder el punto.
  let timer
  const repaginate = () => {
    if (!enabled) return
    clearTimeout(timer)
    timer = setTimeout(() => { const keep = ratio(); measure(); page = clampPage(Math.round(keep * (views() - 1)) * perView); render(false) }, 120)
  }
  window.addEventListener('resize', repaginate)
  new MutationObserver(repaginate).observe(document.body, { attributes: true, attributeFilter: ['style', 'data-paper'] })

  const saved = readAll()[data.book]
  const startRatio = saved && saved.route === route ? Number(saved.position) || 0 : 0
  if (getMode() === 'continuo') { disable(); save() } else {
    (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve()).then(() => enable(startRatio))
  }
})()
