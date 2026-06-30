# UiPath Studio Artifact

`NEXUSSentinelRobot` is the coded-automation side of the Maestro BPMN demo. It performs one bounded adapter operation and returns the structured JSON response to UiPath. `in_Operation` accepts only `evaluate` or `verify`; any other value fails closed before network access.

## Open And Run

1. Open `uipath/NEXUSSentinelRobot/project.json` in UiPath Studio 2026.
2. Restore `UiPath.System.Activities` and `UiPath.WebAPI.Activities` dependencies.
3. Set `SENTINEL_BASE_URL` or supply `in_BaseUrl`.
4. Set `in_Operation` to `evaluate` or `verify` and provide the corresponding JSON in `in_CasePayload`.
5. Run `Main.xaml` and confirm HTTP `200` plus the expected structured result.

The local fallback is `http://127.0.0.1:8080`. No credential is stored in the project.

## Maestro Mapping

Use the workflow for both policy evaluation and post-remediation verification. Deserialize `out_Response` and map:

| Operation | JSON field | Maestro variable |
|---|---|---|
| evaluate | `verdict` | `evalVerdict` |
| evaluate | `risk_level` | `riskLevel` |
| evaluate | `required_human_role` | `requiredHumanRole` |
| evaluate | `audit_id` | `auditId` |
| verify | `verified` | `verified` |
| verify | `recommended_stage` | transition selector |
| verify | `reentry_stage` | `reentryStage` |
| verify | `retry_exhausted` | escalation selector |
| verify | `audit_id` | `verificationAuditId` |

Any non-2xx response throws and must route the process to `Escalated`; it must never default to `ALLOW` or closure.

## Deployment

The durable adapter is `https://nexus-sentinel-policy-adapter.onrender.com`. The repository contains `render.yaml`; no ephemeral tunnel URL is committed.
