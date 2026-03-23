// ==================== MAP LOADING FROM JSON ====================
import {
  GND, WALL, WDEST, BUSH, WATER, CARPET, STONE, DIRT, GRAVEL, WOOD, DOOR,
  BATHROOM, WORN_CARPET, FURNITURE,
  DECO_NONE, DECO_BONES, DECO_SKULL, DECO_CRACK, DECO_WEB,
  DECO_BLOOD, DECO_PEBBLES, DECO_GRASS_TUFT, DECO_MUSHROOM,
  DECO_TORCH, DECO_PUDDLE,
  DECO_FALLEN_BOOKS, DECO_KITCHEN_UTENSILS, DECO_BROKEN_TOYS,
  DECO_BROKEN_MIRROR, DECO_WATER_PUDDLE,
  MAP, DECO,
  COLS, ROWS, setCOLS, setROWS,
  state, spawnZ,
  setFurnitureList, setSurpriseSpawns, setBossSpawn,
} from './state.js';

const groundNameToId = {
  'grass':GND, 'stone':STONE, 'dirt':DIRT, 'gravel':GRAVEL,
  'wood_light':WOOD, 'carpet':CARPET, 'water':WATER, 'door':DOOR,
  'bathroom_tile':BATHROOM, 'worn_carpet':WORN_CARPET,
};
const groundJsonToInternal = [GND, STONE, DIRT, GRAVEL, WOOD, CARPET, WATER, DOOR, BATHROOM, WORN_CARPET];

const decoNameToId = {
  'bones':DECO_BONES, 'skull':DECO_SKULL, 'crack':DECO_CRACK, 'web':DECO_WEB,
  'blood':DECO_BLOOD, 'pebbles':DECO_PEBBLES, 'grass_tuft':DECO_GRASS_TUFT,
  'mushroom':DECO_MUSHROOM, 'torch':DECO_TORCH, 'puddle':DECO_PUDDLE,
  'fallen_books':DECO_FALLEN_BOOKS, 'kitchen_utensils':DECO_KITCHEN_UTENSILS,
  'broken_toys':DECO_BROKEN_TOYS, 'broken_mirror':DECO_BROKEN_MIRROR,
  'water_puddle':DECO_WATER_PUDDLE,
};

export async function loadMapJSON(url) {
  const resp = await fetch(url);
  const json = await resp.json();

  setCOLS(json.cols);
  setROWS(json.rows);
  // Re-read after set
  const cols = json.cols;
  const rows = json.rows;

  // Init arrays
  MAP.length = 0;
  DECO.length = 0;
  for(let r=0; r<rows; r++){
    MAP[r] = new Array(cols).fill(GND);
    DECO[r] = new Array(cols).fill(DECO_NONE);
  }

  // Ground
  for(let r=0; r<rows; r++){
    for(let c=0; c<cols; c++){
      const v = json.ground[r][c];
      MAP[r][c] = groundJsonToInternal[v] ?? GND;
    }
  }

  // Walls — support both formats: [r,c] pairs or {type:'row',...} objects
  if(json.walls){
    for(const w of (json.walls.indestructible||[])){
      if(Array.isArray(w)){
        const [r,c] = w;
        if(r<rows && c<cols) MAP[r][c] = WALL;
      } else if(w.type==='row'){
        for(let c=w.c1; c<=w.c2; c++) MAP[w.r][c] = WALL;
      } else if(w.type==='col'){
        for(let r=w.r1; r<=w.r2; r++) MAP[r][w.c] = WALL;
      }
    }
    for(const w of (json.walls.destructible||[])){
      const [r,c] = Array.isArray(w) ? w : [w.r, w.c];
      if(r<rows && c<cols) MAP[r][c] = WDEST;
    }
  }

  // Doors (override wall to DOOR)
  for(const [r,c] of (json.doors||[])){
    if(r<rows && c<cols) MAP[r][c] = DOOR;
  }

  // Bushes — support both 'bushes' and 'bushPositions' keys
  const bushData = json.bushes || json.bushPositions || [];
  for(const [r,c] of bushData){
    if(r<rows && c<cols && (MAP[r][c]===GND || MAP[r][c]===GRAVEL)) MAP[r][c] = BUSH;
  }

  // Furniture -> mark tiles as FURNITURE for collision (except chandeliers — passable)
  let newFurnitureList = [];
  for(const f of (json.furniture||[])){
    const fw = f.w || 1, fh = f.h || 1;
    newFurnitureList.push({type: f.type, r: f.r, c: f.c, w: fw, h: fh, grand: f.grand || false});
    if(f.type === 'chandelier') continue; // chandeliers hang from ceiling, no collision
    for(let dr=0; dr<fh; dr++){
      for(let dc=0; dc<fw; dc++){
        const rr = f.r+dr, cc = f.c+dc;
        if(rr<rows && cc<cols) MAP[rr][cc] = FURNITURE;
      }
    }
  }
  setFurnitureList(newFurnitureList);

  // Decorations
  for(const dec of (json.decorations||[])){
    const did = decoNameToId[dec.type];
    if(did !== undefined && dec.r<rows && dec.c<cols){
      DECO[dec.r][dec.c] = did;
    }
  }

  // Spawns
  if(json.spawns){
    const sp = json.spawns;
    if(sp.player){
      state.player.x = sp.player.col + 0.5;
      state.player.y = sp.player.row + 0.5;
    }
    for(const z of (sp.zombies||[])){
      const t = z.type || 'normal';
      if(t==='normal') spawnZ(z.col, z.row, 1, 38, '#5a8f3c', 'Zombie');
      else if(t==='medium') spawnZ(z.col, z.row, 2, 48, '#7a6a2a', 'Z.Moyen');
      else if(t==='rage') spawnZ(z.col, z.row, 3, 60, '#8b2020', 'Z.Rage');
    }
    // Surprise spawns (deferred)
    setSurpriseSpawns((sp.surprises || []).map(s => {
      const trig = s.trigger || {};
      return {
        col: s.col, row: s.row,
        triggerCol: trig.col ?? s.triggerCol,
        triggerRow: trig.row ?? s.triggerRow,
        radius: trig.radius ?? s.radius ?? 3,
        triggered: false,
      };
    }));
    // Boss
    if(sp.boss){
      const trigger = sp.boss.trigger || {};
      setBossSpawn({
        col: sp.boss.col, row: sp.boss.row,
        wardrobeCol: trigger.c ?? sp.boss.wardrobeCol,
        wardrobeRow: trigger.r ?? sp.boss.wardrobeRow,
      });
    }
  }

  return json;
}
