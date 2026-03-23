// ==================== CHARACTERS (player + zombies) ====================
import * as THREE from 'three';

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

  // Health bar background
  const hbBgGeo = new THREE.PlaneGeometry(0.5, 0.07);
  const hbBgMat = new THREE.MeshBasicMaterial({color: 0x333333, side: THREE.DoubleSide, depthWrite: false, transparent: true});
  const hbBg = new THREE.Mesh(hbBgGeo, hbBgMat);
  hbBg.position.y = 1.45;
  group.add(hbBg);

  // Health bar fill
  const hbGeo = new THREE.PlaneGeometry(0.48, 0.05);
  const hbMat = new THREE.MeshBasicMaterial({color: 0x44dd44, side: THREE.DoubleSide, depthWrite: false, transparent: true});
  const hb = new THREE.Mesh(hbGeo, hbMat);
  hb.position.y = 1.45;
  group.add(hb);

  return {group, hb, hbMat, sprite, spriteMat, sheets, currentSheet: 'idleBack'};
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

  // Health bar background
  const hbBgGeo = new THREE.PlaneGeometry(0.44, 0.065);
  const hbBgMat = new THREE.MeshBasicMaterial({color: 0x333333, side: THREE.DoubleSide, depthWrite: false, transparent: true});
  const hbBg = new THREE.Mesh(hbBgGeo, hbBgMat);
  hbBg.position.y = 1.35;
  group.add(hbBg);

  // Health bar fill
  const hbGeo = new THREE.PlaneGeometry(0.42, 0.05);
  const hbMat = new THREE.MeshBasicMaterial({color: 0xdd4444, side: THREE.DoubleSide, depthWrite: false, transparent: true});
  const hb = new THREE.Mesh(hbGeo, hbMat);
  hb.position.y = 1.35;
  group.add(hb);

  return {group, hb, hbMat, sprite, spriteMat, sheets, currentSheet: 'idleFront'};
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
