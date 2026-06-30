# UiPath AgentHack Product Feedback

## Context

NEXUS Sentinel Case explored a governed AI-release incident workflow: an external deterministic policy adapter evaluates case evidence; UiPath Maestro is intended to own case stages, decisions, human approval, and re-entry; failed verification returns the case to investigation; and audit identifiers preserve decision lineage without retaining raw prompts.

The public adapter is live at `https://nexus-sentinel-policy-adapter.onrender.com`. The public repository and Studio workflow prove the policy contract, but the team did not complete and verify the full Maestro Cloud case before the submission deadline.

## Evidence-Backed Findings

### 1. Headless publish needs a first-class contract

A non-interactive `@uipath/cli` publish attempt ran for approximately 24 minutes without useful stdout and produced no artifact. The working authentication path required interactive browser OAuth.

Requested improvement:

- Support service-account or client-credentials publishing.
- Provide machine-readable progress and result output.
- Return a non-zero exit code with a specific remediation message on failure.
- Document a minimal CI example for Automation Cloud.

### 2. Arbitrary governed REST services are difficult to discover

In the Maestro BPMN designer session, external integration was presented through Integration Service connectors. We did not find an obvious generic HTTP request task in the palette or inspected action options. This is an observed discoverability problem, not a claim that no such capability exists anywhere in UiPath.

Requested improvement:

- Add a clearly discoverable HTTP task with URL, method, headers, body, timeout, response mapping, and secret-reference fields.
- Publish an official "call a local service" development path with a supported tunnel and production migration guidance.

### 3. Canvas append behavior is fragile

The context-pad append action created an awkwardly placed node during testing. Duplicate or multi-selected elements disabled property editing. The XML tab was a useful declarative fallback and should be retained.

Requested improvement:

- Auto-place and auto-connect appended nodes.
- Make single-selection state clearer.
- Improve keyboard and accessibility support.
- Offer a safe BPMN validation preview before publish.

### 4. Hackathon entitlement and publish readiness need an explicit preflight

Saving eventually succeeded and displayed `Saved recently`; an earlier `Cannot save` state was transient. The remaining uncertainty was whether the available entitlement supported the complete publish-and-run loop.

Requested improvement:

- Provide a hackathon preflight page that verifies tenant, license, Agent Builder, Maestro, Action Center, API workflow, publish, and run permissions.
- Guarantee at least one publish-and-run path for the event duration, or state the missing entitlement before builders start.

## What Worked

- Maestro's case/process model is a strong fit for explicit human approval, exception stages, and recovery loops.
- BPMN, agent tasks, people, APIs, and long-running state form a coherent orchestration model.
- The XML view provides a valuable declarative authoring and diagnostic path.

## Highest-Impact Change

Ship a documented headless publish flow and a first-class generic HTTP task. Together they close the largest gap between coding-agent output and a governed, repeatable Automation Cloud deployment.

## Accuracy Note

This document supersedes the earlier statement that the trial could not save. Save was later observed working. It also deliberately describes generic HTTP as a discoverability gap because the test session did not exhaust every UiPath catalog or custom connector path.
