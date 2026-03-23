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
    chandelier: 0.05, grand_door: 0.7, stairs_broken: 0.5, stairs_broken_left: 0.5, piano: 0.45,
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
    // Piano — 3D inclined plane with LLM texture (same method as stairs)
    if(f.type === 'piano'){
      const pianoTex = loader.load('public/assets/tilesets/furniture-piano.png');
      pianoTex.magFilter = THREE.NearestFilter;
      pianoTex.minFilter = THREE.LinearFilter;
      pianoTex.colorSpace = THREE.SRGBColorSpace;

      const group = new THREE.Group();
      const pianoW = fw * 1.5;
      const pianoD = 2.0;
      const pianoH = 1.0;

      const rampLen = Math.sqrt(pianoD * pianoD + pianoH * pianoH);
      const rampGeo = new THREE.PlaneGeometry(pianoW, rampLen);
      const rampMat = new THREE.MeshToonMaterial({
        map: pianoTex, transparent: true, alphaTest: 0.1, side: THREE.DoubleSide
      });
      const ramp = new THREE.Mesh(rampGeo, rampMat);
      const rampAngle = Math.atan2(pianoH, pianoD);
      ramp.rotation.x = -Math.PI / 2 + rampAngle;
      ramp.position.set(0, pianoH * 0.5, -pianoD * 0.4);
      group.add(ramp);

      group.position.set(f.c + fw / 2, 0, f.r + 0.5);
      group.userData = {furniture: f};
      scene.add(group);
      renderer.furnitureMeshes.push(group);
      continue;
    }

    if(f.type === 'stairs_broken' || f.type === 'stairs_broken_left'){
      // 3D inclined plane with LLM texture
      const texFile = f.type === 'stairs_broken_left'
        ? 'public/assets/tilesets/furniture-stairs_broken_left.png'
        : 'public/assets/tilesets/furniture-stairs_broken.png';
      const stairsTex = loader.load(texFile);
      stairsTex.magFilter = THREE.NearestFilter;
      stairsTex.minFilter = THREE.LinearFilter;
      stairsTex.colorSpace = THREE.SRGBColorSpace;

      const group = new THREE.Group();
      const stairsW = fw * 1.5;
      const stairsD = 2.2;  // longer ramp to reach above the wall
      const stairsH = 1.4;  // taller than wall (0.8) — goes to upper floor

      // Inclined ramp with texture
      const rampLen = Math.sqrt(stairsD * stairsD + stairsH * stairsH);
      const rampGeo = new THREE.PlaneGeometry(stairsW, rampLen);
      const rampMat = new THREE.MeshToonMaterial({
        map: stairsTex, transparent: true, alphaTest: 0.1, side: THREE.DoubleSide
      });
      const ramp = new THREE.Mesh(rampGeo, rampMat);
      const rampAngle = Math.atan2(stairsH, stairsD);
      ramp.rotation.x = -Math.PI / 2 + rampAngle;
      ramp.position.set(0, stairsH * 0.5, -stairsD * 0.4);
      group.add(ramp);

      group.position.set(f.c + fw / 2, 0, f.r + 0.5);
      group.userData = {furniture: f};
      scene.add(group);
      renderer.furnitureMeshes.push(group);
      continue;
    }

    // Grand door
    if(f.type === 'grand_door'){
      buildGrandDoor(scene, renderer, f.r, f.c, f.w);
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
