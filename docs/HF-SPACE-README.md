# NEXUS Sentinel — Deterministic Recovery Gate for AI Releases

NEXUS Sentinel is a typed, audit-bound policy gate for AI-release incident recovery,
orchestrated as a UiPath Maestro BPMN process. It is not a demo of a clever interface.
It is a working contract that any reviewer can replay against a live endpoint and get
the same, reconstructible answer.

## The live instance timeline

The clearest way to understand the system is the run we recorded end-to-end against the
public adapter (`https://nexus-sentinel-policy-adapter.onrender.com`). A single case,
`CASE-2026-9821`, was driven through the full loop in **2.641 seconds**, producing the
verdict chain:

`HOLD → ALLOW → VERIFICATION_FAILED → VERIFICATION_PASSED`

Every stage emitted a signed audit record:

1. **Evaluate (HOLD).** Incomplete evidence and a model-echo mismatch produced verdict
   `HOLD`, risk `HIGH`, reason codes `MODEL_ECHO_MISMATCH, EVIDENCE_INCOMPLETE,
   HUMAN_APPROVAL_REQUIRED`, and the required human role `AI_RELEASE_MANAGER`.
   Audit `audit-350181fca5ac25581189`, fingerprint `8818adb2…`.
2. **Evaluate (ALLOW).** With complete evidence and a matching model, the same case
   evaluated to `ALLOW`, risk `LOW`, recommended stage `Remediation`.
   Audit `audit-e4aa8d3bb4ed746965e7`, fingerprint `1ea6204f…`.
3. **Verify (FAILED).** The first verification, carrying the ALLOW evaluation's audit id
   as its `evaluationAuditId`, reported `verified = false` with
   `MODEL_IDENTITY_STILL_MISMATCHED`, recommended stage `Rework Required`, re-entry
   `Investigation`. Verify audit `audit-d7793d20135c19f7bf5d`.
4. **Verify (PASSED).** After rework, verification reported `verified = true`,
   recommended stage `Closure`, no re-entry. Verify audit `audit-5edb88fc62d3e08ac3a2`.

Both verify calls linked back to evaluation `audit-e4aa8d3bb4ed746965e7`, and the
recorder confirmed **audit-chain integrity: True** — every verify's `evaluationAuditId`
resolves to a real evaluation audit for the same case. The full event log is committed
at `artifacts/instance-timeline/` (`instance-1.json`, `instance-1.md`, `SUMMARY.md`).

## The five-stage closed loop

The system is one deterministic decision, repeated with provenance. A request arrives and
is parsed into a strictly-typed envelope; deterministic rule checks — never a model —
produce a verdict of `ALLOW`, `HOLD`, or `DENY`. Maestro routes the case by that verdict:
`ALLOW` executes bounded remediation, `HOLD` routes to a human approver with a defined
role and a typed decision, `DENY` escalates. After execution, the system calls back into
the same gate with a verify request that must carry the prior evaluation's audit id; the
gate either confirms closure or demands rework, and rework re-enters the loop with new
evidence. Nothing runs out of band: recovery is part of the same typed algebra that
authorized the original action.

## Each stage traces to a paper

- **Evaluate — BIPIA (EMNLP 2024).** Gate at the input boundary with a strict allowlist;
  keep the model out of the trust decision.
- **Typed envelopes & tool arguments — INJECAGENT (IEEE S&P 2025).** Strict types at every
  tool boundary, not just the chat layer, so a malformed `remediationId` is rejected on
  the way in.
- **Approve — Fudan oversight framework (2024–2025).** Human approval is a first-class
  policy primitive: a role, a decision enum, and an audit binding — not a button.
- **Verify — Huang et al., V&V for AI-Enabled Systems (NASA/TM, 2023).** Operational
  provenance over statistical metrics: every verdict is reconstructible.
- **Re-evaluate / recovery — Progent (ACL 2024).** Recovery is a first-class operation
  inside a typed, runtime-bounded action algebra, not an out-of-band patch.

## Why a closed loop

The hardest problem in production AI is not making the model act. It is stopping the model
when it shouldn't act, proving that you did, and recovering safely when it does. NEXUS
Sentinel answers that with the smallest possible thing that actually works: a typed
contract with `extra="forbid"` schemas, deterministic verdicts, and a fingerprinted audit
chain that binds every decision to the one before it.

That is what separates this from a slick UI. A judge does not have to trust a screenshot or
a narrated video. They can POST the four sample bodies themselves, read back the same four
audit ids, follow the `evaluationAuditId` links, and confirm the chain closes — in under
three seconds, against a live endpoint, with the model kept entirely out of the trust
decision. The demo is the contract, and the contract is replayable.
