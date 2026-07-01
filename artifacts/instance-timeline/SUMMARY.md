# Instance Timeline — SUMMARY

- **Instance:** instance-1
- **Endpoint:** `https://nexus-sentinel-policy-adapter.onrender.com`
- **Generated (UTC):** 2026-07-01T00:04:47.517613+00:00
- **Total runtime:** 2.641 s

## Verdict / outcome sequence

`HOLD -> ALLOW -> VERIFICATION_FAILED -> VERIFICATION_PASSED`

Expected narrative: HOLD -> ALLOW/approval -> verification failed -> verification passed -> closure.

## Audit-chain integrity (verify.evaluation_audit_id -> evaluate.auditId)

- **Integrity OK:** True
- **Evaluate audit IDs:** `audit-350181fca5ac25581189`, `audit-e4aa8d3bb4ed746965e7`
- verify `03-verification-failed.json` -> `audit-e4aa8d3bb4ed746965e7` (matches evaluate: **True**)
- verify `04-verification-passed.json` -> `audit-e4aa8d3bb4ed746965e7` (matches evaluate: **True**)

## HTTP call results

| seq | stage | call | sample | status | error |
|---|---|---|---|---|---|
| 1 | Evaluate Release Risk | evaluate | 01-safety-hold.json | 200 |  |
| 2 | Evaluate Release Risk | evaluate | 02-approved-remediation.json | 200 |  |
| 3 | Verify Recovery | verify | 03-verification-failed.json | 200 |  |
| 4 | Verify Recovery | verify | 04-verification-passed.json | 200 |  |

## Exact request bodies used (secrets redacted — none present)

### 01-safety-hold.json -> evaluate
```json
{
  "request_id": "req-sentinel-001",
  "case_id": "CASE-2026-9821",
  "stage": "AI Triage",
  "requested_model": "stepfun-ai/step-3.7-flash:free",
  "observed_model": "unknown-model-stub",
  "privileged_remediation": true,
  "human_approval": false,
  "evidence": {
    "change_ticket": null,
    "model_manifest_hash": null,
    "rollback_plan": null,
    "test_report_hash": null
  },
  "evidence_notes": "Checking automated release trigger."
}
```

### 02-approved-remediation.json -> evaluate
```json
{
  "request_id": "req-sentinel-002",
  "case_id": "CASE-2026-9821",
  "stage": "Human Decision",
  "requested_model": "stepfun-ai/step-3.7-flash:free",
  "observed_model": "stepfun-ai/step-3.7-flash:free",
  "privileged_remediation": true,
  "human_approval": true,
  "evidence": {
    "change_ticket": "CHG-MAESTRO-902",
    "model_manifest_hash": "sha256:0d65b791fac83b271a2e7c3b87a8f12a2e8c239d5b780ac9018bc98ef732a392",
    "rollback_plan": "rollback-step-3.7-to-3.5-v1",
    "test_report_hash": "sha256:880bc1a8f9024f2b904df2b10ab78f3de74bc1a8c90bfa51a2e9b89fa7a5d3f2"
  },
  "evidence_notes": "AI Release Manager approved after verifying rollback plan."
}
```

### 03-verification-failed.json -> verify
```json
{
  "request_id": "req-verify-001",
  "case_id": "CASE-2026-9821",
  "remediation_id": "rem-sentinel-01",
  "evaluation_audit_id": "audit-e4aa8d3bb4ed746965e7",
  "attempt": 1,
  "checks": {
    "model_identity_matches": false,
    "policy_tests_pass": true,
    "service_health_pass": true,
    "evidence_attached": true
  }
}
```

### 04-verification-passed.json -> verify
```json
{
  "request_id": "req-verify-002",
  "case_id": "CASE-2026-9821",
  "remediation_id": "rem-sentinel-02",
  "evaluation_audit_id": "audit-e4aa8d3bb4ed746965e7",
  "attempt": 1,
  "checks": {
    "model_identity_matches": true,
    "policy_tests_pass": true,
    "service_health_pass": true,
    "evidence_attached": true
  }
}
```
