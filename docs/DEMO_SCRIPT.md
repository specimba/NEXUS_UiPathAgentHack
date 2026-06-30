# UiPath AgentHack Demo Script - NEXUS Sentinel Recovery

**Target:** 4:20, English AI narration, burned captions.

## 0:00-0:35 - Problem
Show the title and architecture. Explain that AI releases can arrive with a model-identity mismatch, incomplete evidence, or failed post-remediation checks. UiPath is the execution authority; NEXUS supplies deterministic policy advice.

## 0:35-1:25 - Live Maestro BPMN
Show the published `NEXUS Sentinel AI Release Recovery` diagram. Point out Evaluate, the ALLOW/HOLD/DENY gateway, AI Release Manager Approval, bounded remediation, verification, failed-verification rework, and closure. State clearly that the current approval node is a BPMN User Task and is not yet connected to an Action App.

## 1:25-2:10 - Policy adapter
Open the public Render OpenAPI page and run the safety-hold sample. Highlight `HOLD`, `HIGH`, `MODEL_ECHO_MISMATCH`, `EVIDENCE_INCOMPLETE`, and the audit ID. Explain that the adapter never executes remediation and stores only a fingerprint plus structured outcome in process memory.

## 2:10-3:05 - Failure and recovery
Run `03-verification-failed.json`, showing `verified: false` and `reentry_stage: Investigation`. Then run `04-verification-passed.json`, showing closure. Use the BPMN diagram to connect these outcomes to the failed and passed paths.

## 3:05-3:50 - Published execution evidence
Show UiPath Solutions Management package `Solution 1` version `1.0.0`, successful deployment, and the successful Orchestrator trace through incident, evaluation, verdict, approval, remediation, verification, gateway, and closure.

## 3:50-4:20 - Engineering quality
Show the public GitHub repository, test result, Apache-2.0 license, and coding-agent contribution. Close with limitations: Action App binding and durable audit storage are next steps, not completed claims.
