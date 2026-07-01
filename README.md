# NEXUS Sentinel Recovery

A governed AI-release incident recovery workflow for **UiPath AgentHack Track 2: Maestro BPMN**.
<img width="1221" height="655" alt="chrome_b55Io8ZlYN" src="https://github.com/user-attachments/assets/cce38a65-2577-4267-b125-b39d83ddfc8f" />
https://www.youtube.com/watch?v=gEJQoGezs_E
UiPath Automation Cloud is the control and execution plane. The NEXUS Sentinel Policy Adapter is a deterministic advisory service that evaluates release evidence, returns `ALLOW`, `HOLD`, or `DENY`, and emits an auditable case transition. It never performs remediation.

## Demonstrated Outcome

The reference case catches a model identity mismatch and incomplete evidence, holds privileged remediation for an AI Release Manager, verifies the remediation, reopens the case when the first verification fails, and closes only after every check passes.

## Architecture

```mermaid
flowchart LR
    I["AI Release Incident"] --> M["UiPath Maestro BPMN"]
    M --> P["NEXUS Policy Adapter"]
    P -->|"HOLD"| H["AI Release Manager Approval"]
    P -->|"DENY"| E["Security Escalation"]
    P -->|"ALLOW"| R["Bounded Remediation"]
    H -->|"Approved"| R
    R --> V["Verification"]
    V -->|"Failed"| X["Rework Required"]
    X --> P
    V -->|"Passed"| C["Verified Closure"]
```

## UiPath Components

- Maestro BPMN owns the process sequence, verdict gateways, approval step, remediation, verification, rework loop, and closure.
- The published BPMN contains deterministic verdict routing and an explicit approval task.
- UiPath Solutions Management packages and deploys the process.
- The approval User Task is modeled but is not yet bound to an Action App.
- Orchestrator exposes a successful per-node execution trace.
- UiPath for Coding Agents is used to validate the adapter contract and deployment package.

## Public API

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Dependency-free liveness contract |
| `POST` | `/api/v1/case/evaluate` | Evidence and policy evaluation |
| `POST` | `/api/v1/case/verify` | Post-remediation verification |
| `GET` | `/api/v1/audit/{audit_id}` | Sanitized audit outcome retrieval |

The adapter rejects unknown fields and retains only a SHA-256 input fingerprint plus the structured outcome. Replaying an identical `request_id` returns the original result; changing its payload returns HTTP `409`.

## Run Locally

```bash
python -m pip install -r requirements.txt
uvicorn nexus_uipath_bridge.app:app --host 127.0.0.1 --port 8080
python -m pytest -q
```

Port `8080` is the standalone demo default. Port `7352` remains reserved for the private NEXUS Brain API and is not used by this service.

## Container

```bash
docker build -t nexus-sentinel .
docker run --rm -p 8080:8080 nexus-sentinel
```

Deploy the container to a public HTTPS service, then configure `SENTINEL_BASE_URL` in the UiPath API Workflow. No NEXUS private service, model, database, or credential is required.

## Demo Assets

- `samples/01-safety-hold.json`: mismatch plus missing evidence.
- `samples/02-approved-remediation.json`: corrected identity and approved action.
- `samples/03-verification-failed.json`: first verification forces re-entry after replacing the lineage placeholder with an evaluation `audit_id`.
- `samples/04-verification-passed.json`: final closure gate using the same evaluation lineage.
- `uipath/NEXUSSentinelBPMN/Process.bpmn`: portable source corresponding to the published process.
- `docs/LEVEL2_ORCHESTRATION_CONTRACT.md`: runtime routing, lineage, bounded retry, and honest approval gates.
- `docs/UIPATH_BUILD_GUIDE.md`: exact Maestro BPMN tasks, gateways, and deployment steps.
- `docs/DEMO_SCRIPT.md`: resettable five-minute presentation sequence.
- `docs/SUBMISSION.md`: Devpost-ready copy.
- `docs/PRESENTATION_OUTLINE.md`: slide-by-slide deck content.
- `docs/PRODUCT_FEEDBACK.md`: evidence-backed UiPath product feedback and corrections.
- `docs/JUDGE_MATRIX.md`: verified evidence mapped to the judging criteria.
- `docs/nexus-sentinel-research-grounded-plan.md`: literature-grounded governance architecture.
- `docs/nexus-sentinel-video-plan-v2.md`: workspace evidence demo video plan.
- `tests/test_adversarial_probes.py`: INJECAGENT-style adversarial probes. The complete suite reports `30 passed, 2 xfailed`; the expected failures document homoglyph and zero-width-space bypasses.

## Demo Video

https://github.com/user-attachments/assets/95e50e04-2dc8-48e5-90f3-7ee52e472dfc

## Presentation Deck

[Google Slides Presentation](https://docs.google.com/presentation/d/1J2eYo7MhnAZ9G4sv99mtZ8zBSmdpXKrnh8mi_pkJtvU/edit?usp=sharing)

## Safety Boundaries

- No local paths, secrets, prompts, model weights, or private NEXUS evidence are included.
- The adapter does not call Ollama, Brain API, GMR, or a GPU guard model.
- `selected_model` reports the observed and policy-accepted release model; it does not claim inference occurred.
- Policy outcomes are advisory. UiPath remains the authoritative orchestrator.
- Injection screening is a deterministic tripwire, not a complete semantic prompt-injection defense. Two obfuscation gaps remain explicitly test-marked.
- Numerical security, savings, and automation-rate claims are intentionally omitted unless reproduced.

## Roadmap

- Bind the approval User Task to an Action App and retain approver evidence.
- Replace the in-memory audit store with durable tenant-scoped storage.
- Add signed webhook authentication and tenant isolation.
- Add one gated AI Remediation Proposer after human authorization.

## License

Apache License 2.0. See `LICENSE`.
