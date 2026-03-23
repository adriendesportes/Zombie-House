// ==================== GROUND (from HQ atlas textures) ====================
import * as THREE from 'three';
import {
  GND, WALL, WDEST, BUSH, WATER, STONE, DIRT, GRAVEL, WOOD, CARPET, DOOR,
  BATHROOM, WORN_CARPET, FURNITURE,
  DECO_NONE, DECO_TORCH,
  COLS, ROWS, MAP, DECO, hash,
} from '../state.js';

export function buildGround(scene){
  const cs = 64; // pixels per tile in ground texture (downscaled from 128 atlas)
  const gCanvas = document.createElement('canvas');
  gCanvas.width = COLS * cs;
  gCanvas.height = ROWS * cs;
  const gCtx = gCanvas.getContext('2d');

  // Load atlas images and draw when ready
  const groundAtlas = new Image();
  const doorAtlas = new Image();
  const decoAtlas = new Image();
  let atlasLoaded = 0;
  const AT = 128; // atlas tile size

  // Tile type to atlas index
  const typeToAtlas = {
    [GND]: 0, [BUSH]: 0, [STONE]: 1, [DIRT]: 2, [GRAVEL]: 3,
    [WOOD]: 4, [CARPET]: 5, [WATER]: 6, [DOOR]: -1,
    [WALL]: 0, [WDEST]: 0,
    [BATHROOM]: 7, [WORN_CARPET]: 8,
    [FURNITURE]: 4,
  };
  const decoTypeToAtlas = {
    'bones':0, 'skull':1, 'crack':2, 'web':3, 'blood':4,
    'pebbles':5, 'grass_tuft':6, 'mushroom':7, 'torch':8, 'puddle':9,
    'fallen_books':10, 'kitchen_utensils':11, 'broken_toys':12,
    'broken_mirror':13, 'water_puddle':14,
  };

  // Create texture early so we can return the reference
  const tex = new THREE.CanvasTexture(gCanvas);
  tex.wrapS = THREE.ClampToEdgeWrapping;
  tex.wrapT = THREE.ClampToEdgeWrapping;
  tex.magFilter = THREE.LinearFilter;
  tex.minFilter = THREE.LinearFilter;

  const onAtlasLoad = () => {
    atlasLoaded++;
    if(atlasLoaded < 3) return;

    // Draw ground tiles from atlas
    for(let r=0; r<ROWS; r++){
      for(let c=0; c<COLS; c++){
        const t = MAP[r][c];
        const dx = c * cs, dy = r * cs;

        if(t === WATER){
          gCtx.fillStyle = '#06101a';
          gCtx.fillRect(dx, dy, cs, cs);
        } else if(t === DOOR){
          const doorVar = hash(r, c, 900) % 3;
          gCtx.drawImage(doorAtlas, doorVar * AT, 0, AT, AT, dx, dy, cs, cs);
        } else {
          const atlasIdx = typeToAtlas[t] ?? 0;
          gCtx.drawImage(groundAtlas, atlasIdx * AT, 0, AT, AT, dx, dy, cs, cs);
        }
      }
    }

    // Draw decorations on top of ground
    for(let r=0; r<ROWS; r++){
      for(let c=0; c<COLS; c++){
        const d = DECO[r][c];
        if(d === DECO_NONE) continue;
        if(d === DECO_TORCH) continue;
        const decoNames = ['bones','skull','crack','web','blood','pebbles','grass_tuft','mushroom','torch','puddle','fallen_books','kitchen_utensils','broken_toys','broken_mirror','water_puddle'];
        const name = decoNames[d];
        if(name === undefined) continue;
        const atlasIdx = decoTypeToAtlas[name];
        if(atlasIdx === undefined) continue;
        const dx = c * cs, dy = r * cs;
        gCtx.drawImage(decoAtlas, atlasIdx * AT, 0, AT, AT, dx, dy, cs, cs);
      }
    }

    // Update texture
    tex.needsUpdate = true;
  };

  groundAtlas.onload = onAtlasLoad;
  doorAtlas.onload = onAtlasLoad;
  decoAtlas.onload = onAtlasLoad;
  groundAtlas.src = 'public/assets/tilesets/ground-atlas.png';
  doorAtlas.src = 'public/assets/tilesets/door-atlas.png';
  decoAtlas.src = 'public/assets/tilesets/deco-atlas.png';

  // Fill with dark green while loading
  gCtx.fillStyle = '#2d5a1e';
  gCtx.fillRect(0, 0, gCanvas.width, gCanvas.height);

  const geo = new THREE.PlaneGeometry(COLS, ROWS);
  const mat = new THREE.MeshToonMaterial({map: tex, side: THREE.FrontSide});
  const plane = new THREE.Mesh(geo, mat);
  plane.rotation.x = -Math.PI/2;
  plane.position.set(COLS/2, 0, ROWS/2);
  scene.add(plane);

  return { groundTex: tex, groundCanvas: gCanvas, groundCtxRef: gCtx };
}
