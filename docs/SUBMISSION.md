# NEXUS Sentinel — UiPath AgentHack Submission

**Track:** 1 — Maestro Case (built on UiPath Cloud Maestro, Track-2-adjacent)
**Live demo:** https://nexus-sentinel-policy-adapter.onrender.com/health
**Source:** https://github.com/specimba/NEXUS_UiPathAgentHack
**Team:** NEXUS (Sai lane, Codex lane, Antigravity lane)

## One-paragraph summary

NEXUS Sentinel is a **deterministic, audit-ready policy gate** for AI release recovery, implemented as a typed closed loop. A remediation action enters a UiPath Maestro BPMN canvas, is evaluated against four rule gates (model-identity, policy-tests, service-health, evidence-attached), routed by verdict (ALLOW → execute, HOLD → human approval, DENY → escalate), executed, and verified back through the same gate with audit-id binding. Every step emits a SHA-256 fingerprint; the chain is replayable end-to-end via `/api/v1/audit/{id}`. The architecture is grounded in five specific papers (Progent, BIPIA, INJECAGENT, Huang V&V, Fudan oversight) — see `docs/RESEARCH-GROUNDING.md`.

## What judges will see

- **Live adapter** responding 200 to all 4 sample cases (`samples/01..04.json`).
- **Maestro BPMN** (`uipath/NEXUSSentinelBPMN/Process.bpmn`) with typed conditional flows, a human-approval user task with role assignment, and one gated agentic node.
- **30 passing tests** for the adapter's contract + policy logic.
- **A 3-min narrated demo** (`assets/video/`) showing the live adapter + the BPMN + the audit chain.
- **Research Grounding** (`docs/RESEARCH-GROUNDING.md`) — 5 papers mapped to 5 design decisions.
- **Product Feedback** (`docs/PRODUCT-FEEDBACK.md`) — 6 concrete friction points for the UiPath team, including the P0 publish-API gap.

## How it satisfies the Maestro Case requirements

| Requirement | Where it lives |
|---|---|
| 1. Build a process in UiPath Maestro | `uipath/NEXUSSentinelBPMN/Process.bpmn` (also: `docs/CANVAS-BINDING-SPEC.md` for the live Studio canvas binding) |
| 2. The process must include at least one Service Task | Evaluate Release Risk + Verify Recovery (HTTP POST to adapter) |
| 3. The process must include at least one Decision branch | Three gateway conditions: `${verdict == 'HOLD'}`, `${verified == true}`, `${verified == false}` |
| 4. (Optional) The process must include an Agentic activity | AI Remediation Proposer (gated by approval) |
| 5. The process must be runnable end-to-end | All four sample cases return 200, verify chain bound by `evaluationAuditId` |

## Submission artifacts

- `nexus_uipath_bridge/` — the deterministic policy adapter (FastAPI + Pydantic).
- `uipath/Main.xaml` — UiPath Studio workflow that drives the same flow locally.
- `uipath/NEXUSSentinelBPMN/Process.bpmn` — the Maestro BPMN canvas export.
- `samples/01..04.json` — the four sample request bodies.
- `docs/CANVAS-BINDING-SPEC.md` — paste-ready HTTP bindings for the live Studio canvas.
- `docs/RESEARCH-GROUNDING.md` — the 5-paper design rationale.
- `docs/PRODUCT-FEEDBACK.md` — the product feedback survey (separate award track).
- `docs/handoff-codex-antigravity.md` — multi-lane handoff log.
- `evidence/live-test/` — live adapter evidence + Studio canvas screenshots.
- `artifacts/instance-timeline/` — the recorded end-to-end instance (Lane A in flight).
- `assets/video/agenthack-demo-evidence-narrated.mp4` — the 3-min narrated demo.

## What we are NOT claiming

- We do **not** claim the Maestro Studio canvas auto-published to Orchestrator end-to-end on the trial tier. The BPMN export, the binding spec, and the local Studio workflow (`Main.xaml`) are all shipping; the Cloud publish path is the **single known gap** (see P0 in `docs/PRODUCT-FEEDBACK.md`).
- We do **not** claim a learned policy. The gate is **deterministic** on purpose — see `docs/RESEARCH-GROUNDING.md` §4 for the rationale.
- We do **not** claim zero prompt-injection. We claim a **defensible boundary** that demonstrably does not pass the model prompt into the trust decision.

## What we ARE claiming

- A working, testable, publicly deployable policy gate that solves a real problem (AI release recovery).
- A design that is grounded in published research, not invented from intuition.
- An implementation that runs against a live endpoint, not a mock.
- A code base that is clean, fully tested, and ready for review.