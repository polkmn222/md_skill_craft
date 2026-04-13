# [PROJECT_NAME]

## Project
[One-line project description]
**Stack**: Next.js/React/Vue, TypeScript, Vite/Webpack, Tailwind CSS

## Setup
```bash
npm install
# Or: pnpm install / yarn install
cp .env.example .env.local
npm run dev
```

## Key Commands
| Task | Command |
|------|---------|
| Dev Server | `npm run dev` |
| Build | `npm run build` |
| Preview Build | `npm run preview` |
| Tests | `npm test` |
| Type Check | `npx tsc --noEmit` |
| Lint | `npm run lint` |
| Format | `npm run format` |

## Architecture
- `src/` — Source code
  - `app/` — Routes (Next.js App Router) or `pages/` (Next.js Pages Router)
  - `components/` — Reusable React components
  - `hooks/` — Custom React hooks
  - `lib/` — Utilities and helpers
  - `styles/` — Global styles (Tailwind config)
  - `types/` — TypeScript type definitions
- `public/` — Static assets
- `tests/` — Unit and integration tests (Vitest/Jest)
- `.env.local` — Environment variables (local only)
- `package.json` — Dependencies and scripts
- `tsconfig.json` — TypeScript strict mode enabled

## Conventions
- TypeScript strict mode required
- Component naming: PascalCase (Button.tsx)
- Hook naming: camelCase starting with `use` (useUser.ts)
- Type definitions in separate files or inline with `.d.ts`
- Tailwind CSS for styling (no inline styles)
- React functional components only (no classes)
- Custom hooks for state logic
- Props interface for each component

## Key Dependencies
- **React/Vue** — UI framework
- **TypeScript** — Type safety
- **Vite** / Next.js — Build tool/framework
- **Tailwind CSS** — Styling
- **Vitest** / Jest — Testing
- **ESLint** / **Prettier** — Code quality

## Anti-Patterns
- ❌ Inline CSS or `style={}` (use Tailwind)
- ❌ Missing TypeScript types
- ❌ API calls in components (use hooks/services)
- ❌ State management without library (if complex)
- ❌ Hardcoded API URLs (use environment variables)
- ❌ No tests for custom hooks

## State Management
- **Simple**: useState + useContext
- **Complex**: Zustand / Redux / Recoil (if needed)
- See `src/lib/store.ts` for store setup

## API Integration
- **Client**: Use `fetch` or `axios`
- **Server** (Next.js): Use `route.ts` for API routes
- **Authentication**: JWT tokens in cookies/localStorage
- See `src/lib/api.ts` for API client setup

## Testing
- Unit tests for utilities: `src/lib/*.test.ts`
- Component tests: `src/components/__tests__/*.test.tsx`
- Integration tests: `tests/integration/*.test.ts`
- E2E tests: Use Playwright (if needed)

## Environment Variables
```bash
NEXT_PUBLIC_API_URL=http://localhost:3000/api
VITE_API_URL=http://localhost:3000/api
DATABASE_URL=postgresql://...
```

## Performance
- [ ] Lazy load routes (Next.js automatic)
- [ ] Image optimization (next/image)
- [ ] Code splitting
- [ ] Bundle size monitoring

## Deployment
```bash
npm run build
npm start  # or deploy `dist/` to static host
```

## Development Workflow
1. Create feature branch
2. Run `npm run dev`
3. Develop component/feature
4. Write tests in `tests/`
5. Run `npm test` (ensure all pass)
6. Run `npm run lint` and `npm run format`
7. Commit and push
8. PR checks automatically run

## Skills
@skills/coding-standards.md @skills/validation.md @skills/orchestration.md
