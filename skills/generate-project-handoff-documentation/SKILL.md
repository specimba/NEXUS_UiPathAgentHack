---
name: Generate project handoff documentation
description: Generate a self-contained project handoff document for multi-agent hand-offs: inventory repo + branches + artifacts + runtime state, capture critical gotchas and anti-patterns, define prioritized work with verifiable acceptance gates, assign lane ownership (sole-writer / read-only verifier) to prevent concurrent-writer collisions, and ship an end-state checklist.
---

## When to use
Use when a project is being handed off between sessions, lanes, or agents — especially multi-agent setups where one lane was sole-writer and another lane picks up the rest.

## What it produces
12-section handoff: state of play, inventory + evidence, thesis, critical gotchas, P0/P1 work, replayable tools, owner-assignment table, runtime facts, acceptance gates, anti-patterns, end-state checklist, provenance.

## What it does
1. Inventory each project path via PowerShell (tree, recent git log, status, remote) — read-only.
2. Decision yield — shows the inventory + section sketches, confirms/refines owner split + P0.
3. Write handoff markdown to outputDir with a stable filename.

## Parameters
projectPaths, handoffContext, currentStatus, p0Work, p1Work, laneAssignment, endStateChecklist, liveEndpoints, criticalGotchas, antiPatterns, projectLabel, outputDir, toolsDir.

## Safety
Read-only over project paths. Only the handoff file is written. No commits, pushes, deployments, or permission changes.

## Notes
Reusable for any multi-lane project.
