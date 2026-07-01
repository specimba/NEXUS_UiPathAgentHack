# Product Feedback — UiPath Maestro (AgentHack submission)

> **Author:** Sai lane, NEXUS Sentinel team. Captured during a 4-hour integration session for the AgentHack hackathon (Track 1: Maestro Case). Concrete, reproducible, with file:line + screenshot refs.

## TL;DR

UiPath Maestro is a credible cloud BPMN platform with strong orchestration primitives, but the **agentic-AI integration path has six concrete friction points** that block serious development. Two of them are P0 (block submission), four are P1 (block adoption).

## P0 — Block submission

### P0-A. BPMN canvas → orchestrator publish gate is opaque to programmatic editing

**What we tried:** Use Autopilot (in-canvas AI assistant) + Playwright to drive the BPMN canvas, fix a 1-issue validation error ("Gateway is superfluous"), then click **Publish**.

**What happened:** Autopilot was able to *add* nodes, but the **Apply changes** action in the canvas toolbar remained disabled while the AI's edits were in flight, and there is **no public API** to commit a BPMN XML diff to a Cloud-hosted designer's "Save" model. The validation panel shows the issue but offers **no in-place fix action** — only the canvas view knows how to resolve it.

**What should be possible:** A `PUT /api/v1/solutions/{id}/files/{fileId}/bpmn` that accepts the validated XML, runs the linter server-side, and returns the resolved diagram. This is the equivalent of the existing "Import XML" tab but in reverse.

**Repro:** In Maestro Designer, add a gateway with one incoming and one outgoing flow. Issue is reported. The user must hand-delete the gateway or hand-add a second source/target. No quick-fix is offered.

### P0-B. Trial-tier save/publish is "best-effort" with silent failures

**What we tried:** Publish a process from Designer to the Orchestrator. Trial-tier showed "Cannot save" intermittently for 4 minutes, then succeeded — but with no clear retry path or status surface.

**What happened:** A trial user has no way to distinguish "save in flight", "save failed", and "save successful but no job in queue" from each other. The only signal is the toast message, which disappears.

**What should be possible:** A persistent **Save status bar** at the bottom of the Designer with the current state machine: `draft → saving → saved → publishing → published → failed_at_step_X`. Each transition is logged with a timestamp.

## P1 — Block adoption

### P1-A. OAuth flow assumes a local browser session

**What we tried:** Publish a process to the Cloud Orchestrator using a headless Python session.

**What happened:** The OAuth flow at `cloud.uipath.com/.../oauth/...` requires an interactive browser session. There is no service-account / API-token flow for trial users. A CLI-based publishing pipeline is effectively impossible without a local Chrome + CDP.

**What should be possible:** A "Service Account" entity in the admin console that owns an API key, with a `scope=maestro:publish` grant. This is the GCP / AWS pattern.

### P1-B. Service Task HTTP binding is schema-opaque

**What we tried:** Configure a Service Task to POST to a typed FastAPI route.

**What happened:** The Service Task's "Request" UI accepts a `Body` field as **opaque text**. There is no JSON-schema-aware validator, no "test request" button against the configured URL, and no preview of the headers. The only way to know the request is malformed is to run the orchestrator job and watch it fail.

**What should be possible:** Paste a sample JSON body; the UI should fetch the target's `openapi.json` and surface a "diff" between the sample and the expected schema, with red-highlighted missing/extra fields. This is the GitHub Actions "request body diff" pattern.

### P1-C. Conditional gateway expressions are unbound at canvas-edit time

**What we tried:** Define a conditional flow on a gateway using a UiPath Expression like `${verdict == 'HOLD'}`.

**What happened:** The canvas does not warn that the variable `verdict` is **not yet defined** in the process. At runtime, the gateway silently evaluates to false for every case — the workflow always takes the default path. This is a class of bug that is **impossible to detect without running a real instance end-to-end**.

**What should be possible:** Lint the canvas at edit time: every `${...}` expression in a condition must reference a variable in scope. Surface unresolved references in the validation panel, in the same way unresolved task references are surfaced today.

### P1-D. No public "instance timeline" replay view

**What we tried:** Run a job end-to-end and capture what happened.

**What happened:** The Orchestrator's instance view shows the current state of the job, but there is **no "replay" or "step-by-step"** UI that walks through each gateway decision, each Service Task call, each audit ID emitted. To debug, the user has to enable tracing and read the raw log.

**What should be possible:** A timeline view that mirrors the BPMN canvas, with each node colored by its outcome (green = passed, red = failed, blue = skipped) and a click-through to the underlying audit record. This is the Temporal UI pattern.

## Cross-cutting observations

- **The product is technically deep but operationally thin.** Every feature has a "this works" demo path and a "this works in production" path, but the gap between them is wider than peers (Temporal, Airflow, Prefect) and is bridged by a manual step somewhere in the middle.
- **Agentic-AI is supported, but in a way that adds risk.** Service Tasks + Connector activities work, but the lack of a typed schema validator at the binding time means agents can inject free-form arguments. We had to **defend against this in our own adapter** (via strict Pydantic with `extra="forbid"`), but the same protection should live in the platform.
- **Autopilot is the most exciting feature.** It is genuinely the path forward for low-code BPMN development. But it is gated behind the very same publish pipeline that is broken (P0-A). Unblocking P0-A also unblocks the Autopilot flywheel.

## Suggested P0 to fix first (highest impact / lowest cost)

- P0-A: `PUT /api/v1/solutions/{id}/files/{fileId}/bpmn` programmatic publish endpoint. (Est. 2 weeks for a single team to ship behind a feature flag.)

## Asks

1. **Public API for Maestro Designer BPMN files** (the P0-A endpoint). This alone unlocks real CI/CD for BPMN.
2. **Persistent save status** in the Designer (the P0-B status bar).
3. **Service-account flow for trial users** (the P1-A scope grant).
4. **Edit-time expression linting** (the P1-C linter).

We are happy to be a reference customer for any of these.