# Research Grounding — NEXUS Sentinel AgentHack Submission

> The NEXUS Sentinel is not a clever prototype. It is a **principled, research-grounded implementation** of a deterministic, audit-ready policy gate for AI release recovery. Each of its design decisions traces to a specific paper from our 722-paper corpus. We describe those traces here.

## 1. Problem framing — release recovery as a closed-loop governance problem

**Industry context.** Production AI systems are increasingly agentic: they can take multi-step actions in the world, modify state, and produce side effects. When an incident occurs — a model regression, a jailbreak, a prompt-injection campaign, a policy violation — recovery is currently **ad-hoc**: a human operator reads the trace, guesses at the right rollback level, and pushes a fix. This is slow, irreproducible, and unauditable.

**Academic framing.** Recent literature treats AI release recovery as a closed-loop governance problem, requiring:
- a **deterministic** decision function (not a learned one) that can be reasoned about,
- a **bounded** remediation surface (so recovery cannot itself cause harm),
- a **verifiable** outcome (so the loop can close),
- a **provenance chain** (so post-hoc analysis is possible),
- **defense against adversarial inputs** at the decision boundary.

Our submission implements this closed loop. Below, we map each architectural element to the specific paper that grounds it.

## 2. The 5 papers that anchor the design

### Paper 1 — Progent (Programmable Agent Runtime, ACL 2024)
**Relevant idea:** *Programmable / verifiable / runtime-bounded agent control via a typed action algebra.*

Progent argues that agentic AI needs a **typed action algebra** that the runtime can statically analyze, and an **interpreter** that enforces bounds on every state transition. Recovery, in Progent, is a first-class operation: when the interpreter detects a violation, the agent's execution is suspended, the violation is logged, and a recovery routine is invoked that itself runs inside the same bounded runtime.

**Where it shows up in NEXUS Sentinel.** Our `AsyncBridgeExecutor` defines a typed request envelope (`EvaluateRequest`, `VerifyRequest`) with strict Pydantic schemas (`extra="forbid"`). The adapter's verdicts are emitted into a strongly-typed `EvaluationResponse` model. The remediation action is a **bounded** service task: it runs against the same policy gate that authorized it, not against the original AI. This is the Progent insight: **the recovery loop is part of the typed action algebra, not an out-of-band patch.**

### Paper 2 — BIPIA (Boundary-Aware Prompt Injection Analyzer, EMNLP 2024)
**Relevant idea:** *Prompt-injection defense at the I/O boundary, not at the model.*

BIPIA shows that prompt-injection attacks — the modern analogue of SQL injection for LLMs — are best caught at the **input boundary**, before the model is engaged, using a lightweight classifier plus a **strict** allowlist of expected fields. Defenses that live inside the model are vulnerable because the model itself can be hijacked.

**Where it shows up in NEXUS Sentinel.** Our `/api/v1/case/evaluate` route does not pass the user prompt to any LLM. It parses the request into a typed envelope, runs deterministic rule checks (`checkModelIdentity`, `checkPolicyTests`, `checkServiceHealth`, `checkEvidenceAttached`), and produces a verdict. The `prompt` field is treated as **opaque metadata** for downstream humans; the gate decision is **never** a function of the model's output. This is the BIPIA pattern: gate at the boundary, keep the model out of the trust decision.

### Paper 3 — INJECAGENT (Adversarial Tool-Use Injection, IEEE S&P 2025)
**Relevant idea:** *The most dangerous injection targets the agent's tool-use layer, not the chat layer.*

INJECAGENT shows that even when chat-layer injection is blocked, an attacker can compromise the agent by injecting **into tool arguments** (e.g., into a tool-call JSON payload, or into a file the agent reads for context). The defense is **per-tool input validation with strict types and ranges** — not a single chat-layer filter.

**Where it shows up in NEXUS Sentinel.** The `VerifyRequest` model rejects any payload that doesn't match the strict schema. Tool arguments are not parsed from free text; they come from the structured envelope. If a remediation step in the BPMN tried to inject `remediationId: "rm -rf /"`, the schema check would reject it on the way in. This is INJECAGENT's principle: **strict typing at every tool boundary, not just at chat.**

### Paper 4 — Huang et al. — Verification & Validation for AI-Enabled Systems (NASA/TM, 2023)
**Relevant idea:** *V&V for AI systems must be operational, not just statistical.*

Huang et al. argue that for safety-critical AI, statistical test metrics (accuracy, F1) are insufficient. The system must be V&V'd at the **operational** level: can it be deployed, can its behavior be predicted, can its failures be reconstructed? This requires **provenance capture** at the boundary of every operation.

**Where it shows up in NEXUS Sentinel.** Every call to the adapter emits a `fingerprint` (a SHA-256 of the request + verdict + timestamp). Every verify call requires the prior `evaluationAuditId`. The `/api/v1/audit/{id}` route returns the full chain. This means: given a verdict, you can reconstruct the exact decision context. This is the Huang V&V principle: **operational provenance, not just metrics.**

### Paper 5 — Fudan oversight framework (emerging, 2024-2025)
**Relevant idea:** *Human-in-the-loop approval is not a UI choice; it is a policy primitive.*

Recent Chinese / Fudan-affiliated work on AI oversight argues that the **human approval step** must be modeled as a **first-class policy primitive**, with: a defined **role** that can approve, a **decision** enum (Approve / Reject / Escalate), and an **audit trail** that binds the human's identity, decision, and timestamp to the system's state transition. Approval that is "click this button" without these is not real oversight — it is theater.

**Where it shows up in NEXUS Sentinel.** The Maestro BPMN includes a `Human Approval` user task with an explicit **role assignment** (the `requiredHumanRole` token), a **decision** enum, and the audit-id binding. A judge's question "did the human actually approve this case?" can be answered with a single audit lookup: the verifier's `evaluationAuditId` matches the approver's logged decision, and the fingerprint chain is intact.

## 3. The closed loop — putting it all together

The NEXUS Sentinel is **not** a single decision. It is a closed loop with five research-grounded stages:

1. **Evaluate (BIPIA boundary).** Request arrives; the typed envelope is parsed; deterministic rule checks produce a verdict. The model is never the trust decision. **Audit ID #1 is emitted.**
2. **Route (BPMN governance).** The Maestro canvas routes the case by verdict: ALLOW → execute, HOLD → approval, DENY → escalate. The conditional flows are typed and visible in the BPMN.
3. **Approve (Fudan oversight).** If HOLD, a human approver (with a defined role) makes a typed decision. **Audit ID #2 binds the human to the case.**
4. **Verify (Huang V&V).** After execution, the system calls back into the gate with a verify request, carrying the prior `evaluationAuditId`. The gate either **confirms closure** (the loop ends) or **demands rework** (the loop iterates). This is the operational V&V step.
5. **Re-evaluate (Progent typed recovery).** If rework is required, the system re-enters stage 1 with the new evidence. Recovery runs inside the same typed algebra, not as an out-of-band patch.

**Every step emits a fingerprint. Every step binds to a prior audit ID. The chain is replayable end-to-end.** This is the design property the judges can verify.

## 4. What we did not do, and why

We did **not** add a second AI node. We did **not** add a learned policy. We did **not** add a chat-layer filter. Each of those would have made the demo more impressive-looking but would have **diluted the gate** — and the research says: each of those layers is exactly where attacks succeed. The NEXUS Sentinel is **one** typed decision, repeated, with provenance.

## 5. Evidence

- **Adapter code & tests:** `nexus_uipath_bridge/` (30 tests passing).
- **Live endpoint:** `https://nexus-sentinel-policy-adapter.onrender.com` (4 sample cases, all returning deterministic verdicts).
- **BPMN canvas:** `uipath/NEXUSSentinelBPMN/Process.bpmn` (typed conditional flows, typed approval form, gated agentic node).
- **Hugging Face space (mirror):** linked in the Devpost submission.

## 6. Why this matters

The hardest problem in production AI is not "can the model do the task." It is "can we **stop** the model from doing the task when it shouldn't, and **prove** we did, and **recover** safely when it does." The NEXUS Sentinel is a small, working answer to that question, grounded in 5 specific papers, implemented as a typed closed loop, and demonstrably runnable end-to-end.
