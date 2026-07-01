# NEXUS Sentinel — tweet thread (copy-paste ready)

> 7 tweets, 280-char each, designed to be posted in sequence. Last updated 2026-07-01.

## 1/7 — hook

We built a deterministic, audit-ready policy gate for AI release recovery in 6 hours for the @UiPath AgentHack.

It's a typed closed loop. Every state transition is auditable. Every decision binds to a prior audit id. The whole thing is publicly deployable.

🧵

## 2/7 — the problem

Production AI incidents today:

- A model regresses. A jailbreak lands. A prompt-injection campaign fires.
- The on-call engineer reads the trace, guesses at the rollback level, and ships a fix.
- Slow. Irreproducible. Unauditable.

This is fine for one-off. It's a disaster at scale.

## 3/7 — the design
NEXUS Sentinel is **5 stages** with a typed contract at every boundary:

1. Evaluate (typed request, no LLM in the trust decision)
2. Route (BPMN canvas, verdict-driven)
3. Approve (human role, decision enum, audit id)
4. Verify (binds to prior evaluate by audit id)
5. Re-evaluate (recovery runs inside the same typed algebra)

Every step emits a SHA-256 fingerprint. Replayable end-to-end.

## 4/7 — the research grounding

Every design decision traces to a specific paper. We wrote a short essay mapping 5 papers to 5 decisions:

- Progent (ACL '24) -> typed action algebra
- BIPIA (EMNLP '24) -> boundary-aware injection defense
- INJECAGENT (IEEE S&P '25) -> strict typing at every tool boundary
- Huang V&V (NASA '23) -> operational provenance, not metrics
- Fudan oversight (2024-25) -> human-in-the-loop as a policy primitive

No vibes. No invented-from-intuition.

## 5/7 — the live demo

It's live: https://nexus-sentinel-policy-adapter.onrender.com

One recorded instance, 2.6s, audit-chain integrity True:

HOLD -> ALLOW -> VERIFICATION_FAILED -> VERIFICATION_PASSED

Every step has a fingerprint, a timestamp, an audit id. You can hit /api/v1/audit/{id} and replay any single decision.

## 6/7 — the BPMN canvas

We built the same flow in UiPath Maestro:

- Typed conditional flows
- Human approval user task with role assignment
- One gated agentic node (AI Remediation Proposer)
- Audit-id binding across service tasks

The local export is in the repo. The live Cloud canvas needs a publish-API fix from UiPath (we wrote them a P0 ask).

## 7/7 — where to find it

Repo: github.com/specimba/NEXUS_UiPathAgentHack
Live: nexus-sentinel-policy-adapter.onrender.com
Live instance: artifacts/instance-timeline/ in the repo
Research essay: docs/RESEARCH-GROUNDING.md
Product feedback: docs/PRODUCT-FEEDBACK.md

This is a small, working answer to "how do we make AI recovery auditable?"

Grateful to @UiPath and the AgentHack judges for the chance to ship it.