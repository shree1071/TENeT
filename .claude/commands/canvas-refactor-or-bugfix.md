---
name: canvas-refactor-or-bugfix
description: Workflow command scaffold for canvas-refactor-or-bugfix in TENeT.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /canvas-refactor-or-bugfix

Use this workflow when working on **canvas-refactor-or-bugfix** in `TENeT`.

## Goal

Refactors or fixes bugs in the canvas rendering system, typically touching both the CanvasLayer component and its supporting hooks.

## Common Files

- `frontend/src/components/map/CanvasLayer.tsx`
- `frontend/src/hooks/useCanvasData.ts`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit frontend/src/components/map/CanvasLayer.tsx
- Edit corresponding hook in frontend/src/hooks/ (e.g., useCanvasData.ts)
- Optionally update or add related tests

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.