// ==================== HUD UPDATE ====================
import { state } from './state.js';

const zombieCountEl = document.getElementById('zombie-count');
const pointsEl = document.getElementById('points-display');
const heartsEl = document.getElementById('hearts');
const overlayEl = document.getElementById('overlay');
const overlayTitle = document.getElementById('overlay-title');
const overlayPoints = document.getElementById('overlay-points');
const btnRestart = document.getElementById('btn-restart');
const btnReplay = document.getElementById('btn-replay');
const btnMenu = document.getElementById('btn-menu');

export function updateHUD(){
  const p = state.player;
  const alive = state.zombies.filter(z=>z.hp>0).length;
  zombieCountEl.textContent = `Zombies: ${alive}`;
  pointsEl.textContent = `${p.points} pts`;

  // Hearts
  let h = '';
  for(let i=0;i<3;i++) h += p.hp>=(i+1)*2 ? '❤️' : (p.hp>=i*2+1 ? '💔' : '🖤');
  heartsEl.textContent = h;

  // Overlay
  if(state.gameState==='victory'){
    overlayEl.style.display = 'flex';
    overlayTitle.textContent = 'VICTOIRE !';
    overlayTitle.style.color = '#44ff44';
    overlayPoints.textContent = `${p.points} points`;
    btnRestart.style.display = 'block';
    btnReplay.style.display = 'none';
    btnMenu.style.display = 'none';
  } else if(state.gameState==='gameover'){
    overlayEl.style.display = 'flex';
    overlayTitle.textContent = 'GAME OVER';
    overlayTitle.style.color = '#ff4444';
    overlayPoints.textContent = `${p.points} points`;
    btnRestart.style.display = 'none';
    btnReplay.style.display = 'block';
    btnMenu.style.display = 'block';
  } else {
    overlayEl.style.display = 'none';
  }
}

export function setupHUDListeners(){
  // Restart / Replay key handling
  window.addEventListener('keydown', e => {
    if(e.key.toLowerCase()==='r'){
      if(state.gameState==='victory') location.reload();
      else if(state.gameState==='gameover'){
        state.player.hp = state.player.maxHp;
        state.player.points = Math.max(0, state.player.points-100);
        state.player.invincible = 2000;
        state.gameState = 'playing';
      }
    }
    if(e.key.toLowerCase()==='m' && state.gameState==='gameover') location.reload();
  });
  btnRestart.addEventListener('click', ()=> location.reload());
  btnReplay.addEventListener('click', ()=>{
    state.player.hp = state.player.maxHp;
    state.player.points = Math.max(0, state.player.points-100);
    state.player.invincible = 2000;
    state.gameState = 'playing';
  });
  btnMenu.addEventListener('click', ()=> location.reload());
}
