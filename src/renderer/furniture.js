// ==================== FURNITURE ====================
import * as THREE from 'three';
import { furnitureList } from '../state.js';
import { buildGrandDoor } from './doors.js';

export function buildFurniture(scene, renderer){
  for(const fm of renderer.furnitureMeshes) scene.remove(fm);
  renderer.furnitureMeshes = [];

  const loader = new THREE.TextureLoader();

  const heights = {
    bed: 0.35, long_table: 0.45, bookshelf: 0.8, bathtub: 0.4,
    wardrobe: 0.9, fireplace: 0.6, cradle: 0.35,
    chandelier: 0.05, grand_door: 0.7, stairs_broken: 0.5,
  };

  for(const f of furnitureList){
    const texPath = `public/assets/tilesets/furniture-${f.type}.png`;
    const tex = loader.load(texPath);
    tex.magFilter = THREE.NearestFilter;
    tex.minFilter = THREE.LinearFilter;
    tex.colorSpace = THREE.SRGBColorSpace;

    const fw = f.w || 1;
    const fh = f.h || 1;
    const H = heights[f.type] || 0.5;

    const geo = new THREE.BoxGeometry(fw * 0.95, H, fh * 0.95);
    const topMat = new THREE.MeshToonMaterial({map: tex, color: 0xffffff});
    const sideMat = new THREE.MeshToonMaterial({color: 0x6a4a32});
    const frontMat = new THREE.MeshToonMaterial({color: 0x5a3a28});

    // Broken stairs — 3D stepped construction
    if(f.type === 'stairs_broken'){
      const group = new THREE.Group();
      const stoneMat = new THREE.MeshToonMaterial({color: 0x68635a});
      const stoneHiMat = new THREE.MeshToonMaterial({color: 0x78736a});
      const stoneDkMat = new THREE.MeshToonMaterial({color: 0x504a42});
      const rubbleMat = new THREE.MeshToonMaterial({color: 0x5a5548});
      const railMat = new THREE.MeshToonMaterial({color: 0x4a3520});

      const stepsCount = 6;
      const stepW = fw * 0.95;
      const stepD = 0.28;
      const stepH = 0.12;

      for(let i = 0; i < stepsCount; i++){
        const isBroken = (i === 2 || i === 4);
        const y = i * stepH;
        const z = -i * stepD;

        if(isBroken){
          for(let frag = 0; frag < 4; frag++){
            const fragW = 0.15 + Math.random() * 0.25;
            const fragH = 0.04 + Math.random() * 0.06;
            const fragD = 0.08 + Math.random() * 0.12;
            const fragGeo = new THREE.BoxGeometry(fragW, fragH, fragD);
            const piece = new THREE.Mesh(fragGeo, rubbleMat);
            piece.position.set(
              (frag - 1.5) * 0.35 + (Math.random() - 0.5) * 0.2,
              y * 0.3 + fragH / 2,
              z + (Math.random() - 0.5) * 0.3
            );
            piece.rotation.set(Math.random() * 0.5, Math.random() * 1, Math.random() * 0.3);
            group.add(piece);
          }
        } else {
          const sGeo = new THREE.BoxGeometry(stepW, stepH, stepD);
          const mats = [stoneDkMat, stoneDkMat, stoneHiMat, stoneDkMat, stoneMat, stoneMat];
          const step = new THREE.Mesh(sGeo, mats);
          step.position.set(0, y + stepH / 2, z);
          group.add(step);

          if(i === 3){
            const chip = new THREE.Mesh(new THREE.BoxGeometry(0.2, stepH + 0.01, 0.08), rubbleMat);
            chip.position.set(0.3, y + stepH / 2, z + stepD / 2);
            group.add(chip);
          }
        }
      }

      // Left railing (broken)
      const railH = stepsCount * stepH + 0.3;
      const leftRail = new THREE.Mesh(new THREE.BoxGeometry(0.06, railH * 0.5, 0.06), railMat);
      leftRail.position.set(-stepW / 2 - 0.04, railH * 0.25, 0);
      group.add(leftRail);
      const brokenRail = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.25, 0.05), railMat);
      brokenRail.position.set(-stepW / 2 - 0.04, railH * 0.5 + 0.05, -stepD);
      brokenRail.rotation.z = 0.4;
      brokenRail.rotation.x = -0.3;
      group.add(brokenRail);

      // Right railing (intact)
      const rightRail = new THREE.Mesh(new THREE.BoxGeometry(0.06, railH, 0.06), railMat);
      rightRail.position.set(stepW / 2 + 0.04, railH / 2, -stepsCount * stepD / 2);
      group.add(rightRail);
      const handrail = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.04, stepsCount * stepD), railMat);
      handrail.position.set(stepW / 2 + 0.04, railH + 0.02, -stepsCount * stepD / 2);
      handrail.rotation.x = Math.atan2(stepsCount * stepH, stepsCount * stepD);
      group.add(handrail);

      // Rubble at the base
      for(let j = 0; j < 5; j++){
        const rGeo = new THREE.BoxGeometry(0.08 + Math.random() * 0.1, 0.05 + Math.random() * 0.06, 0.08 + Math.random() * 0.1);
        const rubble = new THREE.Mesh(rGeo, rubbleMat);
        rubble.position.set((Math.random() - 0.5) * stepW, 0.03, 0.3 + Math.random() * 0.4);
        rubble.rotation.set(Math.random() * 0.5, Math.random() * 2, Math.random() * 0.5);
        group.add(rubble);
      }

      // Outline
      const outMat = new THREE.MeshBasicMaterial({color: 0x1a1208, side: THREE.BackSide});
      for(const child of [...group.children]){
        if(child.geometry){
          const outline = new THREE.Mesh(child.geometry.clone(), outMat);
          outline.position.copy(child.position);
          outline.rotation.copy(child.rotation);
          outline.scale.copy(child.scale).multiplyScalar(1.06);
          group.add(outline);
        }
      }

      group.position.set(f.c + fw / 2, 0, f.r + 0.5);
      group.userData = {furniture: f};
      scene.add(group);
      renderer.furnitureMeshes.push(group);
      continue;
    }

    // Grand door
    if(f.type === 'grand_door'){
      buildGrandDoor(scene, f.r, f.c, f.w);
      continue;
    }

    // Chandelier
    if(f.type === 'chandelier'){
      _buildChandelier(scene, renderer, f, fw, fh);
      continue;
    }

    // Default box furniture
    const mats = [sideMat, sideMat, topMat, frontMat, frontMat, sideMat];
    const mesh = new THREE.Mesh(geo, mats);
    mesh.position.set(f.c + fw * 0.5, H / 2, f.r + fh * 0.5);
    mesh.userData = {furniture: f};

    // Outline
    const outGeo = geo.clone();
    const outMat = new THREE.MeshBasicMaterial({color: 0x1a1208, side: THREE.BackSide});
    const outline = new THREE.Mesh(outGeo, outMat);
    outline.scale.set(1.04, 1.04, 1.04);
    mesh.add(outline);

    scene.add(mesh);
    renderer.furnitureMeshes.push(mesh);
  }
}

function _buildChandelier(scene, renderer, f, fw, fh){
  const isGrand = f.grand === true;
  const S = isGrand ? 4.0 : 1.0;
  const group = new THREE.Group();
  const chandelierMat = new THREE.MeshToonMaterial({color: 0xa08840});
  const chainMat = new THREE.MeshToonMaterial({color: 0x706030});
  const candleMat = new THREE.MeshToonMaterial({color: 0xeee8d0});
  const flameMat2 = new THREE.MeshToonMaterial({color: 0xff9920, emissive: 0xff7700, emissiveIntensity: 0.8});
  const flameCoreMat2 = new THREE.MeshToonMaterial({color: 0xffee88, emissive: 0xffdd44, emissiveIntensity: 1.0});

  const hangY = isGrand ? 2.8 : 2.0;

  // Chain
  const chain = new THREE.Mesh(new THREE.CylinderGeometry(0.02*S, 0.02*S, 0.8, 4), chainMat);
  chain.position.set(0, hangY + 0.4, 0);
  group.add(chain);

  // Central hub
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.08*S, 0.06*S, 0.1*S, 8), chandelierMat);
  hub.position.set(0, hangY, 0);
  group.add(hub);

  // Main ring
  const outerR = 0.8 * S;
  const ring = new THREE.Mesh(new THREE.TorusGeometry(outerR, 0.04*S, 6, 20), chandelierMat);
  ring.rotation.x = Math.PI / 2;
  ring.position.set(0, hangY - 0.05, 0);
  group.add(ring);

  // Inner ring
  const innerR = 0.45 * S;
  const ring2 = new THREE.Mesh(new THREE.TorusGeometry(innerR, 0.03*S, 6, 16), chandelierMat);
  ring2.rotation.x = Math.PI / 2;
  ring2.position.set(0, hangY, 0);
  group.add(ring2);

  // Arms + candles on outer ring
  const numCandles = isGrand ? 12 : 8;
  for(let i = 0; i < numCandles; i++){
    const angle = i * Math.PI * 2 / numCandles;
    const ax = Math.cos(angle) * outerR;
    const az = Math.sin(angle) * outerR;
    const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.02*S, 0.02*S, outerR*0.5, 4), chandelierMat);
    arm.rotation.z = Math.PI / 2;
    arm.rotation.y = -angle;
    arm.position.set(Math.cos(angle)*outerR*0.5, hangY, Math.sin(angle)*outerR*0.5);
    group.add(arm);
    const holder = new THREE.Mesh(new THREE.CylinderGeometry(0.04*S, 0.03*S, 0.04*S, 6), chandelierMat);
    holder.position.set(ax, hangY - 0.02, az);
    group.add(holder);
    const candle = new THREE.Mesh(new THREE.CylinderGeometry(0.025*S, 0.025*S, 0.12*S, 5), candleMat);
    candle.position.set(ax, hangY + 0.06*S, az);
    group.add(candle);
    const flame = new THREE.Mesh(new THREE.SphereGeometry(0.035*S, 4, 3), flameMat2);
    flame.scale.set(1, 1.6, 1);
    flame.position.set(ax, hangY + 0.15*S, az);
    group.add(flame);
    if(i % 2 === 0){
      const core = new THREE.Mesh(new THREE.SphereGeometry(0.02*S, 3, 2), flameCoreMat2);
      core.position.set(ax, hangY + 0.16*S, az);
      group.add(core);
    }
  }

  // Inner candles for grand chandelier
  if(isGrand){
    for(let i = 0; i < 6; i++){
      const angle = i * Math.PI / 3;
      const ax = Math.cos(angle) * innerR;
      const az = Math.sin(angle) * innerR;
      const holder = new THREE.Mesh(new THREE.CylinderGeometry(0.03*S, 0.02*S, 0.03*S, 6), chandelierMat);
      holder.position.set(ax, hangY - 0.02, az);
      group.add(holder);
      const candle = new THREE.Mesh(new THREE.CylinderGeometry(0.02*S, 0.02*S, 0.1*S, 5), candleMat);
      candle.position.set(ax, hangY + 0.05*S, az);
      group.add(candle);
      const flame = new THREE.Mesh(new THREE.SphereGeometry(0.03*S, 4, 3), flameMat2);
      flame.scale.set(1, 1.5, 1);
      flame.position.set(ax, hangY + 0.12*S, az);
      group.add(flame);
    }
  }

  const cx = isGrand ? 21.0 : f.c + 0.5;
  const cz = isGrand ? 21.5 : f.r + 0.5;
  group.position.set(cx, 0, cz);
  group.userData = {furniture: f};
  scene.add(group);
  renderer.furnitureMeshes.push(group);

  // Point light
  const lightInt = isGrand ? 6.0 : 3.5;
  const lightRange = isGrand ? 16 : 10;
  const cLight = new THREE.PointLight(0xffaa44, lightInt, lightRange);
  cLight.position.set(cx, hangY - 0.1, cz);
  cLight.baseIntensity = lightInt;
  scene.add(cLight);
  renderer.torchLights.push({light: cLight, flame: null, core: null, r: f.r, c: f.c});
}
