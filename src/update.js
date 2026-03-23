// ==================== UPDATE ====================
import {
  TILE_PX, PLAYER_SPEED,
  GND, WALL, WDEST, WATER, FURNITURE, DOOR,
  COLS, ROWS, MAP,
  state, spawnZ,
  furnitureList, setFurnitureList,
  surpriseSpawns, bossSpawn, bossTriggered, setBossTriggered,
  triggeredSurprises,
} from './state.js';
import { getMove } from './input.js';
import {
  playSFX, sfxShoot, sfxHit, sfxZombieDie, sfxPlayerHit,
  sfxVictory, sfxGameOver, sfxRoar, sfxSurprise,
} from './audio.js';

// Reference to renderer, set from main.js
let _renderer3d = null;
export function setRenderer(r){ _renderer3d = r; }

// ==================== COLLISION ====================
export function walkable(px, py, rad){
  const r = rad || 8/TILE_PX;
  for(const [ox,oy] of [[-r,-r],[r,-r],[-r,r],[r,r]]){
    const c = Math.floor(px+ox), row = Math.floor(py+oy);
    if(row<0||row>=ROWS||c<0||c>=COLS) return false;
    const t = MAP[row][c];
    if(t===WALL||t===WDEST||t===WATER||t===FURNITURE) return false;
  }
  return true;
}

// ==================== SHOOTING ====================
let lastShot = 0;

export function tryOpenDoor(){
  const p = state.player;
  if(!_renderer3d || !_renderer3d.doorMeshes) return false;
  for(const dg of _renderer3d.doorMeshes){
    const dd = dg.userData;
    if(dd.isOpen) continue;
    const dist = Math.hypot(p.x - (dd.c + 0.5), p.y - (dd.r + 0.5));
    if(dist < 1.8){
      dd.isOpen = true;
      MAP[dd.r][dd.c] = DOOR;
      const pivot = dd.doorPivot;
      if(pivot){
        pivot.rotation.y = dd.isHoriz ? -Math.PI / 2 : -Math.PI / 2;
      }
      // Hide halos and lights when door opens
      if(dd.doorLights) dd.doorLights.forEach(l => l.visible = false);
      dg.children.forEach(ch => { if(ch.material && ch.material.opacity < 1) ch.visible = false; });
      playSFX(80, 0.3, 'sawtooth');
      setTimeout(() => playSFX(60, 0.2, 'sine'), 100);
      return true;
    }
  }
  return false;
}

export function tryShoot(){
  const now = performance.now();
  if(now - lastShot < 250) return;
  if(tryOpenDoor()) { lastShot = now; return; }
  lastShot = now;
  const p = state.player;
  let closest = null, minD = Infinity;
  for(const z of state.zombies){
    if(z.hp<=0) continue;
    const d = Math.hypot(z.x - p.x, z.y - p.y);
    if(d < minD){ minD = d; closest = z; }
  }
  let dx = 0, dy = -1;
  if(closest){
    dx = closest.x - p.x; dy = closest.y - p.y;
    const l = Math.hypot(dx,dy); dx/=l; dy/=l;
  }
  state.projectiles.push({
    x: p.x, y: p.y,
    dx, dy,
    speed: 380/TILE_PX,
    life: 0.7, timer: 0,
    trail: [],
  });
  sfxShoot();
}

// ==================== PARTICLES ====================
export function spawnParts(x, y, colorHex, n){
  for(let i=0; i<n; i++){
    const a = Math.random()*6.28, spd = (60+Math.random()*80)/TILE_PX;
    state.particles.push({
      x, y,
      vx: Math.cos(a)*spd, vy: Math.sin(a)*spd,
      colorHex, radius: (2+Math.random()*3)/TILE_PX,
      timer: 0, life: 0.3+Math.random()*0.2, alpha: 1,
    });
  }
}

function spawnWallBreak(x, y){
  for(let i=0; i<8; i++){
    const a = Math.random()*6.28, spd = (80+Math.random()*100)/TILE_PX;
    state.particles.push({
      x: x+(Math.random()*10-5)/TILE_PX,
      y: y+(Math.random()*10-5)/TILE_PX,
      vx: Math.cos(a)*spd,
      vy: Math.sin(a)*spd - 40/TILE_PX,
      colorHex: 0xa88060,
      radius: (3+Math.random()*3)/TILE_PX,
      timer: 0, life: 0.5+Math.random()*0.3, alpha: 1,
    });
  }
}

// ==================== MAIN UPDATE ====================
let gameTimeState = 0;

export function update(dt){
  if(state.gameState!=='playing') return;
  const s = dt/1000;
  gameTimeState += s;
  state.gameTime = gameTimeState;

  const p = state.player;
  if(p.invincible>0) p.invincible -= dt;
  const {dx, dy} = getMove();
  p.moving = dx!==0 || dy!==0;

  if(p.moving){
    p.facingDx = dx; p.facingDy = dy;
    p.angle = Math.atan2(dx, dy);
    if(dy > 0.3) p.facingDown = true;
    else if(dy < -0.3) p.facingDown = false;
    const nx = p.x + dx*PLAYER_SPEED*s;
    const ny = p.y + dy*PLAYER_SPEED*s;
    if(walkable(nx, ny)){ p.x=nx; p.y=ny; }
    else if(walkable(nx, p.y)) p.x=nx;
    else if(walkable(p.x, ny)) p.y=ny;
  }
  p.bobTimer += s*6;
  p.bobY = p.moving ? Math.sin(p.bobTimer)*3/TILE_PX : Math.sin(p.bobTimer*2)*1.5/TILE_PX;
  p.animTimer += dt;
  if(p.animTimer > 150){ p.animTimer=0; p.frame=(p.frame+1)%(p.moving?6:4); }

  // ---- Surprise trigger zones ----
  for(const sp of surpriseSpawns){
    if(sp.triggered) continue;
    const dx2 = p.x - (sp.triggerCol+0.5), dy2 = p.y - (sp.triggerRow+0.5);
    if(Math.hypot(dx2,dy2) < sp.radius){
      sp.triggered = true;
      triggeredSurprises.add(sp);
      const sz = spawnZ(sp.col, sp.row, 1, 42, '#5a8f3c', 'Zombie');
      sfxSurprise();
      spawnParts(sp.col+0.5, sp.row+0.5, 0x88ff44, 12);
      if(_renderer3d && _renderer3d._addZombieMesh) _renderer3d._addZombieMesh(sz);
    }
  }

  // ---- Boss trigger: wardrobe destroyed ----
  if(bossSpawn && !bossTriggered){
    const wr = bossSpawn.wardrobeRow, wc = bossSpawn.wardrobeCol;
    if(MAP[wr][wc] !== FURNITURE && MAP[wr][wc] !== WDEST){
      setBossTriggered(true);
      const bz = spawnZ(bossSpawn.col, bossSpawn.row, 10, 30, '#4a1a4a', 'BOSS', true);
      sfxRoar();
      spawnParts(bossSpawn.col+0.5, bossSpawn.row+0.5, 0xff4444, 16);
      if(_renderer3d && _renderer3d._addZombieMesh) _renderer3d._addZombieMesh(bz);
    }
  }

  for(const z of state.zombies){
    if(z.hp<=0) continue;
    const ddx = p.x-z.x, ddy = p.y-z.y, dist = Math.hypot(ddx,ddy);
    z.moving = dist > 15/TILE_PX;
    if(z.moving){
      const mx = ddx/dist*z.speed*s, my = ddy/dist*z.speed*s;
      z.facingDx = ddx/dist; z.facingDy = ddy/dist;
      z.angle = Math.atan2(ddx/dist, ddy/dist);
      const nx = z.x+mx, ny = z.y+my;
      if(walkable(nx,ny)){ z.x=nx; z.y=ny; }
      else if(walkable(nx,z.y)) z.x=nx;
      else if(walkable(z.x,ny)) z.y=ny;
    }
    z.bobTimer += s*5;
    z.bobY = Math.sin(z.bobTimer)*2/TILE_PX;
    z.animTimer = (z.animTimer||0)+dt;
    if(z.animTimer>180){ z.animTimer=0; z.frame=(z.frame+1)%(z.moving?6:4); }
    const hitDist = z.isBoss ? 22/TILE_PX : 18/TILE_PX;
    if(dist < hitDist && !z.hitCooldown && p.invincible<=0){
      p.hp = Math.max(0, p.hp-1);
      z.hitCooldown = 60;
      p.invincible = 1000;
      state.dmgNumbers.push({x:p.x, y:p.y, text:'-1', timer:0, color:'#ff4444'});
      sfxPlayerHit();
      if(p.hp<=0){ state.gameState='gameover'; sfxGameOver(); }
    }
    if(z.hitCooldown) z.hitCooldown--;
  }

  for(let i=state.projectiles.length-1; i>=0; i--){
    const proj = state.projectiles[i];
    proj.x += proj.dx*proj.speed*s;
    proj.y += proj.dy*proj.speed*s;
    proj.timer += s;
    proj.trail.push({x:proj.x, y:proj.y, a:1});
    if(proj.trail.length>8) proj.trail.shift();
    proj.trail.forEach(t=>t.a*=0.82);
    const tc = Math.floor(proj.x), tr = Math.floor(proj.y);
    if(tc<0||tc>=COLS||tr<0||tr>=ROWS||MAP[tr][tc]===WALL){
      state.projectiles.splice(i,1);
      spawnParts(proj.x, proj.y, 0x44ddff, 4);
      continue;
    }
    if(MAP[tr][tc]===WDEST){
      MAP[tr][tc]=GND;
      state.mapVersion++;
      state.projectiles.splice(i,1);
      spawnWallBreak(proj.x, proj.y);
      continue;
    }
    if(MAP[tr][tc]===FURNITURE){
      let isWardrobe = false;
      if(bossSpawn && !bossTriggered){
        const wr = bossSpawn.wardrobeRow, wc = bossSpawn.wardrobeCol;
        if(tr===wr && tc===wc) isWardrobe = true;
      }
      if(isWardrobe){
        MAP[tr][tc]=GND;
        state.mapVersion++;
        state.projectiles.splice(i,1);
        spawnWallBreak(proj.x, proj.y);
        // Remove from furnitureList
        setFurnitureList(furnitureList.filter(f => !(f.r===tr && f.c===tc)));
        continue;
      }
      state.projectiles.splice(i,1);
      spawnParts(proj.x, proj.y, 0x44ddff, 4);
      continue;
    }
    let hit=false;
    for(const z of state.zombies){
      if(z.hp<=0) continue;
      const hitR = z.isBoss ? 22/TILE_PX : 16/TILE_PX;
      if(Math.hypot(z.x-proj.x, z.y-proj.y) < hitR){
        z.hp--; sfxHit();
        state.dmgNumbers.push({x:z.x, y:z.y, text:''+Math.ceil(100/z.maxHp), timer:0, color:'#ffffff'});
        spawnParts(proj.x, proj.y, 0x44ddff, 3);
        if(z.hp<=0){
          spawnParts(z.x, z.y, 0x55aa33, 8); sfxZombieDie();
          const pts=z.isBoss?50:(z.maxHp===1?10:(z.maxHp===2?20:30));
          p.points+=pts;
          state.dmgNumbers.push({x:z.x, y:z.y-0.5, text:'+'+pts, timer:0, color:'#ffdd44'});
          if(state.zombies.every(zz=>zz.hp<=0)){ state.gameState='victory'; sfxVictory(); }
        }
        hit=true; break;
      }
    }
    if(hit){ state.projectiles.splice(i,1); continue; }
    if(proj.timer > proj.life) state.projectiles.splice(i,1);
  }

  for(let i=state.particles.length-1; i>=0; i--){
    const pt = state.particles[i];
    pt.x += pt.vx*s; pt.y += pt.vy*s;
    pt.timer += s;
    pt.alpha = 1 - pt.timer/pt.life;
    if(pt.timer >= pt.life) state.particles.splice(i,1);
  }

  for(let i=state.dmgNumbers.length-1; i>=0; i--){
    const d = state.dmgNumbers[i];
    d.timer += s;
    d.y -= 55/TILE_PX * s;
    if(d.timer > 0.8) state.dmgNumbers.splice(i,1);
  }

  // Update UI (inline from original — also handled by hud.js updateHUD)
  const alive = state.zombies.filter(z=>z.hp>0).length;
  document.getElementById('zombie-count').textContent = `Zombies: ${alive}`;
  let hearts = '';
  for(let i=0; i<3; i++){
    hearts += p.hp>=(i+1)*2 ? '❤️' : (p.hp>=i*2+1 ? '💔' : '🖤');
  }
  document.getElementById('hearts').textContent = hearts;
}
