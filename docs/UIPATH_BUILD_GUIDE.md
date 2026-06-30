# UiPath Maestro BPMN Build Guide - NEXUS Sentinel

## Verified cloud artifact

The published process is `Maestro BPMN` in package `Solution 1` version `1.0.0`.

Flow:

`AI Release Incident -> Evaluate Release Risk -> Policy Verdict`

- `HOLD -> AI Release Manager Approval -> Execute Bounded Remediation`
- `ALLOW -> Execute Bounded Remediation`
- `DENY -> Security Escalation`
- `Execute Bounded Remediation -> Verify Recovery -> Verification Passed?`
- `Passed -> Verified Closure`
- `Failed -> Rework Required -> Evaluate Release Risk`

The Studio Web model validates with zero issues. Both exclusive gateways use explicit default paths and conditions.

## Adapter boundary

The checked-in Windows workflow calls `POST /api/v1/case/evaluate` and fails closed on non-2xx responses. The public adapter also exposes `POST /api/v1/case/verify` and sanitized audit retrieval. UiPath remains the only execution authority.

## Publish and run evidence

1. Studio Web validation: zero issues.
2. Package: `Solution 1`, version `1.0.0`.
3. Deployment: successful in shared folder `Solution 1`.
4. Manual Orchestrator job: successful.
5. Trace: incident, evaluation, verdict, approval, remediation, verification, verification gateway, and closure.

## Honest limitation

`AI Release Manager Approval` is currently a BPMN User Task with no Action App binding. It auto-completed in the verified run. A live Action Center handoff is planned but must not be claimed in the current submission.
