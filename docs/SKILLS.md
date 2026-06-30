# NEXUS Sentinel — AgentHack Skill Bundle

_Three replayable skills, CLI-ready (claude / codex / antigravity / any agent). Save in the agent's skill directory or upload via the registry's import-zip flow._

---

---
name: Perform adversarial system review
description: Adversarial Level 2 review of a governed service/API: ground in the source to derive the real contract, fire live adversarial probes (happy path, abuse/injection, idempotency/replay, conflict, state transitions, audit), then write an evidence-backed review (failure modes, threats, SLA/retry, audit/correlation, misleading-claim audit, prioritized P0/P1). Read-only/non-destructive — never submits or changes permissions.
---

## When to use
Use when the user asks for an adversarial / red-team / "Level 2" / hostile-judge review of a running service, API, or agent governance layer — especially when there are *claims* to be verified and a live endpoint + source code are available.

## What it does
1. Grounds in source (`params.appSourcePath`): extracts routes, verdict/enum values, required fields, idempotency/audit/correlation logic, auth checks, and any keyword/tripwire controls.
2. Yields a decision so the agent confirms/edits the probe plan derived from the discovered contract.
3. Fires live probes via PowerShell Invoke-WebRequest against `params.endpointBase`, using payloads built from `params.samplesDir` with fresh unique request ids.
4. Yields a checkpoint with raw probe results so the agent verifies evidence is real before it gets written into claims.
5. Writes a structured review to `params.outputDir`.

## Safety
Read-only / non-destructive. Only GETs and POSTs of synthetic adversarial data against an already-public endpoint. Never submits, never changes permissions, never mutates server config.

## Parameters (defaults are for the NEXUS Sentinel adapter)
`systemName`, `appSourcePath`, `endpointBase`, `samplesDir`, `toolsDir`, `outputDir`.

## Notes
At the decision yield: read the discovered contract in observation, then return a probe plan object. At the checkpoint: confirm results look real before the doc is written.

---

---
name: Search and synthesize research papers
description: Ground a project in a local research-paper corpus: inventory the PDFs, theme-keyword match filenames against the project's pillars/gaps, extract abstracts (pymupdf, UTF-8-safe), confirm theme/paper selection via a decision yield, and return structured per-theme abstracts so the agent can write a grounded refinement/related-work synthesis. Read-only over the corpus.
---

## When to use
Use when the user has a local corpus of papers (PDFs) and wants to mine it for ideas that improve a specific project — e.g. "check our papers database and see what we can do," "find related work for X," "ground our design in the literature."

## What it does
1. Inventory the corpus (file counts, extensions, subfolders).
2. Theme-match filenames against a themes map (theme → keyword regex) tuned to the project's pillars and gaps.
3. Decision yield — confirms/refines theme list and which papers to extract.
4. Extract abstracts via pymupdf (fitz), writing to a UTF-8 file (avoids Windows cp1252 crashes).
5. Return structured perTheme data so the agent writes the synthesis narrative.

## Parameters
`papersDir`, `projectContext`, `themesJson` (optional override), `topPerTheme`, `toolsDir`, `outputDir`.

## Driving the replay
At the decision yield: confirm or refine per-theme filename matches. On completed: write the grounded synthesis from perTheme abstracts.

## Notes
Read-only. Requires Python with pymupdf.

---

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
3. Write handoff markdown to `outputDir` with a stable filename.

## Parameters
`projectPaths`, `handoffContext`, `currentStatus`, `p0Work`, `p1Work`, `laneAssignment`, `endStateChecklist`, `liveEndpoints`, `criticalGotchas`, `antiPatterns`, `projectLabel`, `outputDir`, `toolsDir`.

## Safety
Read-only over project paths. Only the handoff file is written. No commits, pushes, deployments, or permission changes.

## Notes
Reusable for any multi-lane project.

---

## Cross-skill usage
- All three are **read-only** over the project + corpus. Only outputs are written (review doc, abstracts file, handoff doc).
- Each yields **decision** / **checkpoint** gates so a supervising agent can intervene.
- All parameters have sensible defaults pointing at the NEXUS Sentinel project on this machine; override for other targets.

## CLI distribution
- The Simular registry treats these as **personal skills** (you own them). To share organization-wide, an account admin must promote them.
- For CLI consumption: copy the SKILL.md bodies above into each agent's skills directory (e.g. ~/.claude/skills/, ~/.codex/skills/). They run as plain Markdown + JavaScript via the agent's SimuLang runtime.
