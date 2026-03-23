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

// Direction angles for 8-directional sprites
const DIR_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315];

// Map angle to number of frames per animation
const PLAYER_FRAMES = { idle: 36, walk: 36 };
const ZOMBIE_FRAMES = { idle: 4, walk: 6 };

function loadDirectionalSheets(loader, basePath, frameConfig, filter){
  const sheets = {};
  for(const angle of DIR_ANGLES){
    for(const anim of Object.keys(frameConfig)){
      const key = `${anim}_${angle}`;
      sheets[key] = loader.load(`${basePath}/${anim}-${angle}.png`);
    }
  }
  for(const key in sheets){
    const tex = sheets[key];
    tex.magFilter = filter;
    tex.minFilter = filter;
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.wrapS = THREE.ClampToEdgeWrapping;
    tex.wrapT = THREE.ClampToEdgeWrapping;
  }
  return sheets;
}

// Convert facingDx/facingDy to nearest 45° angle
export function facingToAngle(dx, dy){
  const angle = (Math.atan2(dx, dy) * 180 / Math.PI + 360) % 360;
  const sector = Math.round(angle / 45) % 8;
  return sector * 45;
}

export function buildPlayer(){
  const group = new THREE.Group();

  const loader = new THREE.TextureLoader();
  const sheets = loadDirectionalSheets(
    loader, 'public/assets/sprites/heroes/angel-monster',
    PLAYER_FRAMES, THREE.LinearFilter
  );

  const initKey = 'idle_0';
  const initTex = sheets[initKey];
  initTex.repeat.set(1/PLAYER_FRAMES.idle, 1);
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

  return {group, sprite, spriteMat, sheets, currentSheet: initKey, frameConfig: PLAYER_FRAMES};
}

export function buildZombie(z){
  const group = new THREE.Group();

  const loader = new THREE.TextureLoader();
  const sheets = loadDirectionalSheets(
    loader, 'public/assets/sprites/enemies/zombie-normal',
    ZOMBIE_FRAMES, THREE.NearestFilter
  );

  const initKey = 'idle_0';
  const initTex = sheets[initKey];
  initTex.repeat.set(1/ZOMBIE_FRAMES.idle, 1);
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

  return {group, sprite, spriteMat, sheets, currentSheet: initKey, frameConfig: ZOMBIE_FRAMES};
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
