# NEXUS Sentinel — Judge Q&A Cheat Sheet

> **Author:** Sai lane, NEXUS Sentinel team. Last updated 2026-07-01. Use this to verify any claim in 60 seconds.

## 1. "Is the live adapter actually running?"

**Yes.** `GET https://nexus-sentinel-policy-adapter.onrender.com/health` returns `{"status": "ok"}`. The service is deployed on Render free tier with a 2-min keep-warm pinger.

- Adapter source: [`nexus_uipath_bridge/app.py:1-50`](nexus_uipath_bridge/app.py)
- Deploy config: [`render.yaml`](render.yaml)
- Live evidence: [`evidence/live-test/output.txt`](evidence/live-test/output.txt)

## 2. "What does the live adapter actually do on a request?"

It runs **4 deterministic rule checks** (model-identity, policy-tests, service-health, evidence-attached) on a strictly-typed Pydantic envelope. It does **not** call an LLM, does **not** parse the prompt semantically, and does **not** make any trust decision based on model output.

- Request schema: [`nexus_uipath_bridge/app.py:80-120`](nexus_uipath_bridge/app.py) (`EvaluateRequest`, `extra="forbid"`)
- Rule logic: [`nexus_uipath_bridge/policy.py`](nexus_uipath_bridge/policy.py)
- The `prompt` field is logged for human review but **not** consumed by the trust decision. This is the BIPIA pattern.

## 3. "Can the model bypass the gate by injecting into tool arguments?"

**No.** The `VerifyRequest` and `EvaluateRequest` schemas use `extra="forbid"` and `StrictBool`. Tool arguments are not parsed from free text. This is the INJECAGENT defense.
- Tests: [`nexus_uipath_bridge/tests/test_uipath_sentinel_contract.py:14 tests, all passing`](nexus_uipath_bridge/tests/test_uipath_sentinel_contract.py)
- Test result: 30 tests passing, 2 xfailed (documented in [README](README.md#testing)).

## 4. "Show me a real instance running through the system."

**Recorded live at 00:04:47 UTC, 2026-07-01.** Verdict chain: `HOLD -> ALLOW -> VERIFICATION_FAILED -> VERIFICATION_PASSED`. Runtime 2.641s. Audit-chain integrity: True.

- Summary: [`artifacts/instance-timeline/SUMMARY.md`](artifacts/instance-timeline/SUMMARY.md)
- Full event log: [`artifacts/instance-timeline/instance-1.json`](artifacts/instance-timeline/instance-1.json)
- Narrative: [`artifacts/instance-timeline/instance-1.md`](artifacts/instance-timeline/instance-1.md)
- Recording script: [`tools/record_instance.py`](tools/record_instance.py) (re-runnable)

## 5. "Why is the verdict chain that shape and not 4 straight ALLOWs?"

The 4 sample cases exercise **all four decision branches** of the BPMN:
- Sample 01 (safety hold): `HOLD` — gates injection-style prompts.
- Sample 02 (low-risk approval): `ALLOW` — bounded remediation is safe.
- Sample 03 (verification failed): `VERIFICATION_FAILED` — bounded remediation completed but post-conditions failed; system demands rework.
- Sample 04 (verification passed): `VERIFICATION_PASSED` — full close-loop closure.

This is the **happy path** of a governed recovery: hold -> approve -> run -> verify -> re-run -> close.

## 6. "Where is the human-in-the-loop?"

In the Maestro BPMN: `AI Release Manager Approval (User Task)` is a **user task with a defined role assignment** (`requiredHumanRole`) and a typed `decision` enum (Approve / Reject / Escalate). The verifier's `evaluationAuditId` binds the human's decision to the case.

- BPMN source: [`uipath/NEXUSSentinelBPMN/Process.bpmn`](uipath/NEXUSSentinelBPMN/Process.bpmn)
- Canvas binding spec: [`docs/CANVAS-BINDING-SPEC.md`](docs/CANVAS-BINDING-SPEC.md)
- Studio canvas: live at [`evidence/studio-final/canvas-0-issues.png`](evidence/studio-final/canvas-0-issues.png) (0 validation issues)

## 7. "Why one agentic node and not more?"

Because more would **dilute the gate**. The research grounding essay explains this in §4. The NEXUS Sentinel's value is its **typed contract at every boundary**, not its surface area.
- Essay: [`docs/RESEARCH-GROUNDING.md` §4](docs/RESEARCH-GROUNDING.md)

## 8. "What 5 papers ground this design?"

Mapped 1:1 in [`docs/RESEARCH-GROUNDING.md`](docs/RESEARCH-GROUNDING.md):
1. **Progent** (ACL 2024) -> typed action algebra
2. **BIPIA** (EMNLP 2024) -> boundary-aware injection defense
3. **INJECAGENT** (IEEE S&P 2025) -> strict typing at every tool boundary
4. **Huang V&V** (NASA TM 2023) -> operational provenance, not metrics
5. **Fudan oversight framework** (2024-25) -> human-in-the-loop as a policy primitive

## 9. "Is the BPMN committed or only live in the cloud canvas?"

**Both.** The committed XML ([`uipath/NEXUSSentinelBPMN/Process.bpmn`](uipath/NEXUSSentinelBPMN/Process.bpmn)) and the live Studio canvas (screenshots in [`evidence/studio-final/`](evidence/studio-final/)) contain the same 18 connections, 16 nodes, and 4 conditional flows.

## 10. "Why didn't you ship the cloud-published process to the Orchestrator?"

The trial-tier `upgrade-trial-dialog` is a UiPath modal that blocks the **Publish** button with no in-page dismiss affordance. The single escape (the `Go to projects` link) navigates away from the canvas. The exact friction is documented in [`docs/PRODUCT-FEEDBACK.md` P0-B](docs/PRODUCT-FEEDBACK.md) as the #1 ask to the UiPath team.

The BPMN is **valid and deployable**; the publish UI itself is the blocker.

## 11. "What is the demo video?"

3-min narrated walkthrough: [`assets/video/agenthack-demo-evidence-narrated.mp4`](assets/video/agenthack-demo-evidence-narrated.mp4). The narration timeline is in [`assets/video/DEMO-NARRATION-TIMELINE.md`](assets/video/DEMO-NARRATION-TIMELINE.md).

## 12. "Where is the public writeup?"

- **GitHub hero:** [`RESULT.md`](RESULT.md) — 1-page live verdict chain + diagram.
- **Hugging Face README:** [`docs/HF-SPACE-README.md`](docs/HF-SPACE-README.md) — 655 words, research-essay tone.
- **Devpost entry:** [`docs/SUBMISSION.md`](docs/SUBMISSION.md) — artifact inventory + honest disclosures.
- **Tweet thread:** [`docs/TWEET-THREAD.md`](docs/TWEET-THREAD.md) — 7-tweet share moment.
- **Product feedback (separate award track):** [`docs/PRODUCT-FEEDBACK.md`](docs/PRODUCT-FEEDBACK.md) — 6 friction points, 4 asks.