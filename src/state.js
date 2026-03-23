// ==================== STATE & CONSTANTS ====================

export const TILE_PX = 40;
export const PLAYER_SPEED = 160 / TILE_PX;

// Tile types (internal)
export const GND=0, WALL=1, WDEST=2, BUSH=3, WATER=4,
      CARPET=5, STONE=6, DIRT=7, GRAVEL=8, WOOD=9, DOOR=10,
      BATHROOM=11, WORN_CARPET=12, FURNITURE=13;

export const DECO_NONE=-1, DECO_BONES=0, DECO_SKULL=1, DECO_CRACK=2, DECO_WEB=3,
      DECO_BLOOD=4, DECO_PEBBLES=5, DECO_GRASS_TUFT=6, DECO_MUSHROOM=7,
      DECO_TORCH=8, DECO_PUDDLE=9,
      DECO_FALLEN_BOOKS=10, DECO_KITCHEN_UTENSILS=11, DECO_BROKEN_TOYS=12,
      DECO_BROKEN_MIRROR=13, DECO_WATER_PUDDLE=14;

// Map dimensions (set after JSON load)
export let COLS = 40;
export let ROWS = 32;

export function setCOLS(v) { COLS = v; }
export function setROWS(v) { ROWS = v; }

// Map arrays (populated from JSON)
export const MAP = [];
export const DECO = [];
export const GROUND_RAW = [];

// Shared mutable lists
export let furnitureList = [];
export let surpriseSpawns = [];
export let bossSpawn = null;
export let triggeredSurprises = new Set();
export let bossTriggered = false;

export function setFurnitureList(v) { furnitureList = v; }
export function setSurpriseSpawns(v) { surpriseSpawns = v; }
export function setBossSpawn(v) { bossSpawn = v; }
export function setTriggeredSurprises(v) { triggeredSurprises = v; }
export function setBossTriggered(v) { bossTriggered = v; }

// ==================== SEEDED RANDOM ====================
export function hash(r,c,s){
  let h=(r*374761393+c*668265263+(s||0)*1274126177)^0x5bd1e995;
  h=Math.imul(h^(h>>>15),0x27d4eb2d);
  return(h^(h>>>13))>>>0;
}
export function hashF(r,c,s){ return hash(r,c,s)/4294967296; }

// ==================== GAME STATE ====================
export const state = {
  player: {
    x: 20 + 0.5, y: 14 + 0.5,
    hp: 6, maxHp: 6,
    name: 'Angel',
    frame: 0, animTimer: 0,
    moving: false,
    bobTimer: 0, bobY: 0,
    facingDx: 0, facingDy: 1,
    facingDown: false,
    angle: 0,
    invincible: 0,
    points: 0,
  },
  zombies: [],
  projectiles: [],
  particles: [],
  dmgNumbers: [],
  gameTime: 0,
  mapVersion: 0,
  gameState: 'loading',
};

export function spawnZ(c,r,hp,spd,col,name,isBoss){
  const z = {
    x: c+0.5, y: r+0.5,
    hp, maxHp: hp,
    speed: spd / TILE_PX,
    color: col, name,
    frame: 0, animTimer: 0,
    bobTimer: Math.random()*6.28, bobY: 0,
    hitCooldown: 0,
    facingDx: 0, facingDy: 1,
    angle: 0,
    moving: false,
    isBoss: !!isBoss,
  };
  state.zombies.push(z);
  return z;
}
