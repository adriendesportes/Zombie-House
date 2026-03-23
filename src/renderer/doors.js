// ==================== DOORS ====================
import * as THREE from 'three';
import { WALL, DOOR, COLS, ROWS, MAP, hash } from '../state.js';

export function buildDoor3D(scene, renderer, r, c, startOpen = false){
  const group = new THREE.Group();
  const H = 0.75;
  const THICKNESS = 0.06;

  // Detect wall orientation
  const wallLeft = c > 0 && (renderer.wallDataIndestructible.some(w=>w.r===r&&w.c===c-1));
  const wallRight = c < COLS-1 && (renderer.wallDataIndestructible.some(w=>w.r===r&&w.c===c+1));
  const isHoriz = wallLeft || wallRight;

  const frameMat = new THREE.MeshToonMaterial({color: 0x4a2d18});
  const lintelMat = new THREE.MeshToonMaterial({color: 0x6a4530});

  // Door panel texture
  const loader = new THREE.TextureLoader();
  const doorTex = loader.load('public/assets/tilesets/door-atlas.png');
  doorTex.magFilter = THREE.NearestFilter;
  doorTex.colorSpace = THREE.SRGBColorSpace;
  const variant = hash(r, c, 900) % 3;
  doorTex.repeat.set(1/3, 1);
  doorTex.offset.set(variant/3, 0);

  const doorMat = new THREE.MeshToonMaterial({map: doorTex, side: THREE.DoubleSide});

  const doorPivot = new THREE.Group();

  if(isHoriz){
    const pGeo = new THREE.BoxGeometry(0.08, H, 0.08);
    const pL = new THREE.Mesh(pGeo, frameMat); pL.position.set(-0.46, H/2, 0); group.add(pL);
    const pR = new THREE.Mesh(pGeo, frameMat); pR.position.set(0.46, H/2, 0); group.add(pR);
    const tGeo = new THREE.BoxGeometry(1, 0.08, 0.1);
    const tM = new THREE.Mesh(tGeo, lintelMat); tM.position.set(0, H + 0.04, 0); group.add(tM);

    const dGeo = new THREE.PlaneGeometry(0.84, H - 0.02);
    const door = new THREE.Mesh(dGeo, doorMat);
    door.position.set(0.42, 0, 0);
    doorPivot.add(door);
    doorPivot.position.set(-0.42, H/2, 0);
  } else {
    const pGeo = new THREE.BoxGeometry(0.08, H, 0.08);
    const pL = new THREE.Mesh(pGeo, frameMat); pL.position.set(0, H/2, -0.46); group.add(pL);
    const pR = new THREE.Mesh(pGeo, frameMat); pR.position.set(0, H/2, 0.46); group.add(pR);
    const tGeo = new THREE.BoxGeometry(0.1, 0.08, 1);
    const tM = new THREE.Mesh(tGeo, lintelMat); tM.position.set(0, H + 0.04, 0); group.add(tM);

    const dGeo = new THREE.PlaneGeometry(0.84, H - 0.02);
    const door = new THREE.Mesh(dGeo, doorMat);
    door.rotation.y = Math.PI / 2;
    door.position.set(0, 0, 0.42);
    doorPivot.add(door);
    doorPivot.position.set(0, H/2, -0.42);
  }

  group.add(doorPivot);
  group.position.set(c + 0.5, 0, r + 0.5);
  group.userData = {r, c, isOpen: startOpen, doorPivot, isHoriz};
  scene.add(group);
  renderer.doorMeshes.push(group);

  // Glowing halo on both sides of closed door (light seeping through)
  for(const side of [-1, 1]){
    const haloGeo = new THREE.PlaneGeometry(
      isHoriz ? 1.2 : 0.6,
      isHoriz ? 0.6 : 1.2
    );
    const haloMat = new THREE.MeshBasicMaterial({
      color: 0xffaa44, transparent: true, opacity: 0.3,
      side: THREE.DoubleSide, depthWrite: false,
    });
    const halo = new THREE.Mesh(haloGeo, haloMat);
    halo.rotation.x = -Math.PI / 2;
    halo.position.set(
      isHoriz ? 0 : side * 0.6,
      0.03,
      isHoriz ? side * 0.6 : 0
    );
    group.add(halo);
  }

  // No PointLights (perf) — halos are enough for the visual effect

  if(startOpen){
    doorPivot.rotation.y = isHoriz ? -Math.PI / 2 : -Math.PI / 2;
    MAP[r][c] = DOOR;
    group.children.forEach(ch => { if(ch.material && ch.material.transparent) ch.visible = false; });
  } else {
    MAP[r][c] = WALL;
  }
}

export function buildGrandDoor(scene, renderer, r, c, w){
  const loader = new THREE.TextureLoader();
  const tex = loader.load('public/assets/tilesets/furniture-grand_door.png');
  tex.magFilter = THREE.NearestFilter;
  tex.colorSpace = THREE.SRGBColorSpace;

  const fw = w || 4;
  const H = 0.95;
  const W = fw;
  const group = new THREE.Group();

  const frameMat = new THREE.MeshToonMaterial({color: 0x5a4a3a});
  const pGeo = new THREE.BoxGeometry(0.2, H, 0.2);
  const pL = new THREE.Mesh(pGeo, frameMat); pL.position.set(-W/2 - 0.1, H/2, 0); group.add(pL);
  const pR = new THREE.Mesh(pGeo, frameMat); pR.position.set(W/2 + 0.1, H/2, 0); group.add(pR);
  const tGeo = new THREE.BoxGeometry(W + 0.4, 0.15, 0.2);
  const tM = new THREE.Mesh(tGeo, new THREE.MeshToonMaterial({color: 0x6a5a48}));
  tM.position.set(0, H + 0.08, 0); group.add(tM);

  // Left door panel
  const texL = tex.clone(); texL.needsUpdate = true;
  texL.repeat.set(0.5, 1); texL.offset.set(0, 0);
  const dGeo = new THREE.PlaneGeometry(W/2 - 0.05, H - 0.05);
  const dL = new THREE.Mesh(dGeo, new THREE.MeshToonMaterial({map: texL, side: THREE.DoubleSide}));
  const pivotL = new THREE.Group();
  dL.position.set(W/4, 0, 0);
  pivotL.add(dL);
  pivotL.position.set(-W/2 + 0.05, H/2, 0);
  pivotL.rotation.y = 0; // closed
  group.add(pivotL);

  // Right door panel
  const texR = tex.clone(); texR.needsUpdate = true;
  texR.repeat.set(0.5, 1); texR.offset.set(0.5, 0);
  const dR = new THREE.Mesh(dGeo, new THREE.MeshToonMaterial({map: texR, side: THREE.DoubleSide}));
  const pivotR = new THREE.Group();
  dR.position.set(-W/4, 0, 0);
  pivotR.add(dR);
  pivotR.position.set(W/2 - 0.05, H/2, 0);
  pivotR.rotation.y = 0; // closed
  group.add(pivotR);

  group.position.set(c + fw/2, 0, r + 0.5);
  group.userData = {r, c, fw, isOpen: false, pivotL, pivotR};
  scene.add(group);

  // Block entrance tiles (closed by default)
  for(let dc = 0; dc < fw; dc++){
    if(c + dc < COLS) MAP[r][c + dc] = WALL;
  }

  // Store reference for opening later
  if(!renderer.grandDoor) renderer.grandDoor = group;
}
