import './folio-experience.js';
const hero = document.querySelector('.folio-hero');
const reduced = matchMedia('(prefers-reduced-motion: reduce)');
const desktop = matchMedia('(min-width: 761px) and (pointer: fine)');
let disposeScene;
let generation = 0;
let motionContext;

function intro() {
  if (!window.gsap || reduced.matches) return;
  motionContext = window.gsap.context(() => {
    window.gsap.from('.folio-heading h1', {opacity:0,y:28,filter:'blur(10px)',duration:1.4,ease:'power3.out',clearProps:'all'});
    window.gsap.from('.folio-kicker,.folio-intro', {opacity:0,y:12,duration:.9,delay:.35,stagger:.15,clearProps:'all'});
  }, hero);
}

async function updateScene() {
  const ticket = ++generation;
  disposeScene?.(); disposeScene = undefined;
  if (reduced.matches) motionContext?.revert();
  if (!desktop.matches || reduced.matches || navigator.connection?.saveData) return;
  try {
    const { mountScene } = await import('./folio-scene.js');
    if (ticket !== generation) return;
    const cleanup = await mountScene(hero, () => ticket !== generation);
    if (ticket !== generation) cleanup?.(); else disposeScene = cleanup;
  } catch (error) {
    // The complete HTML shelf remains usable if WebGL or an asset fails.
    console.warn('Estantería 3D no disponible:', error.message);
  }
}

if (!reduced.matches) {
  const script = document.createElement('script');
  script.src = '/gsap.min.js'; script.onload = intro;
  document.head.append(script);
}
desktop.addEventListener('change', updateScene);
reduced.addEventListener('change', updateScene);
window.addEventListener('pagehide', () => { generation++; disposeScene?.(); motionContext?.revert(); });
window.addEventListener('pageshow', event => { if (event.persisted) updateScene(); });
if ('requestIdleCallback' in window) requestIdleCallback(updateScene, {timeout:1200});
else setTimeout(updateScene, 350);
