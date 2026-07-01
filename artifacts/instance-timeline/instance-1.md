# NEXUS Sentinel — Instance Timeline (instance-1)

- **Endpoint:** `https://nexus-sentinel-policy-adapter.onrender.com`
- **Generated (UTC):** 2026-07-01T00:04:47.517613+00:00
- **Runtime:** 2.641 s
- **Verdict chain:** HOLD -> ALLOW -> VERIFICATION_FAILED -> VERIFICATION_PASSED

## Stage 1: Evaluate Release Risk (evaluate) — `01-safety-hold.json`
- **Timestamp (UTC):** 2026-07-01T00:04:45.519684+00:00
- **HTTP status:** 200
- **Case:** `CASE-2026-9821` | **Verdict:** `HOLD` | **Risk:** `HIGH`
- **Required human role:** `AI_RELEASE_MANAGER` | **Recommended stage:** `Safety Hold`
- **auditId:** `audit-350181fca5ac25581189`
- **input_fingerprint (sha256):** `8818adb27dfc444e95c4bebdde385ed78a24b3d7b8dde3f05ac9b4acda8f117d`
- **Reason codes:** MODEL_ECHO_MISMATCH, EVIDENCE_INCOMPLETE, HUMAN_APPROVAL_REQUIRED

## Stage 2: Evaluate Release Risk (evaluate) — `02-approved-remediation.json`
- **Timestamp (UTC):** 2026-07-01T00:04:46.962847+00:00
- **HTTP status:** 200
- **Case:** `CASE-2026-9821` | **Verdict:** `ALLOW` | **Risk:** `LOW`
- **Required human role:** `None` | **Recommended stage:** `Remediation`
- **auditId:** `audit-e4aa8d3bb4ed746965e7`
- **input_fingerprint (sha256):** `1ea6204fa4e9bea8fc5e85269c1cd90da54278d7e40c413a63009f7efa24a4cc`

## Stage 3: Verify Recovery (verify) — `03-verification-failed.json`
- **Timestamp (UTC):** 2026-07-01T00:04:47.254284+00:00
- **HTTP status:** 200
- **Case:** `CASE-2026-9821` | **Verified:** `False`
- **evaluationAuditId (linkage):** `audit-e4aa8d3bb4ed746965e7`
- **verify auditId:** `audit-d7793d20135c19f7bf5d` | **recommended_stage:** `Rework Required` | **reentry_stage:** `Investigation`
- **Reason codes:** MODEL_IDENTITY_STILL_MISMATCHED

## Stage 4: Verify Recovery (verify) — `04-verification-passed.json`
- **Timestamp (UTC):** 2026-07-01T00:04:47.517564+00:00
- **HTTP status:** 200
- **Case:** `CASE-2026-9821` | **Verified:** `True`
- **evaluationAuditId (linkage):** `audit-e4aa8d3bb4ed746965e7`
- **verify auditId:** `audit-5edb88fc62d3e08ac3a2` | **recommended_stage:** `Closure` | **reentry_stage:** `None`

## [resolution] Close-Loop Resolution — REWORK_REENTRY
- from verify seq: 3
- verified: `False` | recommended_stage: `Rework Required` | reentry: `Investigation`

## [resolution] Close-Loop Resolution — CLOSURE
- from verify seq: 4
- verified: `True` | recommended_stage: `Closure` | reentry: `None`
