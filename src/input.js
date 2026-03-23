// ==================== INPUT ====================

const keys = {};
let joyActive = false;
let joyStart = {x:0, y:0};
let joyDelta = {x:0, y:0};
const JOY_R = 55;
const JOY_DEAD = 12;

let _tryShootFn = null;

export function setupInput(tryShootFn){
  _tryShootFn = tryShootFn;

  window.addEventListener('keydown', e => { keys[e.key.toLowerCase()] = true; e.preventDefault(); });
  window.addEventListener('keyup', e => { keys[e.key.toLowerCase()] = false; });

  const joyZone = document.getElementById('joystick-zone');
  const joyKnob = document.getElementById('joystick-knob');
  const atkBtn = document.getElementById('atk-btn');

  joyZone.addEventListener('touchstart', e => {
    for(const t of e.changedTouches){
      joyActive = true;
      joyStart = {x: t.clientX, y: t.clientY};
      joyDelta = {x:0, y:0};
    }
    e.preventDefault();
  }, {passive: false});

  joyZone.addEventListener('touchmove', e => {
    for(const t of e.changedTouches){
      if(joyActive){
        joyDelta.x = t.clientX - joyStart.x;
        joyDelta.y = t.clientY - joyStart.y;
        const l = Math.min(Math.hypot(joyDelta.x, joyDelta.y), JOY_R);
        const a = Math.atan2(joyDelta.y, joyDelta.x);
        joyKnob.style.left = (33 + Math.cos(a)*l*0.5) + 'px';
        joyKnob.style.top  = (33 + Math.sin(a)*l*0.5) + 'px';
      }
    }
    e.preventDefault();
  }, {passive: false});

  joyZone.addEventListener('touchend', e => {
    joyActive = false;
    joyDelta = {x:0, y:0};
    joyKnob.style.left = '33px';
    joyKnob.style.top  = '33px';
    e.preventDefault();
  }, {passive: false});

  atkBtn.addEventListener('touchstart', e => { _tryShootFn(); e.preventDefault(); }, {passive: false});
  atkBtn.addEventListener('mousedown', e => { _tryShootFn(); });
  window.addEventListener('keydown', e => { if(e.key===' '||e.code==='Space'){ _tryShootFn(); e.preventDefault(); } });
  window.addEventListener('mousedown', e => { if(e.button===0) _tryShootFn(); });
}

export function getMove(){
  let dx=0, dy=0;
  if(keys['z']||keys['w']||keys['arrowup']) dy=-1;
  if(keys['s']||keys['arrowdown']) dy=1;
  if(keys['q']||keys['a']||keys['arrowleft']) dx=-1;
  if(keys['d']||keys['arrowright']) dx=1;
  if(joyActive){
    const l = Math.hypot(joyDelta.x, joyDelta.y);
    if(l > JOY_DEAD){ dx += joyDelta.x/l; dy += joyDelta.y/l; }
  }
  const l = Math.hypot(dx,dy);
  if(l>0){ dx/=l; dy/=l; }
  return {dx, dy};
}
