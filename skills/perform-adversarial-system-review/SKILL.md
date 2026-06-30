---
name: Perform adversarial system review
description: Adversarial Level 2 review of a governed service/API: ground in the source to derive the real contract, fire live adversarial probes (happy path, abuse/injection, idempotency/replay, conflict, state transitions, audit), then write an evidence-backed review (failure modes, threats, SLA/retry, audit/correlation, misleading-claim audit, prioritized P0/P1). Read-only/non-destructive.
---

## When to use
Use when the user asks for an adversarial / red-team / "Level 2" / hostile-judge review of a running service, API, or agent governance layer — especially when there are *claims* to be verified and a live endpoint + source code are available.

## What it does
1. Grounds in source (params.appSourcePath): extracts routes, verdict/enum values, required fields, idempotency/audit/correlation logic, auth checks, and any keyword/tripwire controls.
2. Yields a decision so the agent confirms/edits the probe plan derived from the discovered contract.
3. Fires live probes via PowerShell Invoke-WebRequest against params.endpointBase, using payloads built from params.samplesDir with fresh unique request ids.
4. Yields a checkpoint with raw probe results so the agent verifies evidence is real before it gets written into claims.
5. Writes a structured review to params.outputDir.

## Safety
Read-only / non-destructive. Only GETs and POSTs of synthetic adversarial data against an already-public endpoint. Never submits, never changes permissions, never mutates server config.

## Parameters (defaults are for the NEXUS Sentinel adapter)
systemName, appSourcePath, endpointBase, samplesDir, toolsDir, outputDir.

## Notes
At the decision yield: read the discovered contract in observation, then return a probe plan object. At the checkpoint: confirm results look real before the doc is written.
