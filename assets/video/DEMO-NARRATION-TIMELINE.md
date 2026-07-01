# Demo Narration Timeline — NEXUS Sentinel

Spine: the live instance run (`CASE-2026-9821`, verdict chain
`HOLD → ALLOW → VERIFICATION_FAILED → VERIFICATION_PASSED`, 2.641 s, audit-chain
integrity True). Re-mix over the existing narration MP3 — do not regenerate audio.

---

**0:00 — Title + problem framing**
*Viewer sees:* the NEXUS Sentinel title card over the Maestro BPMN canvas.
*Narrator:* "When an AI release goes wrong, recovery today is ad-hoc — a human reads the
trace and guesses at a fix. NEXUS Sentinel replaces that with a typed, audit-bound policy
gate. Everything you're about to see is a live contract, not a mockup."

**0:30 — The closed loop**
*Viewer sees:* the five-stage loop highlighted on the canvas — Evaluate, Route, Approve,
Verify, Re-evaluate.
*Narrator:* "The gate makes one deterministic decision — ALLOW, HOLD, or DENY — and
repeats it with provenance. The model never makes the trust decision; strict rule checks
do. Maestro routes each case by verdict and closes the loop only when verification passes."

**1:00 — The four audit IDs**
*Viewer sees:* the `instance-1.md` timeline, four audit records scrolling.
*Narrator:* "Here's a real run. The first evaluate returns HOLD — audit
`350181f…` — flagging a model mismatch and incomplete evidence. The second returns ALLOW —
audit `e4aa8d3…`. Then two verify calls: the first fails — audit `d7793d2…` — and the
second passes — audit `5edb88f…`. Four decisions, four signed records."

**1:30 — Fail and re-entry**
*Viewer sees:* stage 3, `verified = false`, recommended stage `Rework Required`, re-entry
`Investigation`.
*Narrator:* "This is the part most demos skip. The first verification fails on
`MODEL_IDENTITY_STILL_MISMATCHED` and the case re-enters investigation. Recovery isn't an
out-of-band patch — it runs back through the same typed gate that authorized the action."

**2:00 — Audit-chain integrity**
*Viewer sees:* `SUMMARY.md` with "Integrity OK: True" and both verify links resolving to
`e4aa8d3…`.
*Narrator:* "Every verify call carries the prior evaluation's audit id, and the recorder
confirms the chain: integrity, True. Given any verdict, you can reconstruct the exact
decision context. This is operational provenance — the whole loop is replayable end to
end, in under three seconds."

**2:30 — Research grounding + close**
*Viewer sees:* the five-paper mapping card (Progent, BIPIA, INJECAGENT, Huang V&V, Fudan).
*Narrator:* "Each stage traces to a specific paper — boundary defense, typed tool
arguments, first-class human approval, operational V&V, and typed recovery. NEXUS Sentinel
is one gate, repeated, with proof. Don't take our word for it — POST the four samples and
read back the same four audit ids."
