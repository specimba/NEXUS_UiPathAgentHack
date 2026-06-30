# Judge Matrix

| Criterion | Evidence | Status | Remaining gap |
|---|---|---|---|
| Business impact | AI-release mismatch, evidence hold, bounded remediation, and verification recovery | Demonstrated in adapter samples and BPMN | Add enterprise KPI data after pilot |
| Platform usage | Studio Web Maestro BPMN, Solutions Management package/deploy, Orchestrator job trace | Verified live on June 30, 2026 | Approval User Task is not Action App-bound |
| Technical execution | Deterministic policy API, idempotency, strict schemas, fail-closed UiPath workflow, 18 tests | Verified | Durable audit storage and webhook auth are future work |
| Completeness | Public repo, Apache-2.0, Render API, BPMN source, build guide, demo/deck scripts | Repository ready | Public video and deck links pending |
| Creativity | Governance adapter separates advisory policy from UiPath execution authority | Implemented | Add Test Cloud pack later |
| Coding agents | Codex implementation/integration; Gemini planning/review; Kilo Code and Cline UiPath support | Documented | Capture visible coding-agent evidence in video |

## Reproduced UiPath Evidence

- Studio Web validation: 0 issues.
- Published package: `Solution 1` version `1.0.0`.
- Deployment: successful.
- Orchestrator run: successful.
- Trace nodes: AI Release Incident, Evaluate Release Risk, Policy Verdict, AI Release Manager Approval, Execute Bounded Remediation, Verify Recovery, Verification Passed?, Verified Closure.

## Accuracy Boundary

The approval task is modeled but currently auto-completes because no Action App is bound. The submission must not claim a live Action Center approval.
