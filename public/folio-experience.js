const dialog=document.querySelector('.book-preview');
let booksPromise;
const books=()=>booksPromise ??= fetch('/folio-books.json').then(response=>{if(!response.ok)throw new Error('No disponible');return response.json();}).catch(error=>{booksPromise=undefined;throw error;});
let currentBook,previousFocus,openRequest=0;
const key='biblioteca.saved-books.v1';
const readSaved=()=>{
  const data=JSON.parse(localStorage.getItem(key)||'[]');
  if(!Array.isArray(data))throw new Error('Selección no disponible');
  return [...new Set(data.filter(value=>typeof value==='string' && /^\/[\w%\-/.]+\/$/.test(value)))];
};
function refreshSaved(){
  const button=dialog.querySelector('[data-preview-save]');
  try{const active=readSaved().includes(currentBook.href);button.textContent=active?'Guardado · Quitar':'Guardar libro';button.setAttribute('aria-pressed',String(active));}
  catch{dialog.querySelector('[data-preview-status]').textContent='No se puede acceder al almacenamiento de este navegador.';}
}
async function openPreview(index,source){
  const request=++openRequest;
  try{
    const entries=await books();if(request!==openRequest || !entries[index])return;
    currentBook=entries[index];previousFocus=source || document.activeElement;
    dialog.querySelector('#preview-title').textContent=currentBook.title;
    dialog.querySelector('[data-preview-author]').textContent=currentBook.author;
    const cover=dialog.querySelector('[data-preview-cover]');cover.src=currentBook.cover;cover.alt=`Portada de ${currentBook.title}`;
    dialog.querySelector('[data-preview-link]').href=currentBook.href;
    dialog.querySelector('[data-preview-status]').textContent='';refreshSaved();
    if(!dialog.open){dialog.showModal();document.documentElement.classList.add('preview-open');}
    dialog.querySelector('.preview-close').focus();
    if(window.gsap && !matchMedia('(prefers-reduced-motion:reduce)').matches)window.gsap.fromTo(dialog,{opacity:0,y:18},{opacity:1,y:0,duration:.3,ease:'power2.out',clearProps:'all'});
  }catch{
    const link=source?.closest('a') || source?.closest('.edition-card')?.querySelector('h3 a');
    if(link)location.assign(link.href);
    else document.querySelector('.folio-selection a')?.focus();
  }
}
document.querySelectorAll('button[data-preview-book]').forEach(button=>button.hidden=false);
document.addEventListener('click',event=>{
  const trigger=event.target.closest('[data-preview-book]');
  if(!trigger || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)return;
  event.preventDefault();openPreview(Number(trigger.dataset.previewBook),trigger);
});
document.addEventListener('folio:select-book',event=>openPreview(event.detail.index));
dialog.querySelector('.preview-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',event=>{if(event.target===dialog){const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();}});
dialog.addEventListener('close',()=>{openRequest++;document.documentElement.classList.remove('preview-open');previousFocus?.focus();});
dialog.querySelector('[data-preview-save]').addEventListener('click',()=>{
  try{
    const saved=readSaved(),exists=saved.includes(currentBook.href);
    localStorage.setItem(key,JSON.stringify(exists?saved.filter(path=>path!==currentBook.href):[...saved,currentBook.href]));
    refreshSaved();dialog.querySelector('[data-preview-status]').textContent=exists?'Libro quitado de Mi biblioteca.':'Libro guardado en Mi biblioteca.';
  }catch{dialog.querySelector('[data-preview-status]').textContent='No se ha podido guardar. Comprueba los permisos de almacenamiento del navegador.';}
});
window.addEventListener('storage',event=>{if(event.key===key&&dialog.open)refreshSaved();});

const filters=document.querySelector('.edition-filters');filters.hidden=false;
filters.addEventListener('click',event=>{
  const button=event.target.closest('[data-edition-filter]');if(!button)return;
  const category=button.dataset.editionFilter;let count=0;
  filters.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
  document.querySelectorAll('.edition-card').forEach(card=>{card.hidden=category!=='Todas'&&card.dataset.editionCategory!==category;if(!card.hidden)count++;});
  document.querySelector('.edition-count').textContent=`${count} libros en esta selección`;
});

const introductions=[
  {title:'¿Qué es la filosofía?',author:'Una primera orientación',text:'La filosofía es la práctica de examinar las preguntas fundamentales sobre la realidad, el conocimiento, la acción y la vida buena mediante razones, conceptos y argumentos.',href:'/que-es-filosofia/'},
  {title:'La República',author:'Una entrada a Platón',text:'La República es un diálogo sobre la justicia, la educación y la organización de la ciudad. Su recorrido va de la pregunta por la vida justa a la alegoría de la caverna.',href:'/la-republica-platon/'},
  {title:'Discurso del método',author:'Una entrada a René Descartes',text:'Descartes busca un punto de partida firme para el conocimiento: somete las creencias a duda, examina el pensamiento y reconstruye desde ahí la relación entre mente, mundo y verdad.',href:'/descartes-discurso-del-metodo-pdf/'}
];
const room=document.querySelector('.reading-room');
room.querySelector('[data-room-controls]').hidden=false;
room.querySelector('[data-room-select="0"]').setAttribute('aria-current','true');
room.addEventListener('click',event=>{
  const select=event.target.closest('[data-room-select]');
  if(select&&!event.ctrlKey&&!event.metaKey&&!event.shiftKey){
    event.preventDefault();const item=introductions[Number(select.dataset.roomSelect)];
    room.querySelectorAll('[data-room-select]').forEach(a=>a.removeAttribute('aria-current'));select.setAttribute('aria-current','true');
    room.querySelector('[data-room-title]').textContent=item.title;room.querySelector('[data-room-author]').textContent=item.author;room.querySelector('[data-room-text]').textContent=item.text;room.querySelector('[data-room-link]').href=item.href;
  }
});
let size=22;
const sizeButtons=[...room.querySelectorAll('[data-reader-size]')];
sizeButtons.forEach(button=>button.addEventListener('click',()=>{
  size=Math.max(18,Math.min(30,size+Number(button.dataset.readerSize)*2));room.querySelector('.room-paper').style.setProperty('--reader-size',`${size}px`);
  sizeButtons.forEach(b=>b.disabled=(size===18&&b.dataset.readerSize==='-1')||(size===30&&b.dataset.readerSize==='1'));
}));
room.querySelector('[data-reader-tone]').addEventListener('click',event=>{
  const active=room.querySelector('.room-paper').classList.toggle('is-noir');event.currentTarget.setAttribute('aria-pressed',String(active));event.currentTarget.textContent=active?'Papel claro':'Papel oscuro';
});
