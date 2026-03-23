// ==================== WALLS ====================
import * as THREE from 'three';
import {
  WALL, WDEST, COLS, ROWS, MAP, hash, hashF,
} from '../state.js';

// Pre-create materials for each wall variant (avoids texture cloning issues)
function makeMaterialsFromAtlas(url, numVariants, loader) {
  const mats = [];
  for(let i = 0; i < numVariants; i++){
    const tex = loader.load(url);
    tex.magFilter = THREE.NearestFilter;
    tex.minFilter = THREE.LinearFilter;
    tex.colorSpace = THREE.SRGBColorSpace;
    tex.repeat.set(1/numVariants, 1);
    tex.offset.set(i/numVariants, 0);
    mats.push(new THREE.MeshToonMaterial({map: tex}));
  }
  return mats;
}

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
  // Remove old meshes
  if(renderer._wallMeshList){
    for(const m of renderer._wallMeshList) scene.remove(m);
  }
  if(renderer._destWallMeshes){
    for(const m of renderer._destWallMeshes) scene.remove(m);
  }

  renderer.wallDataIndestructible = renderer.wallDataIndestructible.filter(w=>MAP[w.r][w.c]===WALL);
  renderer.wallDataDestructible = renderer.wallDataDestructible.filter(w=>MAP[w.r][w.c]===WDEST);

  const H_IND = 0.8, H_DES = 0.6;
  const loader = new THREE.TextureLoader();

  // Pre-create all material variants (each loads its own texture = no cloning)
  const extFrontMats = makeMaterialsFromAtlas('public/assets/tilesets/wall-exterior-atlas.png', 5, loader);
  const extTopMats = makeMaterialsFromAtlas('public/assets/tilesets/wall-exterior-top-atlas.png', 5, loader);
  const intFrontMats = makeMaterialsFromAtlas('public/assets/tilesets/wall-front-atlas.png', 9, loader);
  const intTopMats = makeMaterialsFromAtlas('public/assets/tilesets/wall-top-atlas.png', 9, loader);
  const destFrontMats = makeMaterialsFromAtlas('public/assets/tilesets/wall-dest-atlas.png', 3, loader);

  const isExterior = (r, c) => (r === 3 || r === 28 || c === 3 || c === 36);

  // Indestructible walls
  renderer._wallMeshList = [];
  const geo = new THREE.BoxGeometry(1, H_IND, 1);

  for(const {r,c} of renderer.wallDataIndestructible){
    const ext = isExterior(r, c);
    const hv = hashF(r, c, 200);

    let frontMat, topMat, sideMat;

    if(ext){
      const wv = hash(r, c, 500) % 5;
      frontMat = extFrontMats[wv];
      topMat = extTopMats[wv];
      const sc = new THREE.Color(0x4a4845);
      sc.r = Math.min(1, sc.r + hv*0.05);
      sc.g = Math.min(1, sc.g + hv*0.04);
      sc.b = Math.min(1, sc.b + hv*0.03);
      sideMat = new THREE.MeshToonMaterial({color: sc});
    } else {
      // Interior walls: wood (variant 2)
      const wv = 2;
      frontMat = intFrontMats[wv];
      topMat = intTopMats[wv];
      const sideColors = [0x705848,0x555862,0x685040,0x506050,0x605860,0x353540,0x6a5040,0x504a45,0x506048];
      const sc = new THREE.Color(sideColors[wv]);
      sc.r = Math.min(1, sc.r + hv*0.08);
      sc.g = Math.min(1, sc.g + hv*0.06);
      sc.b = Math.min(1, sc.b + hv*0.05);
      sideMat = new THREE.MeshToonMaterial({color: sc});
    }

    const mats = [sideMat, sideMat, topMat, sideMat, frontMat, frontMat];
    const mesh = new THREE.Mesh(geo, mats);
    mesh.position.set(c+0.5, H_IND/2, r+0.5);
    scene.add(mesh);
    renderer._wallMeshList.push(mesh);
  }
  renderer.wallMeshIndestructible = {dispose:()=>{}};

  // Destructible walls
  renderer._destWallMeshes = [];
  const destGeo = new THREE.BoxGeometry(1, H_DES, 1);

  for(const {r,c} of renderer.wallDataDestructible){
    const wv = hash(r,c,550) % 3;
    const hv = hashF(r,c,201);

    const frontMat = destFrontMats[wv];

    const sideColor = new THREE.Color([0xa08840, 0x906030, 0x888080][wv]);
    sideColor.r = Math.min(1, sideColor.r + hv*0.06);
    sideColor.g = Math.min(1, sideColor.g + hv*0.06);
    const sideMat = new THREE.MeshToonMaterial({color: sideColor});

    const mats = [sideMat, sideMat, frontMat, sideMat, frontMat, frontMat];
    const mesh = new THREE.Mesh(destGeo, mats);
    mesh.position.set(c+0.5, H_DES/2, r+0.5);
    mesh.userData = {r, c};
    scene.add(mesh);
    renderer._destWallMeshes.push(mesh);
  }
  renderer.wallMeshDestructible = {dispose:()=>{}};
}
