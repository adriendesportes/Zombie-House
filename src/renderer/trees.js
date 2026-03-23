// ==================== TREES / BUSHES ====================
import * as THREE from 'three';
import {
  BUSH, GND, WATER, WALL, WDEST, DOOR, WOOD, CARPET, STONE,
  BATHROOM, WORN_CARPET, FURNITURE,
  COLS, ROWS, MAP, hash, hashF,
} from '../state.js';

export function buildBushes(scene, renderer){
  for(const bm of renderer.bushMeshes) scene.remove(bm);
  renderer.bushMeshes = [];

  const loader = new THREE.TextureLoader();
  const treeTex = {
    pine: loader.load('public/assets/tilesets/tree-pine.png'),
    oak: loader.load('public/assets/tilesets/tree-oak.png'),
    spooky: loader.load('public/assets/tilesets/tree-spooky.png'),
    bush: loader.load('public/assets/tilesets/bush.png'),
    thorny: loader.load('public/assets/tilesets/bush-thorny.png'),
    fern: loader.load('public/assets/tilesets/bush-fern.png'),
    dead: loader.load('public/assets/tilesets/bush-dead.png'),
  };
  for(const k in treeTex){
    treeTex[k].magFilter = THREE.NearestFilter;
    treeTex[k].minFilter = THREE.LinearFilter;
    treeTex[k].colorSpace = THREE.SRGBColorSpace;
  }

  const treeTypes = ['pine', 'oak', 'spooky'];
  const bushTypes = ['bush', 'thorny', 'fern', 'dead'];

  const addSprite = (tex, x, y, z, size, dark=true) => {
    const mat = new THREE.SpriteMaterial({
      map: tex, transparent: true, depthWrite: false, alphaTest: 0.1,
      color: dark ? 0x404838 : 0xffffff,
    });
    const sprite = new THREE.Sprite(mat);
    sprite.scale.set(size, size, 1);
    sprite.position.set(x, y, z);
    sprite.center.set(0.5, 0.0);
    scene.add(sprite);
    renderer.bushMeshes.push(sprite);
  };

  const entranceX = 20.5, entranceZ = 29;
  const clearRadius = 5.0;

  for(let r=0; r<ROWS; r++){
    for(let c=0; c<COLS; c++){
      if(MAP[r][c]!==BUSH) continue;

      const density = 2 + hash(r, c, 160) % 3;

      for(let i=0; i<density; i++){
        const h1 = hashF(r, c, 200 + i * 10);
        const h2 = hashF(r, c, 201 + i * 10);
        const h3 = hashF(r, c, 202 + i * 10);

        const ox = (h1 - 0.5) * 1.0;
        const oz = (h2 - 0.5) * 1.0;

        const wx = c + 0.5 + ox;
        const wz = r + 0.5 + oz;

        const tileC = Math.floor(wx), tileR = Math.floor(wz);
        if(tileR < 0 || tileR >= ROWS || tileC < 0 || tileC >= COLS) continue;
        const tileType = MAP[tileR][tileC];
        if(tileType !== BUSH && tileType !== GND) continue;

        let nearBad = false;
        for(let dr=-1; dr<=1 && !nearBad; dr++){
          for(let dc=-1; dc<=1 && !nearBad; dc++){
            const nr = tileR+dr, nc2 = tileC+dc;
            if(nr>=0 && nr<ROWS && nc2>=0 && nc2<COLS){
              const nt = MAP[nr][nc2];
              if(nt===WATER || nt===WALL || nt===WDEST || nt===DOOR ||
                 nt===WOOD || nt===CARPET || nt===STONE || nt===BATHROOM ||
                 nt===WORN_CARPET || nt===FURNITURE) nearBad = true;
            }
          }
        }
        if(nearBad) continue;
        if(Math.hypot(wx - entranceX, wz - entranceZ) < clearRadius) continue;

        const roll = h3;
        if(roll < 0.4){
          const typeIdx = hash(r, c, 210 + i) % 3;
          const type = treeTypes[typeIdx];
          const size = 2.2 + h1 * 1.2;
          addSprite(treeTex[type], c + 0.5 + ox, 0, r + 0.5 + oz, size);
        } else if(roll < 0.65){
          const typeIdx = hash(r, c, 220 + i) % 3;
          const type = treeTypes[typeIdx];
          const size = 1.4 + h2 * 0.8;
          addSprite(treeTex[type], c + 0.5 + ox, 0, r + 0.5 + oz, size);
        } else if(roll < 0.85){
          const bushType = bushTypes[hash(r, c, 230 + i) % bushTypes.length];
          const size = 0.6 + h1 * 0.5;
          addSprite(treeTex[bushType], c + 0.5 + ox, 0, r + 0.5 + oz, size);
        } else {
          const bushType = ['fern', 'dead', 'thorny'][hash(r, c, 240 + i) % 3];
          const size = 0.35 + h2 * 0.3;
          addSprite(treeTex[bushType], c + 0.5 + ox, 0, r + 0.5 + oz, size);
        }
      }
    }
  }
}
