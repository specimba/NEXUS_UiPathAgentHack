# UiPath Studio Artifact

`NEXUSSentinelRobot` is the coded-automation side of the Maestro Case demo. It performs one bounded operation: submit a case-evaluation payload to the NEXUS Sentinel Policy Adapter and return the structured JSON response to UiPath.

## Open And Run

1. Open `uipath/NEXUSSentinelRobot/project.json` in UiPath Studio 2026.
2. Restore `UiPath.System.Activities` and `UiPath.WebAPI.Activities` dependencies.
3. Set environment variable `SENTINEL_BASE_URL` to the public HTTPS adapter URL, or supply `in_BaseUrl` as a workflow argument.
4. Run `Main.xaml`.
5. Confirm the Output panel contains HTTP `200` and a `HOLD` verdict for the default incident.

The local fallback is `http://127.0.0.1:8080`. No credential is stored in the project.

## Maestro Mapping

Use this process as the external/API task invoked from the Investigation stage. Deserialize `out_Response` and map:

| JSON field | Maestro field |
|---|---|
| `verdict` | `verdict` |
| `risk_level` | `riskLevel` |
| `reason_codes` | `reasonCodes` |
| `recommended_stage` | transition selector |
| `audit_id` | `auditId` |

Any non-2xx response throws and must route the case to `Escalated`; it must never default to `ALLOW`.

## Demo URL

For the live recording session on June 30, 2026, the certified quick-tunnel URL is supplied through `SENTINEL_BASE_URL`. It is intentionally not committed because Cloudflare quick-tunnel URLs are ephemeral.

For judging after submission, deploy the repository using `render.yaml` and update the Maestro API Workflow to the durable Render URL.
