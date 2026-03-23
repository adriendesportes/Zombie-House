// ==================== AUDIO ====================

let audioCtx = null;
let musicGain = null;
let sfxGain = null;

export function initAudio(){
  if(audioCtx) return;
  audioCtx = new(window.AudioContext || window.webkitAudioContext)();
  musicGain = audioCtx.createGain(); musicGain.gain.value = 0.3; musicGain.connect(audioCtx.destination);
  sfxGain = audioCtx.createGain(); sfxGain.gain.value = 0.5; sfxGain.connect(audioCtx.destination);
  // Dark ambient music loop
  const buf = audioCtx.createBuffer(1, audioCtx.sampleRate * 4, audioCtx.sampleRate);
  const data = buf.getChannelData(0);
  for(let i = 0; i < data.length; i++){
    const t = i / audioCtx.sampleRate;
    data[i] = (Math.sin(t*55)*0.15 + Math.sin(t*82.5)*0.1 + Math.sin(t*110)*0.08 + Math.sin(t*165*Math.sin(t*0.5))*0.05) * (0.8 + Math.sin(t*0.3)*0.2);
  }
  const src = audioCtx.createBufferSource(); src.buffer = buf; src.loop = true; src.connect(musicGain); src.start();
}

export function playSFX(freq, dur, type){
  if(!audioCtx) return;
  const osc = audioCtx.createOscillator(); const g = audioCtx.createGain();
  osc.type = type || 'square'; osc.frequency.value = freq;
  g.gain.setValueAtTime(0.3, audioCtx.currentTime); g.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + dur);
  osc.connect(g); g.connect(sfxGain); osc.start(); osc.stop(audioCtx.currentTime + dur);
}

export function sfxShoot(){ playSFX(800, 0.1, 'sine'); playSFX(600, 0.08, 'square'); }
export function sfxHit(){ playSFX(200, 0.15, 'sawtooth'); }
export function sfxZombieDie(){ playSFX(150, 0.3, 'sawtooth'); playSFX(100, 0.4, 'sine'); }
export function sfxPlayerHit(){ playSFX(120, 0.2, 'square'); playSFX(80, 0.3, 'sine'); }
export function sfxVictory(){ playSFX(523, 0.15, 'sine'); setTimeout(()=>playSFX(659, 0.15, 'sine'), 150); setTimeout(()=>playSFX(784, 0.3, 'sine'), 300); }
export function sfxGameOver(){ playSFX(200, 0.3, 'sine'); setTimeout(()=>playSFX(150, 0.3, 'sine'), 200); setTimeout(()=>playSFX(100, 0.5, 'sine'), 400); }
export function sfxRoar(){ playSFX(80, 0.5, 'sawtooth'); playSFX(60, 0.6, 'square'); setTimeout(()=>playSFX(50, 0.4, 'sawtooth'), 200); }
export function sfxSurprise(){ playSFX(300, 0.15, 'square'); playSFX(400, 0.12, 'sine'); }

export function setupAudioListeners(){
  ['mousedown','touchstart','keydown'].forEach(ev => window.addEventListener(ev, initAudio, {once: false}));
}
