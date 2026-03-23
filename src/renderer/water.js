// ==================== WATER ====================
import * as THREE from 'three';
import { WATER, COLS, ROWS, MAP } from '../state.js';

export function buildWater(scene, renderer){
  const waterTiles = [];
  for(let r=0; r<ROWS; r++) for(let c=0; c<COLS; c++) if(MAP[r][c]===WATER) waterTiles.push({r,c});
  if(waterTiles.length===0) return;

  // Dark riverbed
  const riverbedGeo = new THREE.PlaneGeometry(COLS, ROWS);
  const riverbedMat = new THREE.MeshBasicMaterial({color: 0x06101a});
  const riverbed = new THREE.Mesh(riverbedGeo, riverbedMat);
  riverbed.rotation.x = -Math.PI/2;
  riverbed.position.set(COLS/2, -0.08, ROWS/2);
  scene.add(riverbed);

  // Water planes
  renderer._waterPlanes = [];
  const waterMat = new THREE.MeshToonMaterial({
    color: 0x102848, transparent: true, opacity: 0.75, depthWrite: false
  });
  for(const {r,c} of waterTiles){
    const geo = new THREE.PlaneGeometry(1.15, 1.15, 6, 6);
    const mesh = new THREE.Mesh(geo, waterMat.clone());
    mesh.rotation.x = -Math.PI/2;
    mesh.position.set(c+0.5, -0.01, r+0.5);
    mesh.renderOrder = 1;
    scene.add(mesh);
    renderer._waterPlanes.push({mesh, geo, posAttr: geo.attributes.position, r, c});
  }

  // Drawbridge
  const bCX = 19 + 4/2;
  const bCZ = 29.5;
  const bW = 4.0;
  const bL = 1.0;
  const bridgeMat = new THREE.MeshToonMaterial({color: 0x6a4a2a});
  const bridgeDarkMat = new THREE.MeshToonMaterial({color: 0x4a3018});
  const bridgeRailMat = new THREE.MeshToonMaterial({color: 0x5a3a20});

  const deckGeo = new THREE.BoxGeometry(bW, 0.1, bL);
  const deck = new THREE.Mesh(deckGeo, bridgeMat);
  deck.position.set(bCX, 0.05, bCZ);
  scene.add(deck);

  for(let pz = -bL/2 + 0.1; pz <= bL/2 - 0.05; pz += 0.18){
    const plank = new THREE.Mesh(
      new THREE.BoxGeometry(bW, 0.11, 0.03), bridgeDarkMat
    );
    plank.position.set(bCX, 0.06, bCZ + pz);
    scene.add(plank);
  }

  for(const side of [-1, 1]){
    const rx = bCX + side * bW/2;
    for(const pz of [-bL/2 + 0.05, bL/2 - 0.05]){
      const post = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.3, 0.06), bridgeRailMat);
      post.position.set(rx, 0.2, bCZ + pz);
      scene.add(post);
    }
    const rail = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.04, bL - 0.1), bridgeRailMat);
    rail.position.set(rx, 0.32, bCZ);
    scene.add(rail);
  }
}
