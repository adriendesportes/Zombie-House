// ==================== EFFECTS (projectiles, particles, damage sprites, bats) ====================
import * as THREE from 'three';
import { COLS, ROWS } from '../state.js';

// ---- Projectile pool ----
export function getProjMesh(projPool){
  if(projPool.length > 0) return projPool.pop();
  const geo = new THREE.SphereGeometry(0.1, 6, 4);
  const mat = new THREE.MeshToonMaterial({color: 0x44ddff, emissive: 0x44ddff, emissiveIntensity: 0.8});
  return new THREE.Mesh(geo, mat);
}

export function getTrailMesh(){
  const geo = new THREE.SphereGeometry(0.065, 5, 3);
  const mat = new THREE.MeshBasicMaterial({color: 0x44ddff, transparent: true, opacity: 0.4, depthWrite: false});
  return new THREE.Mesh(geo, mat);
}

// ---- Particle pool ----
export function getParticleMesh(particlePool, colorHex){
  if(particlePool.length > 0){
    const m = particlePool.pop();
    m.material.color.setHex(colorHex);
    m.visible = true;
    return m;
  }
  const geo = new THREE.SphereGeometry(0.08, 4, 3);
  const mat = new THREE.MeshBasicMaterial({color: colorHex, transparent: true, opacity: 1, depthWrite: false});
  return new THREE.Mesh(geo, mat);
}

// ---- Damage number sprite ----
export function makeDmgSprite(text, color){
  const c = document.createElement('canvas');
  c.width = 128; c.height = 64;
  const ctx = c.getContext('2d');
  ctx.font = 'bold 38px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.strokeStyle = '#000';
  ctx.lineWidth = 5;
  ctx.strokeText(text, 64, 32);
  ctx.fillStyle = color;
  ctx.fillText(text, 64, 32);
  const tex = new THREE.CanvasTexture(c);
  const mat = new THREE.SpriteMaterial({map: tex, transparent: true, depthWrite: false});
  const sprite = new THREE.Sprite(mat);
  sprite.scale.set(0.8, 0.4, 1);
  return sprite;
}

// ---- Bats ----
export function buildBats(scene, renderer){
  renderer.bats = [];
  const batMat = new THREE.MeshBasicMaterial({color: 0x1a1018, side: THREE.DoubleSide});
  for(let i = 0; i < 5; i++){
    const group = new THREE.Group();
    const bodyGeo = new THREE.SphereGeometry(0.08, 4, 3);
    const body = new THREE.Mesh(bodyGeo, batMat);
    group.add(body);
    const wingGeo = new THREE.PlaneGeometry(0.25, 0.12);
    const wingL = new THREE.Mesh(wingGeo, batMat);
    wingL.position.set(-0.15, 0, 0);
    wingL.rotation.x = -Math.PI/2;
    group.add(wingL);
    const wingR = new THREE.Mesh(wingGeo, batMat);
    wingR.position.set(0.15, 0, 0);
    wingR.rotation.x = -Math.PI/2;
    group.add(wingR);

    scene.add(group);
    const bat = {
      group, wingL, wingR,
      x: 0, y: 3, z: 0,
      dx: 0, dz: 0, speed: Math.random() * 2,
      timer: Math.random() * 10, wingAngle: 0,
    };
    respawnBat(bat);
    renderer.bats.push(bat);
  }
}

export function respawnBat(bat){
  const side = Math.floor(Math.random() * 4);
  if(side === 0){ bat.x = -3; bat.z = Math.random() * ROWS; bat.dx = 1; bat.dz = (Math.random()-0.5)*0.5; }
  else if(side === 1){ bat.x = COLS+3; bat.z = Math.random() * ROWS; bat.dx = -1; bat.dz = (Math.random()-0.5)*0.5; }
  else if(side === 2){ bat.z = -3; bat.x = Math.random() * COLS; bat.dz = 1; bat.dx = (Math.random()-0.5)*0.5; }
  else { bat.z = ROWS+3; bat.x = Math.random() * COLS; bat.dz = -1; bat.dx = (Math.random()-0.5)*0.5; }
  const len = Math.hypot(bat.dx, bat.dz);
  bat.dx /= len; bat.dz /= len;
  bat.y = 2.5 + Math.random();
}
