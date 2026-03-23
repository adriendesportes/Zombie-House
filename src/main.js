// ==================== MAIN — Entry point ====================
import { state } from './state.js';
import { setupInput } from './input.js';
import { update, tryShoot, setRenderer } from './update.js';
import { ThreeRenderer } from './renderer/ThreeRenderer.js';
import { updateHUD, setupHUDListeners } from './hud.js';
import { loadMapJSON } from './map-loader.js';
import { setupAudioListeners } from './audio.js';

// ==================== GAME LOOP ====================
let renderer3d = null;
let lastTime = 0;

function gameLoop(time = 0){
  const dt = Math.min(time - lastTime, 50);
  lastTime = time;
  update(dt);
  if(renderer3d) renderer3d.render(dt);
  updateHUD();
  requestAnimationFrame(gameLoop);
}

// ==================== START ====================
async function startGame(){
  // Setup audio auto-unlock listeners
  setupAudioListeners();

  // Setup HUD button listeners
  setupHUDListeners();

  // Load map JSON then start
  try {
    await loadMapJSON('public/assets/maps/level-1-manoir.json');
  } catch(e) {
    console.warn('Failed to load level-1-manoir.json, falling back to level-1.json', e);
    await loadMapJSON('public/assets/maps/level-1.json');
  }
  state.gameState = 'playing';

  try {
    renderer3d = new ThreeRenderer();
  } catch(err) {
    console.error('ThreeRenderer init failed:', err);
    document.body.innerHTML = '<pre style="color:red;padding:20px;">'+err.stack+'</pre>';
    return;
  }

  // Wire up renderer reference for update.js (needed for door opening, zombie mesh spawning)
  setRenderer(renderer3d);

  // Setup input (needs tryShoot which needs renderer reference)
  setupInput(tryShoot);

  requestAnimationFrame(gameLoop);
}

startGame();
