// ==================== TORCH LIGHTS ====================
import * as THREE from 'three';
import { DECO_TORCH, WALL, COLS, ROWS, MAP, DECO } from '../state.js';

export function buildTorchLights(scene, renderer){
  const bracketMat = new THREE.MeshToonMaterial({color: 0x3a3028});
  const stickMat = new THREE.MeshToonMaterial({color: 0x5a4030});
  const flameMat = new THREE.MeshToonMaterial({color: 0xff8820, emissive: 0xff6600, emissiveIntensity: 0.8});
  const flameCoreMat = new THREE.MeshToonMaterial({color: 0xffee88, emissive: 0xffdd44, emissiveIntensity: 1.0});

  for(let r=0; r<ROWS; r++){
    for(let c=0; c<COLS; c++){
      if(DECO[r][c]!==DECO_TORCH) continue;

      // Find nearest wall to attach torch to
      let wallDir = {x:0, z:0};
      if(r > 0 && MAP[r-1][c] === WALL) wallDir = {x:0, z:-0.45};
      else if(r < ROWS-1 && MAP[r+1][c] === WALL) wallDir = {x:0, z:0.45};
      else if(c > 0 && MAP[r][c-1] === WALL) wallDir = {x:-0.45, z:0};
      else if(c < COLS-1 && MAP[r][c+1] === WALL) wallDir = {x:0.45, z:0};

      const isEntrance = (r === 28 && (c === 18 || c === 23));
      const scale = isEntrance ? 1.8 : 1.0;

      let tx, tz, torchY;
      if(isEntrance){
        tx = c + 0.5;
        tz = r + 1.0;
        torchY = 0.0;
      } else {
        tx = c + 0.5 + wallDir.x;
        tz = r + 0.5 + wallDir.z;
        torchY = 0.65;
      }

      const group = new THREE.Group();

      const s = scale;
      const offX = -wallDir.x * 0.15 * s;
      const offZ = -wallDir.z * 0.15 * s;

      if(isEntrance){
        const pillar = new THREE.Mesh(new THREE.CylinderGeometry(0.06*s, 0.08*s, 0.9*s, 6), bracketMat);
        pillar.position.set(0, 0.45*s, 0);
        group.add(pillar);
        const base = new THREE.Mesh(new THREE.CylinderGeometry(0.12*s, 0.14*s, 0.08*s, 6), bracketMat);
        base.position.set(0, 0.02*s, 0);
        group.add(base);
        const brazier = new THREE.Mesh(new THREE.CylinderGeometry(0.12*s, 0.08*s, 0.12*s, 6), new THREE.MeshToonMaterial({color: 0x2a2018}));
        brazier.position.set(0, 0.92*s, 0);
        group.add(brazier);
        const flame = new THREE.Mesh(new THREE.SphereGeometry(0.12*s, 6, 5), flameMat);
        flame.scale.set(1, 2.0, 1);
        flame.position.set(0, 1.15*s, 0);
        group.add(flame);
        const core = new THREE.Mesh(new THREE.SphereGeometry(0.06*s, 4, 3), flameCoreMat);
        core.position.set(0, 1.2*s, 0);
        group.add(core);
      } else {
        const bracket = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.06, 0.2), bracketMat);
        bracket.position.set(0, torchY, 0);
        if(wallDir.z !== 0) bracket.rotation.y = Math.PI/2;
        group.add(bracket);
        const stick = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.04, 0.3, 5), stickMat);
        stick.position.set(offX, torchY + 0.15, offZ);
        group.add(stick);
        const flame = new THREE.Mesh(new THREE.SphereGeometry(0.08, 5, 4), flameMat);
        flame.scale.set(1, 1.5, 1);
        flame.position.set(offX, torchY + 0.35, offZ);
        group.add(flame);
        const core = new THREE.Mesh(new THREE.SphereGeometry(0.04, 4, 3), flameCoreMat);
        core.position.set(offX, torchY + 0.37, offZ);
        group.add(core);
      }

      group.position.set(tx, 0, tz);
      scene.add(group);

      const lightIntensity = isEntrance ? 4.0 : 2.5;
      const lightRange = isEntrance ? 12 : 8;
      const lightY = isEntrance ? 1.3 * scale : torchY + 0.4;
      const light = new THREE.PointLight(0xff8830, lightIntensity, lightRange);
      light.position.set(tx, lightY, tz);
      light.baseIntensity = lightIntensity;
      scene.add(light);
      const allChildren = group.children;
      const flameObj = allChildren.find(ch => ch.material === flameMat);
      const coreObj = allChildren.find(ch => ch.material === flameCoreMat);
      renderer.torchLights.push({light, flame: flameObj, core: coreObj, r, c});
    }
  }
}
