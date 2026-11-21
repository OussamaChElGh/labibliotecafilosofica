import * as THREE from './vendor/three.module.js';
import { RoomEnvironment } from './vendor/RoomEnvironment.js';

export async function mountScene(hero, cancelled) {
  const stage = hero.querySelector('.folio-stage');
  const pauseButton = hero.querySelector('.folio-pause');
  const label = hero.querySelector('.folio-selection');
  const labelLink = label.querySelector('a');
  const response = await fetch('/folio-books.json');
  if (!response.ok) throw new Error('Catálogo de portadas no disponible');
  const data = await response.json();
  if (cancelled()) return;
  const renderer = new THREE.WebGLRenderer({alpha:true, antialias:true, powerPreference:'low-power'});
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(19.5, 1, .1, 100);
  camera.position.set(3.6, 2.15, 7.4);
  camera.lookAt(-1.4, .05, -.6);
  const pmrem = new THREE.PMREMGenerator(renderer);
  const room = new RoomEnvironment();
  const environment = pmrem.fromScene(room, .04);
  scene.environment = environment.texture;
  room.dispose(); pmrem.dispose();
  const key = new THREE.DirectionalLight('#fff3e4', 2.4); key.position.set(-4,6,6); scene.add(key);
  const rim = new THREE.DirectionalLight('#bfd2ff', 1.1); rim.position.set(6,3,-4); scene.add(rim);
  scene.add(new THREE.AmbientLight(0xffffff,.12));
  const geometry = new THREE.BoxGeometry(1,1.5,.2);
  const textures = [];
  const materials = [];
  function paper(vertical) {
    const canvas = document.createElement('canvas'); canvas.width=canvas.height=256;
    const ctx=canvas.getContext('2d'); ctx.fillStyle='#efe7d6'; ctx.fillRect(0,0,256,256);
    for(let i=0;i<256;i+=2){ctx.fillStyle=`rgba(110,85,50,${.05+(i%7)*.02})`;ctx.fillRect(vertical?i:0,vertical?0:i,vertical?1:256,vertical?256:1);}
    const texture=new THREE.CanvasTexture(canvas);texture.colorSpace=THREE.SRGBColorSpace;textures.push(texture);
    const material=new THREE.MeshStandardMaterial({map:texture,roughness:.9,envMapIntensity:.55});materials.push(material);return material;
  }
  const edge = paper(false), ends = paper(true);
  const loader = new THREE.TextureLoader();
  // allSettled ensures late textures can also be disposed if a request fails.
  const loaded = await Promise.allSettled(data.map(book => loader.loadAsync(book.cover).then(texture => {textures.push(texture);return texture;})));
  const release = () => { geometry.dispose(); materials.forEach(m=>m.dispose()); textures.forEach(t=>t.dispose()); environment.dispose(); renderer.dispose(); renderer.domElement.remove(); };
  if(cancelled() || loaded.some(r=>r.status==='rejected')) {release();return;}
  const books = data.map((book,i) => {
    const texture=loaded[i].value;texture.colorSpace=THREE.SRGBColorSpace;texture.anisotropy=Math.min(8,renderer.capabilities.getMaxAnisotropy());
    const color = new THREE.Color(book.spineColor).multiplyScalar(.62);
    const spine=new THREE.MeshPhysicalMaterial({color,roughness:.55,clearcoat:.3,envMapIntensity:.55});
    const cover=new THREE.MeshPhysicalMaterial({map:texture,roughness:.42,clearcoat:.55,clearcoatRoughness:.35,envMapIntensity:.55});
    const back=new THREE.MeshStandardMaterial({color,roughness:.6,envMapIntensity:.55}); materials.push(spine,cover,back);
    const mesh=new THREE.Mesh(geometry,[edge,spine,ends,ends,cover,back]);
    mesh.userData.index=i;mesh.position.y=-3;
    const group=new THREE.Group();group.position.set(1.55-i*.5,-1.12,.9-i*.2);group.rotation.y=.32;group.add(mesh);scene.add(group);
    return {mesh,group,y:-3,z:0,vy:0,vz:0,sx:0,sy:0};
  });
  let width=1,height=1,frame=0,last=0,elapsed=0,visible=true,paused=false,disposed=false,pointer=null;
  const project=new THREE.Vector3(),raycaster=new THREE.Raycaster(),ndc=new THREE.Vector2();
  let selected=0;
  const events=new AbortController(); const options={signal:events.signal};
  const updateLabel=index=>{
    if(index===selected && labelLink.dataset.ready) return;
    selected=index;const book=data[index];labelLink.href=book.href;labelLink.textContent=book.title;
    const author=document.createElement('small');author.textContent=` — ${book.author} ↗`;labelLink.append(author);labelLink.dataset.ready='true';
  };
  function resize(){width=hero.clientWidth;height=hero.clientHeight;renderer.setSize(width,height,false);camera.aspect=width/height;camera.updateProjectionMatrix();wake();}
  function wake(){if(!frame && !disposed && visible && !document.hidden) frame=requestAnimationFrame(render);}
  function render(now){
    frame=0;if(disposed || !visible || document.hidden)return;
    const dt=Math.min(last?(now-last)/1000:1/60,.05);last=now;elapsed+=dt;
    let moving=false;
    for(let i=0;i<books.length;i++){
      const b=books[i];
      // Stable base projection avoids chasing a book as it rises.
      project.set(0,.1,0);b.group.localToWorld(project);project.project(camera);
      b.sx=(project.x*.5+.5)*width;b.sy=(-project.y*.5+.5)*height;
      const spread=Math.max(width,height)*.085;
      const influence=pointer&&!paused?Math.exp(-((b.sx-pointer.x)**2+((b.sy-pointer.y)*.55)**2)/(spread*spread)):0;
      const target=elapsed<.25+(books.length-i)*.035?-3:.78*influence;
      for(let n=0;n<4;n++){const h=dt/4;b.vy+=((target-b.y)*70-b.vy*12.5)*h;b.y+=b.vy*h;b.vz+=((Math.max(target,0)*.35-b.z)*70-b.vz*12.5)*h;b.z+=b.vz*h;}
      b.mesh.position.set(0,b.y,b.z);b.mesh.rotation.x=-b.vy*.012;
      if(Math.abs(target-b.y)>.001 || Math.abs(b.vy)>.001 || Math.abs(b.vz)>.001)moving=true;
    }
    renderer.render(scene,camera);
    if(moving || elapsed<2)wake();else last=0;
  }
  function pick(event){
    const rect=hero.getBoundingClientRect();const x=event.clientX-rect.left,y=event.clientY-rect.top;
    ndc.set(x/width*2-1,1-y/height*2);raycaster.setFromCamera(ndc,camera);
    return raycaster.intersectObjects(books.map(b=>b.mesh),false)[0]?.object.userData.index;
  }
  hero.addEventListener('pointermove',event=>{
    if(event.target.closest('a,button,summary,input')){pointer=null;hero.style.cursor='';wake();return;}
    const rect=hero.getBoundingClientRect();pointer={x:event.clientX-rect.left,y:event.clientY-rect.top};
    const index=pick(event);hero.style.cursor=index===undefined?'':'pointer';if(index!==undefined)updateLabel(index);wake();
  },options);
  const leave=()=>{pointer=null;hero.style.cursor='';wake();};
  hero.addEventListener('pointerleave',leave,options);window.addEventListener('blur',leave,options);
  let down;
  hero.addEventListener('pointerdown',e=>{down={x:e.clientX,y:e.clientY};},options);
  hero.addEventListener('click',event=>{
    if(event.target.closest('a,button,summary,input') || !down || Math.hypot(event.clientX-down.x,event.clientY-down.y)>6)return;
    const index=pick(event);if(index!==undefined)hero.dispatchEvent(new CustomEvent('folio:select-book',{bubbles:true,detail:{index}}));
  },options);
  hero.addEventListener('keydown',event=>{if(event.key==='Escape'){leave();labelLink.blur();}},options);
  pauseButton.addEventListener('click',()=>{
    paused=!paused;pauseButton.textContent=paused?'Activar animación':'Pausar animación';pauseButton.setAttribute('aria-pressed',String(paused));
    if(paused){elapsed=3;for(const b of books){b.y=b.z=b.vy=b.vz=0;}}wake();
  },options);
  document.addEventListener('visibilitychange',()=>{last=0;if(document.hidden){cancelAnimationFrame(frame);frame=0;}else wake();},options);
  const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;last=0;if(visible)wake();else{cancelAnimationFrame(frame);frame=0;}},{threshold:0});observer.observe(hero);
  const resizer=new ResizeObserver(resize);resizer.observe(hero);
  function dispose(){if(disposed)return;disposed=true;events.abort();observer.disconnect();resizer.disconnect();cancelAnimationFrame(frame);hero.classList.remove('is-3d');hero.style.cursor='';pauseButton.hidden=label.hidden=true;release();}
  renderer.domElement.addEventListener('webglcontextlost',event=>{event.preventDefault();dispose();},options);
  stage.append(renderer.domElement);hero.classList.add('is-3d');pauseButton.hidden=label.hidden=false;updateLabel(0);resize();
  return dispose;
}
