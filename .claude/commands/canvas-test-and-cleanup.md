---
name: canvas-test-and-cleanup
description: Workflow command scaffold for canvas-test-and-cleanup in TENeT.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /canvas-test-and-cleanup

Use this workflow when working on **canvas-test-and-cleanup** in `TENeT`.

## Goal

Adds or updates tests for canvas-related components and hooks, and/or performs code cleanup such as removing trailing whitespace or deleting dead files.

## Common Files

- `frontend/src/hooks/useCanvasOverlay.test.tsx`
- `frontend/src/components/PerformanceCanvasLayer.test.tsx`
- `frontend/src/components/map/CanvasLayer.tsx`
- `frontend/src/hooks/useCanvasData.ts`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Edit or add test files in frontend/src/hooks/ or frontend/src/components/
- Remove dead or orphaned files if necessary
- Strip trailing whitespace from canvas-related files

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.