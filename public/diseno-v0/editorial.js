for (const [id,key] of [['layout','layout'],['density','density']]) {
  const control=document.getElementById(id);
  try { const saved=sessionStorage.getItem('biblioteca-v0-'+key); if(saved && [...control.options].some(o=>o.value===saved)) control.value=saved; } catch {}
  document.documentElement.dataset[key]=control.value;
  control.addEventListener('change',()=>{document.documentElement.dataset[key]=control.value;try{sessionStorage.setItem('biblioteca-v0-'+key,control.value)}catch{}});
}
document.addEventListener('keydown',event=>{if(event.key==='Escape'){const panel=document.querySelector('.tweaks');if(panel.open){panel.open=false;panel.querySelector('summary').focus()}}});
