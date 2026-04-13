# [PROJECT_NAME]

## Project
[One-line game description]
**Stack**: Phaser 3 / Three.js / Babylon.js, TypeScript, Vite

## Setup
```bash
npm install
npm run dev
# Visit: http://localhost:5173 (Vite default)
```

## Key Commands
| Task | Command |
|------|---------|
| Dev Server | `npm run dev` |
| Build | `npm run build` |
| Preview | `npm run preview` |
| Tests | `npm test` |
| Type Check | `npx tsc --noEmit` |
| Lint | `npm run lint` |

## Architecture
- `src/` — Game source
  - `scenes/` — Phaser/Three.js scenes (main game loop)
  - `game/` — Game logic (decoupled from engine)
    - `entities/` — Game objects (player, enemies, items)
    - `systems/` — Game systems (physics, collision, AI)
    - `state/` — Game state management
  - `ui/` — User interface (menus, HUD)
  - `assets/` — Images, audio, data
  - `main.ts` — Game initialization
- `tests/` — Unit tests (Vitest)
- `public/` — Static files
- `index.html` — Entry point

## Conventions
- TypeScript strict mode required
- Game logic separate from rendering (testable)
- Scenes for state management (Phaser)
- Event-driven communication between systems
- No global variables (dependency injection)
- Asset loading in preload phase

## Key Dependencies
- **Phaser 3** / Three.js / Babylon.js — Game engine
- **TypeScript** — Type safety
- **Vite** — Build/dev server
- **Vitest** — Testing framework
- **ESLint** / **Prettier** — Code quality

## Game Loop (Phaser)
```typescript
// preload() → create() → update() → render (built-in)
export class GameScene extends Phaser.Scene {
  preload() { /* Load assets */ }
  create() { /* Initialize */ }
  update() { /* Every frame, ~60fps */ }
}
```

## Anti-Patterns
- ❌ Game logic inside scenes (hard to test)
- ❌ Direct sprite manipulation without abstraction
- ❌ Global game state (use scene or manager)
- ❌ No tests for game logic
- ❌ Hardcoded values (use constants)
- ❌ Heavy computation in update() (optimize!)

## Game State Management
```typescript
// Game state in a separate class (testable)
class GameState {
  player: Player
  enemies: Enemy[] = []
  score: number = 0
  
  takeDamage(damage: number) {
    this.player.hp -= damage
  }
}

// Scenes use game state
scene.gameState = new GameState()
```

## Physics & Collision (Phaser)
- **Type**: Arcade (2D simple) or Matter (realistic)
- See `config.physics` in game initialization
- Collision handled in update or event listeners

## Sprite Animation (Phaser)
```typescript
// Define animation in create
this.anims.create({
  key: 'player-walk',
  frames: this.anims.generateFrameNumbers('player', { start: 0, end: 3 }),
  frameRate: 10,
  repeat: -1,
})

// Play animation
sprite.play('player-walk')
```

## Input Handling
```typescript
// Keyboard
this.input.keyboard?.on('keydown-SPACE', () => { })

// Mouse
sprite.setInteractive()
sprite.on('pointerdown', () => { })
sprite.on('pointerover', () => { })
```

## Testing Game Logic
```typescript
// ✅ Test pure logic
function calculateDamage(attack: number, defense: number): number {
  return Math.max(1, attack - defense)
}

test('calculates damage correctly', () => {
  expect(calculateDamage(10, 3)).toBe(7)
})

// ✅ Test game state
test('player takes damage', () => {
  const state = new GameState()
  state.takeDamage(5)
  expect(state.player.hp).toBe(95) // if max is 100
})

// ❌ Don't test scene internals
// test('scene plays animation', () => { ... })  // Hard to test!
```

## Performance Tips
- [ ] Batch draw calls
- [ ] Use object pooling for bullets/particles
- [ ] Profile with DevTools
- [ ] Limit draw calls per frame
- [ ] Use texture atlases (not individual images)
- [ ] Cache heavy calculations

## Audio
- **Preload**: `this.sound.add('bgm', { loop: true })`
- **Play**: `this.sound.play('bgm')`
- **Stop**: `this.sound.stop('bgm')`

## Deployment
```bash
npm run build
# Deploy `dist/` to static hosting (GitHub Pages, Netlify, etc.)
```

## Development Workflow
1. Create game scene
2. Load assets in preload
3. Create game objects in create
4. Update positions in update
5. Test game logic separately
6. Run `npm test` (game logic tests)
7. Run `npm run dev` to visualize
8. Commit and push

## Skills
@skills/coding-standards.md @skills/validation.md @skills/typing-for-games.md @skills/phaser-patterns.md (if Phaser)

## References
- [Phaser 3 Documentation](https://photonstorm.github.io/phaser3-docs/)
- [Three.js Documentation](https://threejs.org/docs/)
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
