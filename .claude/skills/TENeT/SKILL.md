```markdown
# TENeT Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill teaches the core development patterns and conventions used in the TENeT TypeScript codebase. The repository focuses on interactive map canvas rendering, with modular components and hooks for extensibility. You'll learn how to implement new features, refactor or fix bugs, and maintain high code quality through testing and cleanup, following established conventions and workflows.

## Coding Conventions

- **Language:** TypeScript
- **Framework:** None detected (React likely, based on `.tsx` files)
- **File Naming:** PascalCase for components and hooks  
  _Example:_ `CanvasLayer.tsx`, `UseCanvasData.ts`
- **Import Style:** Relative imports  
  _Example:_
  ```typescript
  import useCanvasData from '../hooks/useCanvasData';
  ```
- **Export Style:** Default exports  
  _Example:_
  ```typescript
  export default CanvasLayer;
  ```
- **Commit Messages:** Conventional commits with prefixes  
  _Examples:_
  - `feat: add zoom interaction to CanvasLayer`
  - `fix: correct overlay rendering bug`
  - `chore: remove unused test files`
- **Component Structure:**  
  - Components in `frontend/src/components/`
  - Hooks in `frontend/src/hooks/`

## Workflows

### Canvas Feature Development
**Trigger:** When adding or significantly updating map canvas rendering or interactivity  
**Command:** `/canvas-feature`

1. Edit or create `frontend/src/components/map/CanvasLayer.tsx` to implement new rendering or interaction logic.
2. Edit or create a related hook in `frontend/src/hooks/` (e.g., `useCanvasData.ts` or `useCanvasOverlay.tsx`) to manage data or overlays.
3. Update `frontend/src/App.tsx` if integration or wiring is needed.
4. Optionally, update or add tests in `frontend/src/hooks/` or `frontend/src/components/map/`.

_Example:_
```typescript
// frontend/src/components/map/CanvasLayer.tsx
import React from 'react';
import useCanvasData from '../../hooks/useCanvasData';

const CanvasLayer = () => {
  const data = useCanvasData();
  // ...rendering logic
};

export default CanvasLayer;
```

### Canvas Refactor or Bugfix
**Trigger:** When fixing a bug or refactoring logic in the map canvas rendering or data pipeline  
**Command:** `/canvas-fix`

1. Edit `frontend/src/components/map/CanvasLayer.tsx` to address bugs or improve structure.
2. Edit the corresponding hook in `frontend/src/hooks/` (e.g., `useCanvasData.ts`).
3. Optionally, update or add related tests.

_Example:_
```typescript
// frontend/src/hooks/useCanvasData.ts
const useCanvasData = () => {
  // Refactored or bugfixed logic here
};
export default useCanvasData;
```

### Canvas Test and Cleanup
**Trigger:** When improving test coverage or performing code hygiene tasks for canvas-related code  
**Command:** `/canvas-cleanup`

1. Edit or add test files in `frontend/src/hooks/` or `frontend/src/components/`.
2. Remove dead or orphaned files if necessary.
3. Strip trailing whitespace from canvas-related files.

_Example:_
```typescript
// frontend/src/hooks/useCanvasOverlay.test.tsx
import { renderHook } from '@testing-library/react-hooks';
import useCanvasOverlay from './useCanvasOverlay';

test('should return overlay data', () => {
  const { result } = renderHook(() => useCanvasOverlay());
  expect(result.current).toBeDefined();
});
```

## Testing Patterns

- **Test Framework:** Unknown (likely Jest or React Testing Library based on file patterns)
- **Test File Pattern:** Files named `*.test.*` (e.g., `useCanvasOverlay.test.tsx`)
- **Test Location:** Tests are placed alongside hooks or components, e.g., `frontend/src/hooks/` or `frontend/src/components/`
- **Typical Test Example:**
  ```typescript
  // frontend/src/components/PerformanceCanvasLayer.test.tsx
  import { render } from '@testing-library/react';
  import PerformanceCanvasLayer from './PerformanceCanvasLayer';

  test('renders without crashing', () => {
    render(<PerformanceCanvasLayer />);
  });
  ```

## Commands

| Command           | Purpose                                                        |
|-------------------|----------------------------------------------------------------|
| /canvas-feature   | Start a new feature or major update for map canvas rendering   |
| /canvas-fix       | Refactor or fix bugs in canvas rendering or data pipeline      |
| /canvas-cleanup   | Add/update tests or perform code cleanup for canvas components |
```
