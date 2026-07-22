---
name: canvas-feature-development
description: Workflow command scaffold for canvas-feature-development in TENeT.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /canvas-feature-development

Use this workflow when working on **canvas-feature-development** in `TENeT`.

## Goal

Implements new features or major changes to the map canvas rendering and interaction logic, often involving both the CanvasLayer component and associated hooks for data or overlay logic.

## Common Files

- `frontend/src/components/map/CanvasLayer.tsx`
- `frontend/src/hooks/useCanvasData.ts`
- `frontend/src/hooks/useCanvasOverlay.tsx`
- `frontend/src/App.tsx`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit or create frontend/src/components/map/CanvasLayer.tsx
- Edit or create related hook in frontend/src/hooks/ (e.g., useCanvasData.ts or useCanvasOverlay.tsx)
- Update frontend/src/App.tsx if integration or wiring is needed
- Optionally update or add tests in frontend/src/hooks/ or frontend/src/components/map/

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.