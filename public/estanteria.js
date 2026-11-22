// «Mi biblioteca» como estantería: tres baldas (Leyendo, Quiero leer, Leídos) con los libros de lomo.
// Todo se guarda en este navegador (localStorage), sin cuenta:
//   biblioteca.saved-books.v1  rutas de las fichas guardadas (botón «Guardar libro» y lector online)
//   biblioteca.lectura.v1      marcapáginas del lector: capítulo y progreso de cada obra
//   biblioteca.estados.v1      estado elegido a mano para cada ficha: leyendo, quiero, leido
// Los textos guardados nunca se insertan como HTML.
(() => {
  const mount = document.querySelector('[data-bookcase]')
  if (!mount) return
  const SAVED = 'biblioteca.saved-books.v1'
  const MARKS = 'biblioteca.lectura.v1'
  const STATES = 'biblioteca.estados.v1'
  const ROUTE = /^\/[\w%\-/.]+\/$/
  const SHELVES = [
    ['leyendo', 'Leyendo', 'Los libros que tienes entre manos.'],
    ['quiero', 'Quiero leer', 'Tu próxima lectura está aquí.'],
    ['leido', 'Leídos', 'Los que ya terminaste.'],
  ]
  const PALETTE = ['#143a2c', '#4a1820', '#16233b', '#4f3615', '#161015', '#2f3a2a', '#5a2a1c', '#263247']
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches

  const load = (key, fallback) => {
    try { const value = JSON.parse(localStorage.getItem(key) || 'null'); return value ?? fallback } catch { return fallback }
  }
  const store = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); return true } catch { return false } }
  const savedList = () => { const v = load(SAVED, []); return Array.isArray(v) ? [...new Set(v.filter(r => typeof r === 'string' && ROUTE.test(r)))] : [] }
  const marks = () => { const v = load(MARKS, {}); return v && typeof v === 'object' && !Array.isArray(v) ? v : {} }
  const states = () => { const v = load(STATES, {}); return v && typeof v === 'object' && !Array.isArray(v) ? v : {} }
  const hash = text => [...text].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7)
  const percent = value => Math.max(0, Math.min(100, Math.round((Number(value) || 0) * 100)))
  const el = (tag, className, text) => { const node = document.createElement(tag); if (className) node.className = className; if (text != null) node.textContent = text; return node }
  const track = (name, params) => { try { window.gtag && window.gtag('event', name, params) } catch {} }

  let catalog = []
  const byRoute = new Map()

  // Une ficha guardada, marcapáginas y estado en una sola entrada por libro.
  const entries = () => {
    const saved = savedList(), all = marks(), chosen = states()
    const markByRoute = {}
    for (const [slug, mark] of Object.entries(all)) {
      if (mark && typeof mark === 'object' && ROUTE.test(mark.bookRoute || '')) markByRoute[mark.bookRoute] = { ...mark, slug }
    }
    const routes = [...new Set([...saved, ...Object.keys(markByRoute)])]
    return routes.map(route => {
      const book = byRoute.get(route)
      const mark = markByRoute[route]
      if (!book && !mark) return null
      const progress = mark ? Number(mark.progress) || 0 : 0
      let state = ['leyendo', 'quiero', 'leido'].includes(chosen[route]) ? chosen[route] : null
      if (!state) state = progress >= 0.98 ? 'leido' : (mark ? 'leyendo' : 'quiero')
      return {
        route, state, progress, mark,
        title: book?.title || mark?.bookTitle || 'Libro',
        author: book?.author || '',
        cover: book?.cover || '',
        read: book?.read || '',
        chapters: book?.chapters || 0,
        color: book?.color || PALETTE[hash(route) % PALETTE.length],
        updated: mark?.updated || 0,
      }
    }).filter(Boolean)
  }

  // Lomo de un libro: ancho según su extensión, alto variable para que la balda no parezca un código de barras.
  const spine = entry => {
    const h = hash(entry.route)
    const button = el('button', 'spine')
    button.type = 'button'
    button.dataset.route = entry.route
    button.draggable = true
    const width = entry.chapters ? Math.min(62, 34 + Math.round(Math.sqrt(entry.chapters) * 3)) : 36 + (h % 14)
    button.style.setProperty('--spine-w', width + 'px')
    button.style.setProperty('--spine-h', (196 + (h % 5) * 11) + 'px')
    button.style.setProperty('--spine-color', entry.color)
    button.style.setProperty('--spine-tilt', (entry.state === 'leido' && h % 4 === 0) ? '-3deg' : '0deg')
    button.setAttribute('aria-label', `${entry.title}${entry.author ? ', de ' + entry.author : ''}. ${labelOf(entry)}`)
    const band = el('span', 'spine-band'); band.setAttribute('aria-hidden', 'true')
    const title = el('span', 'spine-title', entry.title)
    const author = el('span', 'spine-author', entry.author.split(' ').slice(-1)[0] || '')
    button.append(band, title, author)
    if (entry.state === 'leyendo' && entry.progress > 0) {
      const ribbon = el('span', 'spine-ribbon'); ribbon.style.setProperty('--ribbon', Math.max(12, percent(entry.progress)) + '%')
      ribbon.setAttribute('aria-hidden', 'true'); button.append(ribbon)
    }
    if (entry.state === 'leido') { const star = el('span', 'spine-star', '✦'); star.setAttribute('aria-hidden', 'true'); button.append(star) }
    return button
  }
  const labelOf = entry => entry.state === 'leyendo' ? `Leyendo, ${percent(entry.progress)} % leído`
    : entry.state === 'leido' ? 'Leído' : 'Quiero leerlo'

  // Libro abierto: portada, progreso, estado y acciones.
  const dialog = el('dialog', 'book-open')
  dialog.setAttribute('aria-labelledby', 'book-open-title')
  document.body.append(dialog)
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close() })
  dialog.addEventListener('close', () => { const back = mount.querySelector(`.spine[data-route="${CSS.escape(dialog.dataset.route || '')}"]`); back?.focus() })

  const openBook = (route, origin) => {
    const entry = entries().find(e => e.route === route)
    if (!entry) return
    dialog.dataset.route = route
    dialog.replaceChildren()
    const close = el('button', 'book-open-close', '×'); close.type = 'button'; close.setAttribute('aria-label', 'Cerrar'); close.addEventListener('click', () => dialog.close())
    const cover = el('div', 'book-open-cover')
    cover.style.setProperty('--spine-color', entry.color)
    if (entry.cover) { const img = el('img'); img.src = entry.cover; img.alt = ''; img.decoding = 'async'; cover.append(img) }
    else cover.append(el('span', 'book-open-fallback', entry.title))
    const body = el('div', 'book-open-body')
    body.append(el('p', 'eyebrow', entry.author || 'La Biblioteca Filosófica'))
    const h = el('h2', null, entry.title); h.id = 'book-open-title'; body.append(h)
    if (entry.mark && entry.progress > 0) {
      body.append(el('p', 'book-open-where', `${entry.mark.chapterTitle || 'Capítulo ' + (entry.mark.chapter || 1)} · ${percent(entry.progress)} % leído`))
      const bar = el('div', 'book-open-bar'); const fill = el('span'); fill.style.width = percent(entry.progress) + '%'; bar.append(fill); body.append(bar)
    } else if (entry.chapters) {
      body.append(el('p', 'book-open-where', `${entry.chapters} capítulos para leer online`))
    }
    const actions = el('div', 'book-open-actions')
    const primary = el('a', 'button')
    if (entry.mark && ROUTE.test(entry.mark.route || '') && entry.state !== 'leido') { primary.href = entry.mark.route; primary.textContent = 'Continuar leyendo ↗' }
    else if (entry.read) { primary.href = entry.read; primary.textContent = entry.state === 'leido' ? 'Volver a leer ↗' : 'Empezar a leer ↗' }
    else { primary.href = entry.route; primary.textContent = 'Ver la ficha ↗' }
    actions.append(primary)
    if (primary.getAttribute('href') !== entry.route) { const ficha = el('a', 'text-link', 'Ficha y resumen'); ficha.href = entry.route; actions.append(ficha) }
    body.append(actions)
    const group = el('div', 'book-open-states'); group.setAttribute('role', 'group'); group.setAttribute('aria-label', 'Mover a la balda')
    for (const [state, label] of SHELVES) {
      const b = el('button', null, label); b.type = 'button'; b.setAttribute('aria-pressed', String(entry.state === state))
      b.addEventListener('click', () => { setState(route, state); dialog.close() })
      group.append(b)
    }
    body.append(el('p', 'book-open-label', 'Colocar en la balda'), group)
    const remove = el('button', 'book-open-remove', 'Quitar de mi biblioteca'); remove.type = 'button'
    remove.addEventListener('click', () => { removeBook(route); dialog.close() })
    body.append(remove)
    dialog.append(close, cover, body)
    if (typeof dialog.showModal === 'function') dialog.showModal(); else dialog.setAttribute('open', '')
    if (!reduced && origin && cover.animate) {
      const from = origin.getBoundingClientRect(), to = cover.getBoundingClientRect()
      if (to.width) cover.animate([
        { transform: `translate(${from.left - to.left}px, ${from.top - to.top}px) scale(${from.width / to.width}, ${from.height / to.height}) rotateY(70deg)`, opacity: .6 },
        { transform: 'none', opacity: 1 },
      ], { duration: 420, easing: 'cubic-bezier(.2,.8,.2,1)' })
    }
    track('library_open_book', { route })
  }

  const setState = (route, state) => {
    const all = states(); all[route] = state
    const saved = savedList(); if (!saved.includes(route)) saved.push(route)
    if (store(STATES, all) && store(SAVED, saved)) { track('library_move_book', { route, state }); render() } else error()
  }
  const removeBook = route => {
    const all = states(); delete all[route]
    const m = marks(); for (const [slug, mark] of Object.entries(m)) if (mark?.bookRoute === route) delete m[slug]
    if (store(STATES, all) && store(SAVED, savedList().filter(r => r !== route)) && store(MARKS, m)) { track('book_unsaved', { route }); render() } else error()
  }
  const error = () => { status.textContent = 'No se puede guardar en este navegador. Comprueba que el almacenamiento esté permitido.' }

  // Pintado de la estantería.
  const status = el('p', 'bookcase-status'); status.setAttribute('role', 'status')
  const resume = el('section', 'bookcase-resume'); resume.hidden = true
  const shelves = el('div', 'bookcase-shelves')
  const empty = el('div', 'library-empty')
  empty.hidden = true
  empty.append(el('h2', null, 'Una estantería por llenar.'), el('p', null, 'Abre una ficha y pulsa «Guardar libro», o empieza a leer uno online: aparecerá aquí.'))
  const explore = el('a', 'button', 'Explorar libros ↗'); explore.href = '/libros-pdf-gratis/'; empty.append(explore)
  const suggest = el('section', 'bookcase-suggest'); suggest.hidden = true
  mount.replaceChildren(status, resume, empty, shelves, suggest)

  const render = () => {
    const list = entries()
    const counts = { leyendo: 0, quiero: 0, leido: 0 }
    for (const e of list) counts[e.state]++
    status.textContent = list.length
      ? `${counts.leyendo} leyendo · ${counts.quiero} por leer · ${counts.leido} ${counts.leido === 1 ? 'leído' : 'leídos'}`
      : ''
    empty.hidden = list.length > 0

    // Continuar leyendo: el último libro abierto en el lector.
    const last = list.filter(e => e.state === 'leyendo' && e.mark && ROUTE.test(e.mark.route || '')).sort((a, b) => b.updated - a.updated)[0]
    resume.replaceChildren(); resume.hidden = !last
    if (last) {
      const cover = el('div', 'bookcase-resume-cover'); cover.style.setProperty('--spine-color', last.color)
      if (last.cover) { const img = el('img'); img.src = last.cover; img.alt = ''; img.decoding = 'async'; cover.append(img) }
      const text = el('div', 'bookcase-resume-text')
      text.append(el('p', 'eyebrow', 'Seguir leyendo'), el('h2', null, last.title),
        el('p', null, `${last.mark.chapterTitle || ''} · ${percent(last.progress)} % leído`))
      const bar = el('div', 'book-open-bar'); const fill = el('span'); fill.style.width = percent(last.progress) + '%'; bar.append(fill)
      const go = el('a', 'button', 'Continuar ↗'); go.href = last.mark.route
      text.append(bar, go)
      resume.append(cover, text)
    }

    shelves.replaceChildren()
    for (const [state, label, hint] of SHELVES) {
      const items = list.filter(e => e.state === state)
        .sort((a, b) => state === 'leyendo' ? b.updated - a.updated : a.title.localeCompare(b.title, 'es'))
      if (!list.length) continue
      const section = el('section', 'bookcase-shelf'); section.dataset.state = state
      const head = el('header'); head.append(el('h2', null, label), el('span', 'count', String(items.length)))
      const row = el('div', 'bookcase-row'); row.dataset.state = state
      row.setAttribute('aria-label', `${label}: ${items.length} ${items.length === 1 ? 'libro' : 'libros'}`)
      if (items.length) for (const item of items) row.append(spine(item))
      else row.append(el('p', 'bookcase-hint', hint + ' Arrastra un libro hasta aquí o ábrelo y elige esta balda.'))
      section.append(head, row)
      shelves.append(section)
    }

    // Sugerencias para llenar la estantería: lecturas online que aún no están en ella.
    suggest.replaceChildren()
    const mine = new Set(list.map(e => e.route))
    const pool = catalog.filter(b => b.read && !mine.has(b.route))
    suggest.hidden = !pool.length
    if (pool.length) {
      const day = Math.floor(Date.now() / 864e5)
      const picks = pool.map(b => [hash(b.route + day), b]).sort((a, b) => a[0] - b[0]).slice(0, 6).map(x => x[1])
      const head = el('header'); head.append(el('h2', null, list.length ? 'Para tu próxima balda' : 'Empieza por uno de estos'))
      const grid = el('ul', 'bookcase-suggest-grid')
      for (const b of picks) {
        const li = el('li'); const a = el('a'); a.href = b.route
        const figure = el('span', 'bookcase-suggest-cover'); figure.style.setProperty('--spine-color', b.color || PALETTE[hash(b.route) % PALETTE.length])
        if (b.cover) { const img = el('img'); img.src = b.cover; img.alt = ''; img.loading = 'lazy'; img.decoding = 'async'; figure.append(img) }
        a.append(figure, el('strong', null, b.title), el('span', null, b.author))
        const add = el('button', 'bookcase-add', '+ A la balda «Quiero leer»'); add.type = 'button'
        add.addEventListener('click', () => setState(b.route, 'quiero'))
        li.append(a, add); grid.append(li)
      }
      suggest.append(head, grid)
    }
  }

  // Abrir un libro y arrastrarlo de una balda a otra.
  mount.addEventListener('click', event => {
    const target = event.target.closest('.spine')
    if (target) openBook(target.dataset.route, target)
  })
  let dragging = null
  mount.addEventListener('dragstart', event => {
    const target = event.target.closest('.spine'); if (!target) return
    dragging = target.dataset.route; event.dataTransfer.effectAllowed = 'move'; event.dataTransfer.setData('text/plain', dragging)
    target.classList.add('is-dragging')
  })
  mount.addEventListener('dragend', event => { event.target.closest?.('.spine')?.classList.remove('is-dragging'); dragging = null; mount.querySelectorAll('.is-over').forEach(n => n.classList.remove('is-over')) })
  mount.addEventListener('dragover', event => {
    const row = event.target.closest('.bookcase-row'); if (!row || !dragging) return
    event.preventDefault(); mount.querySelectorAll('.is-over').forEach(n => n !== row && n.classList.remove('is-over')); row.classList.add('is-over')
  })
  mount.addEventListener('drop', event => {
    const row = event.target.closest('.bookcase-row'); if (!row || !dragging) return
    event.preventDefault(); setState(dragging, row.dataset.state)
  })
  addEventListener('storage', event => { if ([SAVED, MARKS, STATES, null].includes(event.key)) render() })

  status.textContent = 'Cargando tu estantería…'
  fetch('/catalogo-libros.json')
    .then(response => response.ok ? response.json() : [])
    .catch(() => [])
    .then(data => {
      catalog = Array.isArray(data) ? data : []
      for (const book of catalog) byRoute.set(book.route, book)
      render()
    })
})()
