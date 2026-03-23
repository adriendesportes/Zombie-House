// ==================== CHARACTERS (player + zombies) ====================
import * as THREE from 'three';

// Create a health bar as a Sprite with canvas texture (always faces camera)
function createHealthBar(width, height, color){
  const canvas = document.createElement('canvas');
  canvas.width = 64;
  canvas.height = 8;
  const ctx = canvas.getContext('2d');
  // Background
  ctx.fillStyle = '#333333';
  ctx.fillRect(0, 0, 64, 8);
  // Fill
  ctx.fillStyle = color;
  ctx.fillRect(1, 1, 62, 6);

  const tex = new THREE.CanvasTexture(canvas);
  tex.magFilter = THREE.NearestFilter;
  const mat = new THREE.SpriteMaterial({map: tex, transparent: true, depthWrite: false});
  const sprite = new THREE.Sprite(mat);
  sprite.scale.set(width, height, 1);
  sprite.center.set(0.5, 0.5);
  return {sprite, canvas, ctx, tex};
}

function updateHealthBar(hb, ratio){
  const ctx = hb.ctx;
  ctx.clearRect(0, 0, 64, 8);
  // Background
  ctx.fillStyle = '#333333';
  ctx.fillRect(0, 0, 64, 8);
  // Fill
  ctx.fillStyle = hb.fillColor;
  ctx.fillRect(1, 1, Math.max(0, 62 * ratio), 6);
  hb.tex.needsUpdate = true;
}

export function buildPlayer(){
  const group = new THREE.Group();

  const loader = new THREE.TextureLoader();
  const sheets = {
    idleBack:  loader.load('public/assets/sprites/heroes/angel-monster/idle.png'),
    walkBack:  loader.load('public/assets/sprites/heroes/angel-monster/walk.png'),
    idleFront: loader.load('public/assets/sprites/heroes/angel-monster/idle-front.png'),
    walkFront: loader.load('public/assets/sprites/heroes/angel-monster/walk-front.png'),
  };
  for(const key in sheets){
    const tex = sheets[key];
    tex.magFilter = THREE.NearestFilter;
    tex.minFilter = THREE.NearestFilter;
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS = THREE.ClampToEdgeWrapping;
    tex.wrapT = THREE.ClampToEdgeWrapping;
  }
  const initTex = sheets.idleBack;
  initTex.repeat.set(1/4, 1);
  initTex.offset.set(0, 0);

  const spriteMat = new THREE.SpriteMaterial({
    map: initTex,
    transparent: true,
    depthWrite: false,
  });
  const sprite = new THREE.Sprite(spriteMat);
  sprite.scale.set(1.4, 1.4, 1);
  sprite.position.y = 0.7;
  sprite.center.set(0.5, 0.3);
  group.add(sprite);

  return {group, sprite, spriteMat, sheets, currentSheet: 'idleBack'};
}

export function buildZombie(z){
  const group = new THREE.Group();

  const loader = new THREE.TextureLoader();
  const sheets = {
    idleFront: loader.load('public/assets/sprites/enemies/zombie-normal/idle-front.png'),
    idleBack:  loader.load('public/assets/sprites/enemies/zombie-normal/idle-back.png'),
    walkFront: loader.load('public/assets/sprites/enemies/zombie-normal/walk-front.png'),
    walkBack:  loader.load('public/assets/sprites/enemies/zombie-normal/walk-back.png'),
  };
  for(const key in sheets){
    const tex = sheets[key];
    tex.magFilter = THREE.NearestFilter;
    tex.minFilter = THREE.NearestFilter;
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS = THREE.ClampToEdgeWrapping;
    tex.wrapT = THREE.ClampToEdgeWrapping;
  }
  const initTex = sheets.idleFront;
  initTex.repeat.set(1/4, 1);
  initTex.offset.set(0, 0);

  const spriteMat = new THREE.SpriteMaterial({
    map: initTex,
    transparent: true,
    depthWrite: false,
  });
  const sprite = new THREE.Sprite(spriteMat);
  const bossScale = z.isBoss ? 1.8 : 1.3;
  sprite.scale.set(bossScale, bossScale, 1);
  sprite.position.y = 0.65;
  sprite.center.set(0.5, 0.3);
  group.add(sprite);

  return {group, sprite, spriteMat, sheets, currentSheet: 'idleFront'};
}

export function makeShadow(){
  const geo = new THREE.CircleGeometry(0.28, 8);
  const mat = new THREE.MeshBasicMaterial({color: 0x000000, transparent: true, opacity: 0.35, depthWrite: false});
  const mesh = new THREE.Mesh(geo, mat);
  mesh.rotation.x = -Math.PI/2;
  mesh.position.y = 0.01;
  return mesh;
}

export function makeHalo(color){
  const geo = new THREE.RingGeometry(0.22, 0.32, 12);
  const mat = new THREE.MeshBasicMaterial({color, transparent: true, opacity: 0.6, depthWrite: false, side: THREE.DoubleSide});
  const mesh = new THREE.Mesh(geo, mat);
  mesh.rotation.x = -Math.PI/2;
  mesh.position.y = 0.02;
  return mesh;
}
