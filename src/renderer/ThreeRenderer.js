// ==================== THREE.JS RENDERER ====================
import * as THREE from 'three';
import {
  DOOR, WDEST, FURNITURE, MAP,
  COLS, ROWS, state,
} from '../state.js';
import { buildGround } from './ground.js';
import { buildWalls } from './walls.js';
import { buildDoor3D } from './doors.js';
import { buildFurniture } from './furniture.js';
import { buildBushes } from './trees.js';
import { buildWater } from './water.js';
import { buildPlayer, buildZombie, makeShadow, makeHalo, facingToAngle } from './characters.js';
import { buildBats, respawnBat, getProjMesh, getTrailMesh, getParticleMesh, makeDmgSprite } from './effects.js';
import { buildTorchLights } from './torches.js';

export class ThreeRenderer {
  constructor(){
    this.canvas = document.getElementById('three-canvas');
    this.renderer = new THREE.WebGLRenderer({canvas: this.canvas, antialias: true});
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.shadowMap.enabled = false;

    this.scene = new THREE.Scene();
    this.scene.background = new THREE.Color(0x050810);
    this.scene.fog = new THREE.Fog(0x1a3a10, 22, 50);

    this.camera = new THREE.PerspectiveCamera(50, window.innerWidth/window.innerHeight, 0.1, 100);
    this.camTarget = new THREE.Vector3();
    this.camera.position.set(20, 12, 14+10);
    this.camera.lookAt(20, 0, 14);

    // Lighting
    const amb = new THREE.AmbientLight(0x405868, 0.7);
    this.scene.add(amb);
    const dir = new THREE.DirectionalLight(0x8898b0, 0.6);
    dir.position.set(-5, 10, 5);
    this.scene.add(dir);

    // Maps
    this.lastMapVersion = -1;
    this.wallMeshIndestructible = null;
    this.wallMeshDestructible = null;
    this.wallDataIndestructible = [];
    this.wallDataDestructible = [];

    // Character meshes
    this.playerMesh = null;
    this.playerShadow = null;
    this.playerHalo = null;
    this.zombieMeshes = [];

    // Projectile pool
    this.projPool = [];
    this.activeProjMeshes = new Map();

    // Particle pool
    this.particlePool = [];
    this.activeParticles = [];

    // Damage number sprites
    this.dmgSprites = [];

    // Torch point lights
    this.torchLights = [];

    // Water mesh
    this.waterMesh = null;
    this.waterGeo = null;
    this._waterPlanes = null;

    // Bush meshes
    this.bushMeshes = [];

    // Furniture meshes
    this.furnitureMeshes = [];

    // Door meshes
    this.doorMeshes = [];

    // Dest wall meshes
    this._destWallMeshes = [];

    // Bats
    this.bats = [];

    this._buildScene();

    window.addEventListener('resize', ()=>{
      this.camera.aspect = window.innerWidth/window.innerHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(window.innerWidth, window.innerHeight);
    });
  }

  _buildScene(){
    const groundResult = buildGround(this.scene);
    this.groundTex = groundResult.groundTex;
    this.groundCanvas = groundResult.groundCanvas;
    this.groundCtxRef = groundResult.groundCtxRef;

    buildWalls(this.scene, this);
    // Build doors (from DOOR tiles found during wall scan, but wall scan already
    // populated wallDataIndestructible, so we re-scan for doors)
    this._buildDoors();
    buildBushes(this.scene, this);
    buildWater(this.scene, this);
    buildFurniture(this.scene, this);
    buildBats(this.scene, this);

    // Night fog
    this.scene.fog = new THREE.FogExp2(0x0c1220, 0.03);
    buildTorchLights(this.scene, this);

    this.playerMesh = buildPlayer();
    this.scene.add(this.playerMesh.group);

    // HTML health bars
    this._hbContainer = document.getElementById('healthbars-container');
    this._hbElements = [];
    this._playerHB = this._createHtmlHB('Angel', '#44dd44');
    this._hbContainer.appendChild(this._playerHB.el);
    this.playerShadow = makeShadow();
    this.scene.add(this.playerShadow);
    this.playerHalo = makeHalo(0x44cc44);
    this.scene.add(this.playerHalo);

    for(const z of state.zombies){
      this._addZombieMeshInternal(z);
    }
  }

  _buildDoors(){
    // Scan map for DOOR tiles and build 3D doors
    // (buildWalls already handled WALL and WDEST, doors were skipped there)
    for(let r=0; r<ROWS; r++){
      for(let c=0; c<COLS; c++){
        if(MAP[r][c] === DOOR){
          if(r === ROWS - 4) continue; // entrance row
          buildDoor3D(this.scene, this, r, c, false);
        }
      }
    }
  }

  _addZombieMeshInternal(z){
    const zm = buildZombie(z);
    this.scene.add(zm.group);
    const sh = makeShadow();
    this.scene.add(sh);
    const hl = makeHalo(0xcc3333);
    this.scene.add(hl);
    const hbEl = this._createHtmlHB(z.name || 'Zombie', '#dd4444');
    this._hbContainer.appendChild(hbEl.el);
    this.zombieMeshes.push({group: zm.group, parts: zm, shadow: sh, halo: hl, zRef: z, hbEl});
  }

  _addZombieMesh(z){
    this._addZombieMeshInternal(z);
  }

  // ---- Main render method ----
  _createHtmlHB(name, color){
    const el = document.createElement('div');
    el.className = 'hpbar';
    el.innerHTML = `<div class="hpbar-name">${name}</div><div class="hpbar-bg"><div class="hpbar-fill" style="width:100%;background:${color}"></div></div>`;
    const fill = el.querySelector('.hpbar-fill');
    return {el, fill, color};
  }

  _projectToScreen(worldPos){
    const v = worldPos.clone();
    v.project(this.camera);
    return {
      x: (v.x * 0.5 + 0.5) * window.innerWidth,
      y: (-v.y * 0.5 + 0.5) * window.innerHeight,
      visible: v.z < 1
    };
  }

  render(dt){
    const s = dt/1000;
    const t = state.gameTime;
    const p = state.player;

    // Rebuild walls if map changed
    if(state.mapVersion !== this.lastMapVersion){
      if(this._destWallMeshes){
        this._destWallMeshes = this._destWallMeshes.filter(m => {
          if(MAP[m.userData.r][m.userData.c] !== WDEST){
            this.scene.remove(m);
            m.geometry.dispose();
            return false;
          }
          return true;
        });
      }
      this.furnitureMeshes = this.furnitureMeshes.filter(mesh => {
        const f = mesh.userData?.furniture;
        if(!f) return true;
        if(f.type === 'chandelier') return true;
        let destroyed = false;
        for(let dr=0; dr<(f.h||1); dr++){
          for(let dc=0; dc<(f.w||1); dc++){
            if(MAP[f.r+dr]?.[f.c+dc] !== FURNITURE) destroyed = true;
          }
        }
        if(destroyed){
          this.scene.remove(mesh);
          if(mesh.material) mesh.material.dispose();
          if(mesh.geometry) mesh.geometry.dispose();
          return false;
        }
        return true;
      });
      this.lastMapVersion = state.mapVersion;
    }

    // Camera follow player with lerp
    const targetX = p.x;
    const targetZ = p.y;
    this.camTarget.x += (targetX - this.camTarget.x)*0.08;
    this.camTarget.z += (targetZ - this.camTarget.z)*0.08;
    this.camera.position.x += (this.camTarget.x - this.camera.position.x + 0)*0.08;
    this.camera.position.z += (this.camTarget.z + 10 - this.camera.position.z)*0.08;
    this.camera.position.y = 12;
    this.camera.lookAt(this.camTarget.x, 0, this.camTarget.z);

    // Water animation
    if(this._waterPlanes){
      for(const wp of this._waterPlanes){
        const pos = wp.posAttr;
        for(let i=0; i<pos.count; i++){
          const x = pos.getX(i) + wp.c + 0.5;
          const z = pos.getZ(i) + wp.r + 0.5;
          pos.setY(i, Math.sin(t*1.8 + x*1.2 + z*0.8)*0.03 + Math.sin(t*2.5 + z*1.5)*0.015);
        }
        pos.needsUpdate = true;
        const pulse = 0.75 + Math.sin(t*0.8 + wp.r*0.3 + wp.c*0.2)*0.08;
        wp.mesh.material.opacity = pulse;
      }
    }

    // Bats animation
    for(const bat of this.bats){
      bat.timer += dt/1000;
      const speed = 3 + bat.speed;
      bat.x += bat.dx * speed * dt/1000;
      bat.z += bat.dz * speed * dt/1000;
      bat.y = 2.5 + Math.sin(bat.timer * 4) * 0.5;
      bat.wingAngle = Math.sin(bat.timer * 12) * 0.8;
      bat.wingL.rotation.z = bat.wingAngle;
      bat.wingR.rotation.z = -bat.wingAngle;
      bat.group.position.set(bat.x, bat.y, bat.z);
      bat.group.rotation.y = Math.atan2(bat.dx, bat.dz);
      if(bat.x < -5 || bat.x > COLS+5 || bat.z < -5 || bat.z > ROWS+5){
        respawnBat(bat);
      }
    }

    // Door halo pulse (no PointLights — just visual halos)
    for(const dg of this.doorMeshes){
      const dd = dg.userData;
      if(dd.isOpen) continue;
      const pulse = 0.2 + Math.sin(t * 2.5 + dd.r * 1.3 + dd.c * 0.7) * 0.15;
      dg.children.forEach(ch => {
        if(ch.material && ch.material.transparent){
          ch.material.opacity = pulse;
        }
      });
    }

    // Torch flicker
    for(const torch of this.torchLights){
      const flicker = 0.8 + Math.sin(t*8 + torch.r*3 + torch.c*7)*0.12 + Math.sin(t*13 + torch.c*5)*0.08;
      torch.light.intensity = torch.light.baseIntensity * flicker;
      if(torch.flame){
        torch.flame.scale.y = 1.3 + Math.sin(t*10 + torch.r*4)*0.4;
        torch.flame.scale.x = 1.0 + Math.sin(t*7 + torch.c*3)*0.15;
        torch.flame.position.y += Math.sin(t*12 + torch.r)*0.002;
      }
      if(torch.core){
        torch.core.scale.set(
          0.8 + Math.sin(t*15 + torch.c)*0.3,
          0.8 + Math.sin(t*11 + torch.r)*0.3,
          0.8 + Math.sin(t*9)*0.2
        );
      }
    }

    // Player
    const pm = this.playerMesh;
    const bobY = p.moving ? 0.06*Math.abs(Math.sin(p.bobTimer)) : 0.03*Math.sin(p.bobTimer*2);
    pm.group.position.set(p.x, bobY, p.y);
    pm.group.visible = !(p.invincible > 0 && Math.floor(t*12) % 2 === 0);

    const pAngle = facingToAngle(p.facingDx, p.facingDy);
    const pAnim = p.moving ? 'walk' : 'idle';
    const sheetKey = `${pAnim}_${pAngle}`;
    const numFrames = pm.frameConfig[pAnim];

    if(pm.currentSheet !== sheetKey){
      const newTex = pm.sheets[sheetKey];
      newTex.repeat.set(1/numFrames, 1);
      newTex.offset.set(0, 0);
      pm.spriteMat.map = newTex;
      pm.spriteMat.needsUpdate = true;
      pm.currentSheet = sheetKey;
    }

    const frame = p.frame % numFrames;
    pm.spriteMat.map.offset.set(frame / numFrames, 0);

    // HTML health bar — project to screen
    const pRatio = p.hp/p.maxHp;
    this._playerHB.fill.style.width = (pRatio * 100) + '%';
    const pScreen = this._projectToScreen(new THREE.Vector3(p.x, 1.6, p.y));
    this._playerHB.el.style.left = pScreen.x + 'px';
    this._playerHB.el.style.top = pScreen.y + 'px';
    this._playerHB.el.style.display = pScreen.visible ? 'block' : 'none';

    // Player shadow and halo
    this.playerShadow.position.set(p.x, 0.01, p.y);
    this.playerHalo.position.set(p.x, 0.02, p.y);
    this.playerHalo.material.opacity = 0.4 + 0.2*Math.sin(t*2);

    // Zombies
    for(let i=0; i<this.zombieMeshes.length; i++){
      const zm = this.zombieMeshes[i];
      const z = zm.zRef;
      if(z.hp<=0){
        zm.group.visible = false;
        zm.shadow.visible = false;
        zm.halo.visible = false;
        if(zm.hbEl) zm.hbEl.el.style.display = 'none';
        continue;
      }
      zm.group.visible = true;
      zm.shadow.visible = true;
      zm.halo.visible = true;
      const bobOff = z.moving ? 0.04*Math.abs(Math.sin(z.bobTimer)) : 0.02*Math.sin(z.bobTimer);
      zm.group.position.set(z.x, bobOff, z.y);
      zm.shadow.position.set(z.x, 0.01, z.y);
      zm.halo.position.set(z.x, 0.02, z.y);
      zm.halo.material.opacity = 0.3 + 0.15*Math.sin(t*2 + i);

      // Sprite sheet animation (8 directions)
      const zp = zm.parts;
      if(zp.sheets){
        const zAngle = facingToAngle(z.facingDx, z.facingDy);
        const zAnim = z.moving ? 'walk' : 'idle';
        const zSheetKey = `${zAnim}_${zAngle}`;
        const zNumFrames = zp.frameConfig[zAnim];

        if(zp.currentSheet !== zSheetKey){
          const newTex = zp.sheets[zSheetKey];
          newTex.repeat.set(1/zNumFrames, 1);
          newTex.offset.set(0, 0);
          zp.spriteMat.map = newTex;
          zp.spriteMat.needsUpdate = true;
          zp.currentSheet = zSheetKey;
        }
        const zFrame = (z.frame || 0) % zNumFrames;
        zp.spriteMat.map.offset.set(zFrame / zNumFrames, 0);
      }

      // HTML health bar — project to screen
      const zRatio = z.hp/z.maxHp;
      if(zm.hbEl){
        zm.hbEl.fill.style.width = (zRatio * 100) + '%';
        const hbY = z.isBoss ? 1.8 : 1.4;
        const zScreen = this._projectToScreen(new THREE.Vector3(z.x, hbY, z.y));
        zm.hbEl.el.style.left = zScreen.x + 'px';
        zm.hbEl.el.style.top = zScreen.y + 'px';
        zm.hbEl.el.style.display = (z.hp > 0 && zScreen.visible) ? 'block' : 'none';
      }
    }

    // Projectiles
    const activeProjSet = new Set(state.projectiles);
    for(const [key, mesh] of this.activeProjMeshes){
      if(!activeProjSet.has(key)){
        this.scene.remove(mesh.main);
        this.projPool.push(mesh.main);
        for(const tr of mesh.trails){ this.scene.remove(tr); }
        this.activeProjMeshes.delete(key);
      }
    }
    for(const proj of state.projectiles){
      if(!this.activeProjMeshes.has(proj)){
        const main = getProjMesh(this.projPool);
        this.scene.add(main);
        const trails = [];
        for(let ti=0; ti<8; ti++){
          const tr = getTrailMesh();
          this.scene.add(tr);
          trails.push(tr);
        }
        this.activeProjMeshes.set(proj, {main, trails});
      }
      const {main, trails} = this.activeProjMeshes.get(proj);
      main.position.set(proj.x, 0.4, proj.y);
      for(let ti=0; ti<trails.length; ti++){
        const tr = trails[ti];
        if(ti < proj.trail.length){
          const pt = proj.trail[proj.trail.length-1-ti];
          tr.position.set(pt.x, 0.4, pt.y);
          tr.material.opacity = pt.a*0.4;
          tr.scale.setScalar(1 - ti*0.1);
          tr.visible = true;
        } else {
          tr.visible = false;
        }
      }
    }

    // Particles
    const activeParticleSet = new Set(state.particles);
    for(let i=this.activeParticles.length-1; i>=0; i--){
      const ap = this.activeParticles[i];
      if(!activeParticleSet.has(ap.ref)){
        this.scene.remove(ap.mesh);
        ap.mesh.visible = false;
        this.particlePool.push(ap.mesh);
        this.activeParticles.splice(i,1);
      }
    }
    const particleMeshRefs = new Set(this.activeParticles.map(ap=>ap.ref));
    for(const pt of state.particles){
      if(!particleMeshRefs.has(pt)){
        const mesh = getParticleMesh(this.particlePool, pt.colorHex);
        this.scene.add(mesh);
        this.activeParticles.push({ref: pt, mesh});
      }
    }
    for(const ap of this.activeParticles){
      const pt = ap.ref;
      ap.mesh.position.set(pt.x, 0.3 + (1-pt.alpha)*0.5, pt.y);
      ap.mesh.scale.setScalar(pt.radius * 10 * pt.alpha);
      ap.mesh.material.opacity = Math.max(0, pt.alpha);
    }

    // Damage numbers
    const activeDmgSet = new Set(state.dmgNumbers);
    for(let i=this.dmgSprites.length-1; i>=0; i--){
      const ds = this.dmgSprites[i];
      if(!activeDmgSet.has(ds.ref)){
        this.scene.remove(ds.sprite);
        ds.sprite.material.map.dispose();
        ds.sprite.material.dispose();
        this.dmgSprites.splice(i,1);
      }
    }
    const dmgRefs = new Set(this.dmgSprites.map(ds=>ds.ref));
    for(const d of state.dmgNumbers){
      if(!dmgRefs.has(d)){
        const sprite = makeDmgSprite(d.text, d.color);
        this.scene.add(sprite);
        this.dmgSprites.push({ref: d, sprite});
      }
    }
    for(const ds of this.dmgSprites){
      const d = ds.ref;
      ds.sprite.position.set(d.x, 1.5 + d.timer*0.8, d.y);
      ds.sprite.material.opacity = Math.max(0, 1-d.timer/0.8);
    }

    this.renderer.render(this.scene, this.camera);
  }
}
