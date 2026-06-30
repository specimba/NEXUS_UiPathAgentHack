# Level 2 Orchestration Contract

## Verified baseline

- UiPath Maestro BPMN package `Solution 1` v1.0.0 was deployed and produced three successful Service unattended jobs.
- The public policy adapter is deterministic and exposes evaluation, verification, health, and sanitized audit retrieval.
- The first published process proved the sequence but used default gateway routes and an unbound approval User Task.

## Level 2 controls

| Control | Contract | Evidence gate |
|---|---|---|
| Runtime verdict | `verdict` must be `ALLOW`, `HOLD`, or `DENY` and drives the Policy Verdict gateway. | Run one case per verdict; no default success route. |
| Evaluation lineage | Verification may carry `evaluation_audit_id`; the adapter rejects cross-case linkage. | Linked verification returns the same parent ID; wrong case returns HTTP 409. |
| Bounded recovery | `attempt` is 1-3. A failed third attempt routes to `Escalated` and cannot re-enter Investigation. | Adapter test plus Maestro max-retry path. |
| Human accountability | HOLD requires `AI_RELEASE_MANAGER`. A real approval record requires Action Center/Action App entitlement. | Do not claim accountable approval while the User Task auto-completes. |
| Error handling | Adapter errors and verification timeouts route to audit escalation, not remediation or closure. | Boundary-event validation and an injected failure run. |
| Idempotency | `request_id` plus content fingerprint returns the prior audit; changed content under the same ID returns 409. | Replay test and conflict test. |

## Specialist reconciliation

UiPath Autopilot confirmed variable mapping, workflow-backed service tasks, conditional gateways, retry counters, and boundary escalation are supported. Its first generated conditions used assignment syntax and produced four validation errors; independent validation detected this before publish.

Sai/Claude identified the key lifecycle defect: verification did not require or preserve evaluation lineage. The adapter now supports a checked `evaluation_audit_id` and bounded attempts. Sai also recommended treating durable audit storage and authenticated public routes as roadmap items unless reproduced.

Antigravity/Gemini was invoked for an architecture review but its first run ended in an MCP configuration error. No Antigravity claim was adopted.

## Two-job acceptance proof

1. Rework case: evaluation returns HOLD; approval is recorded if entitlement exists; verification attempt 1 fails; the process increments the counter and returns to Verify Recovery; a later passing verification closes.
2. Straight-pass case: evaluation returns ALLOW; remediation runs; verification passes on attempt 1; the process closes with zero retries.

Publishing is blocked until Studio Web validation returns zero issues and the runtime variable/output mappings are inspected.
