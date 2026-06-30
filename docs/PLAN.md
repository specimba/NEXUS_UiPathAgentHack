# NEXUS Sentinel Late-Submission Sprint

## Summary
Deliver a truthful, working **Track 1 Maestro Case** submission by **21:00 Istanbul time on June 30**, with the organizer’s hard deadline at **06:00 Istanbul time on July 1**.

The current adapter, public repository, Render deployment, tests, and UiPath desktop workflow are usable foundations. The decisive missing requirement is a published, running **Studio Web Maestro Case**. Official rules require a functional Automation Cloud solution, public repository, public demo video under five minutes, and presentation deck. [Devpost requirements](https://uipath-agenthack.devpost.com/rules)

Use a timed fallback: spend no more than 60 minutes proving that a Case Management Project can be created, saved, validated, and exposes Publish. If entitlement blocks that gate, pivot completely to Track 2 using the existing BPMN draft.

## Implementation

### 1. Parallel Coordination
- Codex owns the critical path, repository truth, integration, tests, assets, and final checklist.
- Antigravity/Gemini operates the UiPath Case designer and records exact UI findings. It must not submit forms or publish without the sprint gate.
- Grok receives one bounded MCP/CDP review task: score the project against the five judging criteria and return only actionable gaps.
- Sai/Opus is advisory-only because its current window reports `Connection Error`; it joins only if connectivity recovers.
- Use CDP on `9224` for Grok. Use Computer Use only for UiPath and Antigravity surfaces that CDP cannot reach.
- Save every advisory response as a versioned review artifact; Codex reconciles it before adoption.

### 2. Maestro Case Critical Path
Create `NEXUS Sentinel AI Release Recovery` as a Studio Web Case Management Project.

Case fields:

- `case_id`
- `requested_model`
- `observed_model`
- `evidence_complete`
- `privileged_remediation`
- `human_approval`
- `verdict`
- `risk_level`
- `reason_codes`
- `verification_passed`
- `retry_count`
- `audit_id`

Stages:

1. `Intake`
2. `Investigation`
3. `Remediation`
4. `Verification`
5. `Closure`
6. Secondary: `Safety Hold`
7. Secondary: `Escalated`

Execution:

- Extend the existing UiPath workflow to support `evaluate` and `verify` modes and expose structured outputs instead of only raw JSON.
- Publish that workflow to Orchestrator and use it as the Case plan’s RPA/API task.
- `HOLD` activates `Safety Hold` and creates a Human Action for the AI Release Manager.
- Approval updates `human_approval=true` and re-evaluates the case.
- `DENY` activates `Escalated`.
- `ALLOW` enters `Remediation`.
- Failed verification sets `verification_passed=false`, increments `retry_count`, and re-enters `Investigation`.
- Passed verification enters `Closure`.
- UiPath owns all stages, human decisions, re-entry, and side effects. The NEXUS adapter remains advisory.

Case route passes only if, within 60 minutes, Studio Web permits project creation, save, validation, and Publish. Otherwise pivot to Track 2 and implement the same flow as BPMN:

`Start → Evaluate → Verdict Gateway → Human Approval → Remediation → Verify → Rework Loop/End`.

### 3. Accuracy and Public Assets
Preserve the existing adapter contract; do not add unnecessary model dependencies.

Correct all public claims:

- Do not claim Agent Builder unless a real agent is shown running.
- Do not call in-memory audit records immutable or durable.
- Do not claim a complete Maestro deployment until a live instance is reproduced.
- Explicitly document Codex, Gemini, Kilo Code, and Cline contributions for coding-agent bonus eligibility.
- Include visible evidence of coding-agent use in the video.

Required assets:

- Public GitHub repository with accurate README and Apache-2.0 license.
- Three screenshots: Case plan, Safety Hold/Human Action, and failed-verification re-entry or final closure.
- Six-slide deck using the official template:
  1. Problem
  2. NEXUS Sentinel solution
  3. UiPath/NEXUS architecture
  4. Live exception and human-approval flow
  5. Verification/re-entry evidence
  6. Impact, limitations, and next steps
- A 4:15–4:40 demo recorded from a resettable case using AI English narration and burned-in captions.
- Upload the video publicly to YouTube and the deck to a public Google Drive link.
- Populate the late Devpost submission but stop before the final Submit button for operator approval.

## Verification
- Run all public repository tests; retain at least the current `17 passed`.
- Verify Render `/health`, OpenAPI, all four sample payloads, idempotent replay, audit retrieval, and cold-start behavior.
- Reproduce one complete UiPath Cloud run:
  - mismatch produces `HOLD`;
  - human approval releases remediation;
  - first verification fails and re-enters Investigation;
  - second verification succeeds and closes.
- Confirm a published process/case instance appears in Maestro; the current tenant has zero published processes.
- Secret-scan the repository and presentation assets.
- Test repository, video, deck, Render, and Devpost links from a logged-out browser.
- Confirm video duration is under five minutes and visibly shows UiPath Cloud executing, not only slides or local curl commands.
- Complete a judge matrix covering business impact, platform depth, technical execution, completeness, creativity, and coding-agent evidence.

## Timeline and Defaults
- `11:30–12:30`: Case feasibility gate and conditional Track 2 pivot.
- `12:30–15:30`: Build, publish, and run the UiPath orchestration.
- `15:30–17:00`: Stabilize the full two-pass scenario and capture screenshots.
- `17:00–18:30`: Reconcile README, Devpost copy, and coding-agent evidence.
- `18:30–19:30`: Produce deck and AI narration.
- `19:30–20:30`: Record, edit, caption, and upload the demo.
- `20:30–21:00`: Logged-out link verification and operator-approved submission.
- `21:00–05:30`: Emergency correction reserve only.
- Final submission remains operator-controlled.
- After submission, use the organizer’s 48-hour staging window only for compatible cloud refinements, not for changing the submitted project’s core identity.
