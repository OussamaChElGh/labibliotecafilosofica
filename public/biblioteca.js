const catalog = document.querySelector("[data-catalog]");
const readingRoute = document.querySelector('[data-reading-route]');
const track = (name, detail = {}) => {
  const event = { event: name, ...detail, ts: Date.now() };
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push(event);
  window.dispatchEvent(new CustomEvent('biblioteca:analytics', { detail: event }));
};
if (readingRoute) {
  const key = 'biblioteca.route.intro-filosofia.v1';
  const steps = [...readingRoute.querySelectorAll('[data-route-step]')];
  const progress = readingRoute.querySelector('[data-route-progress]');
  const complete = readingRoute.querySelector('[data-complete-route]');
  let done = [];
  try { done = JSON.parse(localStorage.getItem(key) || '[]'); } catch {}
  const render = () => {
    steps.forEach((step, index) => {
      const active = done.includes(index);
      step.classList.toggle('is-complete', active);
      step.setAttribute('aria-pressed', String(active));
    });
    if (progress) progress.textContent = `${done.length} de ${steps.length} etapas completadas`;
    if (complete) complete.textContent = done.length === steps.length ? 'Ruta completada ✓' : 'Marcar ruta como completada';
  };
  steps.forEach((step, index) => step.addEventListener('click', () => {
    done = done.includes(index) ? done.filter(value => value !== index) : [...done, index].sort((a,b) => a-b);
    try { localStorage.setItem(key, JSON.stringify(done)); } catch {}
    track('reading_route_step', { route: 'intro-filosofia', step: index, completed: done.includes(index) });
    render();
  }));
  complete?.addEventListener('click', () => {
    done = steps.map((_, index) => index);
    try { localStorage.setItem(key, JSON.stringify(done)); } catch {}
    track('reading_route_completed', { route: 'intro-filosofia', steps: steps.length });
    render();
  });
  render();
}
const dashboardRoute = document.querySelector('[data-dashboard-route]');
if (dashboardRoute) {
  let done = [];
  try { done = JSON.parse(localStorage.getItem('biblioteca.route.intro-filosofia.v1') || '[]'); } catch {}
  const copy = dashboardRoute.querySelector('[data-dashboard-progress]');
  if (copy) copy.textContent = done.length ? `${done.length} de 5 etapas completadas. ${done.length < 5 ? 'Tu siguiente paso está listo.' : 'Ruta completada; descubre otra colección.'}` : 'Todavía no has empezado. La primera etapa dura unos minutos.';
}

if (catalog) {
  const form = catalog.querySelector("form");
  const search = form.elements.q;
  const category = form.elements.tema;
  const status = catalog.querySelector("[data-status]");
  const parameters = new URLSearchParams(location.search);
  let pdfOnly = parameters.get("scope") === "pdf";
  search.value = parameters.get("q") || "";
  const more = catalog.querySelector("[data-more]");
  const normalize = (value) => value.normalize("NFD").replace(/\p{M}/gu, "").toLocaleLowerCase("es");
  const cards = [...catalog.querySelectorAll("[data-search]")].map((element) => ({
    element,
    text: normalize(element.dataset.search),
    categories: element.dataset.category.split(" "),
  }));
  const batch = 18;
  let limit = batch;

  function update() {
    const words = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let matches = 0;
    for (const { element, text, categories } of cards) {
      const match = (!pdfOnly || element.dataset.pdf === "true") && (!category.value || categories.includes(category.value)) && words.every((word) => text.includes(word));
      if (match) matches++;
      element.hidden = !match || matches > limit;
    }
    const shown = Math.min(matches, limit);
    status.textContent = matches ? `${shown} de ${matches} publicaciones` : "Sin resultados. Prueba otro término o tema.";
    more.hidden = matches <= limit;
  }

  const refresh = () => { limit = batch; update(); };
  form.hidden = false;
  form.addEventListener("submit", (event) => { event.preventDefault(); refresh(); });
  form.addEventListener("input", refresh);
  form.addEventListener("reset", () => { pdfOnly = false; requestAnimationFrame(refresh); });
  more.addEventListener("click", () => { limit += batch; update(); });
  update();
  if (location.hash === "#buscar") search.focus();
}

const menus = [...document.querySelectorAll(".nav-disclosure")];
for (const menu of menus) {
  menu.addEventListener("toggle", () => {
    if (menu.open) for (const other of menus) if (other !== menu) other.open = false;
  });
}
document.addEventListener("click", (event) => {
  if (!event.target.closest(".nav-disclosure")) for (const menu of menus) menu.open = false;
});
document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") return;
  const open = menus.find((menu) => menu.open);
  if (open) { open.open = false; open.querySelector("summary").focus(); }
});

// Compact mobile navigation with a no-JavaScript visible fallback.
const mobileMenu = document.querySelector('.mobile-menu-toggle');
const primaryNav = document.querySelector('#primary-navigation');
if (mobileMenu && primaryNav) {
  document.documentElement.classList.add('nav-ready');
  mobileMenu.hidden=false;
  const closeMenu=()=>{primaryNav.classList.remove('is-open');mobileMenu.setAttribute('aria-expanded','false');};
  mobileMenu.addEventListener('click',()=>{const open=primaryNav.classList.toggle('is-open');mobileMenu.setAttribute('aria-expanded',String(open));});
  primaryNav.addEventListener('keydown',event=>{if(event.key==='Escape'){closeMenu();mobileMenu.focus();}});
  primaryNav.addEventListener('click',event=>{if(event.target.closest('a'))closeMenu();});
  matchMedia('(min-width:761px)').addEventListener('change',closeMenu);
}

// Keep readable HTML without JavaScript; load motion only when requested by the device.
const animated = document.querySelector('.opening,.category-hero,.book-detail,.catalog,.folio-page-head,.folio-article-head');
if (animated && matchMedia('(prefers-reduced-motion: no-preference)').matches) {
  const library = document.createElement('script');
  library.src = '/gsap.min.js';
  library.addEventListener('load', () => {
    const gsap = window.gsap;
    const media = gsap.matchMedia();
    media.add('(prefers-reduced-motion: no-preference)', () => {
      const hero = document.querySelector('.opening-copy,.category-hero>div,.book-detail>div:last-child,.folio-page-head,.folio-article-head');
      if (hero) gsap.from([...hero.children], {y:24,duration:.65,stagger:.09,ease:'power3.out',clearProps:'transform'});
      const cover = document.querySelector('.featured-book>img,.book-detail .featured img');
      if (cover) gsap.from(cover,{y:32,rotation:0,duration:.85,delay:.12,ease:'power3.out',clearProps:'transform'});
      const observer = new IntersectionObserver(entries => {
        for (const entry of entries) {
          if (!entry.isIntersecting) continue;
          observer.unobserve(entry.target);
          const children=[...entry.target.children].filter(el=>!el.hidden);
          gsap.from(children,{y:20,duration:.55,stagger:.065,ease:'power2.out',clearProps:'transform'});
        }
      },{threshold:.08});
      document.querySelectorAll('.book-grid,.feature-grid,.product-grid,.library-paths,.history-grid>ol,.subsections,.timeline,.collection-grid,.route-steps').forEach(el=>observer.observe(el));
      const handlers=[];
      document.querySelectorAll('.nav-disclosure').forEach(menu=>{
        const handler=()=>{if(menu.open) gsap.fromTo(menu.querySelector('.nav-panel'),{y:-8,opacity:0},{y:0,opacity:1,duration:.2,ease:'power2.out',clearProps:'all'})};
        menu.addEventListener('toggle',handler); handlers.push([menu,handler]);
      });
      return ()=>{observer.disconnect();handlers.forEach(([el,fn])=>el.removeEventListener('toggle',fn));};
    });
  }, {once:true});
  document.head.append(library);
}

if (document.querySelector('.entry')) {
  const progress = document.createElement('div');
  progress.className = 'reading-progress';
  progress.setAttribute('aria-hidden','true');
  document.body.append(progress);
  let queued = false;
  const updateProgress = () => {
    const range = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${range > 0 ? Math.min(1,scrollY/range) : 0})`;
    queued = false;
  };
  addEventListener('scroll', () => { if (!queued) {queued=true; requestAnimationFrame(updateProgress);} }, {passive:true});
  updateProgress();
}


// Store only known book paths. Never render persisted strings as HTML.
(() => {
  const key='biblioteca.saved-books.v1';
  const saveButton=document.querySelector('[data-save-route]');
  const library=document.querySelector('[data-personal-library]');
  if (!saveButton && !library) return;
  const read=()=>{
    const parsed=JSON.parse(localStorage.getItem(key)||'[]');
    if (!Array.isArray(parsed)) throw new Error('invalid saved list');
    return [...new Set(parsed.filter(value=>typeof value==='string' && /^\/[\w%\-/.]+\/$/.test(value)))];
  };
  const write=values=>localStorage.setItem(key,JSON.stringify(values));
  // Progreso de lectura online (lo guarda lector-libro.js), indexado por la ruta de la ficha.
  const marksKey='biblioteca.lectura.v1';
  const readMarks=()=>{
    try{
      const data=JSON.parse(localStorage.getItem(marksKey)||'{}');const byRoute={};
      for(const [slug,mark] of Object.entries(data&&typeof data==='object'?data:{})){
        if(mark&&typeof mark.bookRoute==='string'&&/^\/leer\/[\w-]+\/([\w-]+\/)?$/.test(mark.route||''))byRoute[mark.bookRoute]={...mark,slug};
      }
      return byRoute;
    }catch{return {};}
  };
  const forgetMark=route=>{
    try{
      const data=JSON.parse(localStorage.getItem(marksKey)||'{}');
      for(const [slug,mark] of Object.entries(data))if(mark&&mark.bookRoute===route)delete data[slug];
      localStorage.setItem(marksKey,JSON.stringify(data));
    }catch{}
  };
  const pct=mark=>Math.max(0,Math.min(100,Math.round((Number(mark.progress)||0)*100)));
  const showProgress=(row,mark)=>{
    let box=row.querySelector('.saved-progress');
    if(!mark){box?.remove();row.classList.remove('is-reading');return;}
    if(!box){box=document.createElement('div');box.className='saved-progress';row.querySelector('a')?.after(box);}
    box.replaceChildren();
    const bar=document.createElement('div');bar.className='continue-bar';
    const fill=document.createElement('span');fill.style.width=pct(mark)+'%';bar.append(fill);
    const link=Object.assign(document.createElement('a'),{href:mark.route,textContent:`Seguir leyendo · ${pct(mark)} % ↗`});
    const detail=Object.assign(document.createElement('p'),{textContent:String(mark.chapterTitle||'')});
    box.append(bar,link,detail);row.classList.add('is-reading');
  };
  const readOnline=document.querySelector('[data-read-online]');
  if(readOnline&&saveButton){
    const mark=readMarks()[saveButton.dataset.saveRoute];
    if(mark){readOnline.href=mark.route;readOnline.textContent=`Seguir leyendo · ${pct(mark)} % ↗`;}
  }
  const message=document.querySelector('.save-message');
  const status=library?.querySelector('[data-library-status]');
  const rows=library ? [...library.querySelectorAll('[data-saved-route]')] : [];
  const announceError=()=>{
    const target=message||status;
    if(target) target.textContent='No se puede acceder a tu selección guardada. Comprueba que el almacenamiento del navegador esté permitido.';
  };
  const refresh=()=>{
    try {
      const saved=read();
      if(saveButton){const active=saved.includes(saveButton.dataset.saveRoute);saveButton.setAttribute('aria-pressed',String(active));saveButton.textContent=active?'Guardado · Quitar':'Guardar libro';}
      if(library){
        let count=0;const marks=readMarks();
        for(const row of rows){row.hidden=!saved.includes(row.dataset.savedRoute);if(!row.hidden)count++;showProgress(row,row.hidden?null:marks[row.dataset.savedRoute]);}
        // Lo que estás leyendo, primero y por orden de última lectura.
        const list=rows[0]?.parentElement;
        if(list)[...rows].sort((a,b)=>(marks[b.dataset.savedRoute]?.updated||0)-(marks[a.dataset.savedRoute]?.updated||0)).forEach(row=>list.append(row));status.textContent=count===1?'1 libro guardado':`${count} libros guardados`;library.querySelector('[data-library-empty]').hidden=count>0;}
    } catch {announceError();}
  };
  if(saveButton){
    saveButton.hidden=false;
    saveButton.addEventListener('click',()=>{
      try {
        const saved=read(), route=saveButton.dataset.saveRoute, exists=saved.includes(route);
        write(exists?saved.filter(value=>value!==route):[...saved,route]);
        track(exists ? 'book_unsaved' : 'book_saved', { route });
        refresh();message.textContent=exists?'Libro quitado de tu biblioteca.':'Libro guardado. Lo encontrarás en «Mi biblioteca».';
        if(window.gsap && matchMedia('(prefers-reduced-motion: no-preference)').matches) window.gsap.fromTo(saveButton,{scale:.96},{scale:1,duration:.25,ease:'power2.out',clearProps:'transform'});
      } catch {announceError();}
    });
  }
  if(library) library.addEventListener('click',event=>{
    const button=event.target.closest('[data-remove-route]');if(!button)return;
    try{
      const visibleButtons=rows.filter(row=>!row.hidden).map(row=>row.querySelector('[data-remove-route]'));
      const index=visibleButtons.indexOf(button);
      write(read().filter(value=>value!==button.dataset.removeRoute));forgetMark(button.dataset.removeRoute);refresh();
      const next=visibleButtons[index+1]||visibleButtons[index-1]||library.querySelector('.library-empty a');next?.focus();
    }catch{announceError();}
  });
  addEventListener('storage',event=>{if(event.key===key || event.key===marksKey || event.key===null)refresh();});
  refresh();
})();

// The same catalog, presented as a visual shelf or a compact reading list.
for (const listing of document.querySelectorAll('.category-listing')) {
  if(!listing.querySelector('.book-grid')) continue;
  const toolbar=document.createElement('div'); toolbar.className='view-controls';
  const label=document.createElement('span');label.textContent='Explora a tu manera';toolbar.append(label);
  const group=document.createElement('div');group.setAttribute('role','group');group.setAttribute('aria-label','Presentación de libros');toolbar.append(group);
  const buttons=[];
  const select=(mode,animate=false)=>{
    listing.dataset.view=mode;
    for(const button of buttons)button.setAttribute('aria-pressed',String(button.dataset.mode===mode));
    try{sessionStorage.setItem('biblioteca.catalog-view',mode)}catch{}
    if(animate && window.gsap && matchMedia('(prefers-reduced-motion: no-preference)').matches){
      const first=listing.querySelector('.book-grid');
      window.gsap.fromTo(first,{opacity:.5,y:8},{opacity:1,y:0,duration:.3,ease:'power2.out',clearProps:'all'});
    }
  };
  for(const [mode,text] of [['grid','Portadas'],['list','Lista']]){
    const button=document.createElement('button');button.type='button';button.dataset.mode=mode;button.textContent=text;button.addEventListener('click',()=>select(mode,true));buttons.push(button);group.append(button);
  }
  listing.prepend(toolbar);
  let mode='grid';try{if(sessionStorage.getItem('biblioteca.catalog-view')==='list')mode='list'}catch{}
  select(mode);
}

// Reading appearance is local to the current page; content and URLs stay intact.
if(document.querySelector('.reader-v2')){
 const toolbar=document.querySelector('.reader-toolbar');toolbar.hidden=false;
 let readingSize=19;
 toolbar.addEventListener('click',async event=>{
  const button=event.target.closest('button');if(!button)return;
  if(button.dataset.paper){document.body.dataset.paper=button.dataset.paper;toolbar.querySelectorAll('[data-paper]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));}
  if(button.dataset.textSize){readingSize=Math.max(16,Math.min(28,readingSize+Number(button.dataset.textSize)));document.body.style.setProperty('--reading-size',readingSize+'px');toolbar.querySelectorAll('[data-text-size]').forEach(b=>b.disabled=(readingSize===16&&Number(b.dataset.textSize)<0)||(readingSize===28&&Number(b.dataset.textSize)>0));}
  if(button.hasAttribute('data-text-font')){const sans=button.getAttribute('aria-pressed')!=='true';button.setAttribute('aria-pressed',String(sans));document.body.style.setProperty('--reading-font',sans?'Inter, sans-serif':'Georgia, serif');}
  if(button.hasAttribute('data-share-page')){try{await navigator.clipboard.writeText(location.origin+location.pathname);toolbar.querySelector('[data-reader-status]').textContent='Enlace copiado.';}catch{toolbar.querySelector('[data-reader-status]').textContent='Puedes copiar el enlace desde la barra de direcciones.';}}
 });
}


// Seguir leyendo: muestra en la portada y en Mi biblioteca el punto donde se dejó cada lectura online.
// Los datos los guarda lector-libro.js en este navegador. Nunca se insertan como HTML.
(() => {
  // En «Mi biblioteca» el progreso va dentro de cada libro guardado; aquí solo la portada.
  const home = location.pathname === '/' ? document.querySelector('main > section') : null
  if (!home) return
  let marks = []
  try {
    const data = JSON.parse(localStorage.getItem('biblioteca.lectura.v1') || '{}')
    marks = Object.values(data && typeof data === 'object' ? data : {})
      .filter(m => m && /^\/leer\/[\w-]+\/([\w-]+\/)?$/.test(m.route || '') && typeof m.bookTitle === 'string')
      .sort((a, b) => (b.updated || 0) - (a.updated || 0)).slice(0, 3)
  } catch { return }
  if (!marks.length) return
  const section = document.createElement('section')
  section.className = 'dashboard-route continue-reading-home'
  const text = document.createElement('div')
  const eyebrow = Object.assign(document.createElement('p'), { className: 'eyebrow', textContent: 'Seguir leyendo' })
  const title = Object.assign(document.createElement('h2'), { textContent: marks[0].bookTitle })
  const pct = Math.max(0, Math.min(100, Math.round((Number(marks[0].progress) || 0) * 100)))
  const detail = Object.assign(document.createElement('p'), { textContent: `${marks[0].chapterTitle || ''} · ${pct} % leído` })
  text.append(eyebrow, title, detail)
  for (const other of marks.slice(1)) {
    const link = Object.assign(document.createElement('a'), { href: other.route, textContent: `También: ${other.bookTitle} ↗` })
    const line = document.createElement('p'); line.append(link); text.append(line)
  }
  const button = Object.assign(document.createElement('a'), { className: 'button', href: marks[0].route, textContent: 'Continuar donde lo dejaste ↗' })
  section.append(text, button)
  home.after(section)
})()

// Afiliados de Amazon por país: el lector va a la tienda donde puede comprar.
// Rellena la etiqueta de cada tienda; mientras esté vacía, los enlaces se quedan en amazon.es.
;(() => {
  const STORES = {
    mx: { host: 'www.amazon.com.mx', tag: '' },  // México
    us: { host: 'www.amazon.com', tag: '' },     // EE. UU. y resto de América
  };
  const AMERICA = ['US', 'AR', 'BO', 'CL', 'CO', 'CR', 'CU', 'DO', 'EC', 'SV', 'GT', 'HN', 'NI', 'PA', 'PY', 'PE', 'PR', 'UY', 'VE'];
  const links = document.querySelectorAll('a[data-query][href*="amazon.es"]');
  if (!links.length || !Object.values(STORES).some((store) => store.tag)) return;
  const apply = (country) => {
    const store = country === 'MX' ? STORES.mx : AMERICA.includes(country) ? STORES.us : null;
    if (!store || !store.tag) return;
    links.forEach((link) => {
      link.href = `https://${store.host}/s?k=${link.dataset.query}&i=stripbooks&tag=${store.tag}`;
    });
  };
  let cached = null;
  try { cached = sessionStorage.getItem('biblioteca.pais'); } catch (error) {}
  if (cached !== null) return apply(cached);
  fetch('/api/pais').then((response) => response.json()).then(({ country }) => {
    try { sessionStorage.setItem('biblioteca.pais', country || ''); } catch (error) {}
    apply(country || '');
  }).catch(() => {});
})();
