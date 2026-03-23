// ==================== WALLS (InstancedMesh) ====================
import * as THREE from 'three';
import {
  WALL, WDEST, DOOR, COLS, ROWS, MAP, hash, hashF,
} from '../state.js';

export function buildWalls(scene, renderer){
  renderer.wallDataIndestructible = [];
  renderer.wallDataDestructible = [];
  renderer.doorMeshes = [];
  for(let r=0; r<ROWS; r++){
    for(let c=0; c<COLS; c++){
      if(MAP[r][c]===WALL) renderer.wallDataIndestructible.push({r,c});
      else if(MAP[r][c]===WDEST) renderer.wallDataDestructible.push({r,c});
    }
  }
  rebuildWallMeshes(scene, renderer);
}

export function rebuildWallMeshes(scene, renderer){
  // Remove old
  if(renderer.wallMeshIndestructible){ scene.remove(renderer.wallMeshIndestructible); if(renderer.wallMeshIndestructible.geometry) renderer.wallMeshIndestructible.geometry.dispose(); }
  if(renderer.wallMeshDestructible){ scene.remove(renderer.wallMeshDestructible); if(renderer.wallMeshDestructible.geometry) renderer.wallMeshDestructible.geometry.dispose(); }

  // Filter still-existing walls
  renderer.wallDataIndestructible = renderer.wallDataIndestructible.filter(w=>MAP[w.r][w.c]===WALL);
  renderer.wallDataDestructible = renderer.wallDataDestructible.filter(w=>MAP[w.r][w.c]===WDEST);

  const H_IND = 0.8, H_DES = 0.6;

  // Load wall textures from atlas
  const loader = new THREE.TextureLoader();
  const wallFrontTex = loader.load('public/assets/tilesets/wall-front-atlas.png');
  const wallTopTex = loader.load('public/assets/tilesets/wall-top-atlas.png');
  const extFrontTex = loader.load('public/assets/tilesets/wall-exterior-atlas.png');
  const extTopTex = loader.load('public/assets/tilesets/wall-exterior-top-atlas.png');
  const wallDestTex = loader.load('public/assets/tilesets/wall-dest-atlas.png');
  [wallFrontTex, wallTopTex, extFrontTex, extTopTex, wallDestTex].forEach(t => {
    t.magFilter = THREE.NearestFilter;
    t.minFilter = THREE.LinearFilter;
    t.colorSpace = THREE.SRGBColorSpace;
  });

  // Detect exterior walls
  const isExterior = (r, c) => (r === 3 || r === 28 || c === 3 || c === 36);

  for(const {r,c} of renderer.wallDataIndestructible){
    const ext = isExterior(r, c);
    const hv = hashF(r, c, 200);
    const geo = new THREE.BoxGeometry(1, H_IND, 1);

    let frontMat, topMat, sideMat;

    if(ext){
      const wv = hash(r, c, 500) % 5;
      frontMat = new THREE.MeshToonMaterial({color: 0xffffff});
      const ft = extFrontTex.clone(); ft.needsUpdate = true;
      ft.repeat.set(1/5, 1); ft.offset.set(wv/5, 0);
      frontMat.map = ft;

      topMat = new THREE.MeshToonMaterial({color: 0xffffff});
      const tt = extTopTex.clone(); tt.needsUpdate = true;
      tt.repeat.set(1/5, 1); tt.offset.set(wv/5, 0);
      topMat.map = tt;

      const sc = new THREE.Color(0x4a4845);
      sc.r = Math.min(1, sc.r + hv*0.05);
      sc.g = Math.min(1, sc.g + hv*0.04);
      sc.b = Math.min(1, sc.b + hv*0.03);
      sideMat = new THREE.MeshToonMaterial({color: sc});
    } else {
      const wv = hash(r, c, 500) % 9;
      const NV = 9;
      frontMat = new THREE.MeshToonMaterial({color: 0xffffff});
      const ft = wallFrontTex.clone(); ft.needsUpdate = true;
      ft.repeat.set(1/NV, 1); ft.offset.set(wv/NV, 0);
      frontMat.map = ft;

      topMat = new THREE.MeshToonMaterial({color: 0xffffff});
      const tt = wallTopTex.clone(); tt.needsUpdate = true;
      tt.repeat.set(1/NV, 1); tt.offset.set(wv/NV, 0);
      topMat.map = tt;

      const sideColors = [0x705848,0x555862,0x685040,0x506050,0x605860,0x353540,0x6a5040,0x504a45,0x506048];
      const sc = new THREE.Color(sideColors[wv] || 0x605050);
      sc.r = Math.min(1, sc.r + hv*0.08);
      sc.g = Math.min(1, sc.g + hv*0.06);
      sc.b = Math.min(1, sc.b + hv*0.05);
      sideMat = new THREE.MeshToonMaterial({color: sc});
    }

    const mats = [sideMat, sideMat, topMat, sideMat, frontMat, frontMat];
    const mesh = new THREE.Mesh(geo, mats);
    mesh.position.set(c+0.5, H_IND/2, r+0.5);
    scene.add(mesh);
  }
  renderer.wallMeshIndestructible = {dispose:()=>{}};

  // Destructible walls
  renderer._destWallMeshes = [];
  for(const {r,c} of renderer.wallDataDestructible){
    const wv = hash(r,c,550) % 3;
    const hv = hashF(r,c,201);

    const geo = new THREE.BoxGeometry(1, H_DES, 1);

    const frontMat = new THREE.MeshToonMaterial({color: 0xffffff});
    const frontTex = wallDestTex.clone();
    frontTex.needsUpdate = true;
    frontTex.repeat.set(1/3, 128/170);
    frontTex.offset.set(wv/3, 42/170);
    frontMat.map = frontTex;

    const topMat = new THREE.MeshToonMaterial({color: 0xffffff});
    const topTexC = wallDestTex.clone();
    topTexC.needsUpdate = true;
    topTexC.repeat.set(1/3, 128/170);
    topTexC.offset.set(wv/3, 42/170);
    topMat.map = topTexC;

    const sideColor = new THREE.Color([0xa08840, 0x906030, 0x888080][wv]);
    sideColor.r = Math.min(1, sideColor.r + hv*0.06);
    sideColor.g = Math.min(1, sideColor.g + hv*0.06);
    const sideMat = new THREE.MeshToonMaterial({color: sideColor});

    const mats = [sideMat, sideMat, topMat, sideMat, frontMat, frontMat];
    const mesh = new THREE.Mesh(geo, mats);
    mesh.position.set(c+0.5, H_DES/2, r+0.5);
    mesh.userData = {r, c};
    scene.add(mesh);
    renderer._destWallMeshes.push(mesh);
  }
  renderer.wallMeshDestructible = {dispose:()=>{}};
}
