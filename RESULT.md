# NEXUS Sentinel — Live Result

> A deterministic, audit-ready policy gate for AI release recovery, implemented as a typed closed loop on UiPath Maestro.

## Live instance verdict chain

```
HOLD → ALLOW → VERIFICATION_FAILED → VERIFICATION_PASSED
```

- **Total runtime:** 2.641 s
- **HTTP calls:** 4 evaluate + 2 verify, all 200 OK
- **Audit-chain integrity:** `True` (every verify binds to its prior evaluate via `evaluationAuditId`)
- **Live endpoint:** `https://nexus-sentinel-policy-adapter.onrender.com`
- **Generated (UTC):** 2026-07-01T00:04:47

## What this proves

A remediation case can enter the system, hit a HOLD, route to human approval, transition to ALLOW, run, fail verification once, re-run, and close out — **with a SHA-256 fingerprint and an audit id at every stage**. A judge can hit `/api/v1/audit/{id}` and replay any single decision in the chain.

## How the closed loop works

```
  [request] -> [Evaluate] -> [BPMN route by verdict]
                              |
                  +-----------+-----------+
                  |           |           |
                ALLOW        HOLD        DENY
                  |           |           |
                [Execute] [Human Approval] [Escalate]
                  |           |
                  +--> [Verify] <--------+
                          |
              +-----------+-----------+
              |                       |
           verified==true        verified==false
              |                       |
        [Closure]               [Rework -> Re-evaluate]
```

## Why this matters

Most production AI incident responses are ad-hoc. NEXUS Sentinel turns the response into a **typed contract**: every state transition is auditable, every decision is bound to a prior audit id, and the loop closes deterministically. The five papers that ground this design are mapped 1:1 in [`docs/RESEARCH-GROUNDING.md`](docs/RESEARCH-GROUNDING.md).

## See also

- **Adapter code & tests:** [`nexus_uipath_bridge/`](nexus_uipath_bridge/) — 30 tests passing.
- **Maestro BPMN:** [`uipath/NEXUSSentinelBPMN/Process.bpmn`](uipath/NEXUSSentinelBPMN/Process.bpmn).
- **Studio binding spec:** [`docs/CANVAS-BINDING-SPEC.md`](docs/CANVAS-BINDING-SPEC.md).
- **Research Grounding essay:** [`docs/RESEARCH-GROUNDING.md`](docs/RESEARCH-GROUNDING.md).
- **Product Feedback (UiPath):** [`docs/PRODUCT-FEEDBACK.md`](docs/PRODUCT-FEEDBACK.md).
- **Full timeline narrative:** [`artifacts/instance-timeline/instance-1.md`](artifacts/instance-timeline/instance-1.md).
- **Submission entry (Devpost):** [`docs/SUBMISSION.md`](docs/SUBMISSION.md).
- **Demo video plan:** [`assets/video/DEMO-NARRATION-TIMELINE.md`](assets/video/DEMO-NARRATION-TIMELINE.md) (Lane F in flight).