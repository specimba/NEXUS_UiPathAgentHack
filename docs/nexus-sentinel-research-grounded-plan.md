# NEXUS Sentinel — Research-Grounded Refinement Plan (from the PAPERS corpus)
_Source: C:\Users\speci.000\Downloads\ARCHIVIST\PAPERS (754 PDFs). Deep dive 2026-06-30._

## Headline
The corpus isn't tangential — it is the **academic backbone of our exact design**. Five papers map 1:1 onto NEXUS Sentinel's pillars, and three of them directly fix the weaknesses my adversarial Level-2 review flagged (weak injection tripwire F7, no privilege/auth F5, verify-linkage F6). This lets us reframe the submission from "a hackathon BPMN" to "a literature-grounded governance pattern" — exactly the depth that survives a hostile judge.

---

## The five load-bearing papers (with how we use each)

### 1. Progent: Securing AI Agents with Privilege Control — UC Berkeley (Dawn Song et al.)
**The single most important find.** Progent represents privilege as a **security policy of symbolic rules over tool calls**, checked by a **deterministic procedure** enforcing least privilege. An LLM proposes policy updates; an **SMT solver classifies each update as a narrowing (applied automatically) or an expansion (requires explicit approval)** — so the agent's action space "can only shrink without approval" (**monotonic confinement**).
→ **This is our governance gate, named and citable.** Our deterministic policy adapter = Progent's deterministic policy check. Our **ALLOW = narrowing (auto), HOLD = expansion (needs human approval), DENY = blocked** maps exactly onto monotonic confinement. *We adopt Progent's vocabulary in the submission and frame our human-approval node as the "expansion requires approval" rule.* Fixes the credibility gap behind F5 (privilege/auth).

### 2. Benchmarking & Defending Against Indirect Prompt Injection (BIPIA) — Microsoft
Finds LLMs universally vulnerable because they **can't separate informational context from actionable instructions**; proposes **boundary awareness** defenses.
→ **Direct fix for F7.** Our injection control is currently a keyword substring tripwire (we flagged it as evadable). We upgrade the narrative (and, time permitting, the adapter) from "keyword match" to **boundary-awareness**: treat evidence fields as *data, never instructions*. Cite BIPIA as the principle.

### 3. INJECAGENT: Benchmarking Indirect Prompt Injections in Tool-Integrated LLM Agents — UIUC
A benchmark of **1,054 test cases**; ReAct GPT-4 is attackable **24%** of the time.
→ **Evidence for "why this matters."** We cite the 24% figure to justify the DENY-on-injection path, and we can sample a handful of INJECAGENT-style payloads as additional adversarial probes against our adapter (extends the live evidence table).

### 4. A Survey of Safety & Trustworthiness of LLMs through Verification & Validation — Huang et al., AI Review 2024
Frames safety as a **lifecycle V&V process** (falsification/evaluation, verification, runtime monitoring).
→ **Backs our verify→closure gate.** We reframe "Verify Recovery" as a **runtime V&V checkpoint**, and our retry-budget loop as bounded falsification before closure. Gives F6 (verify linkage) a principled frame: verification must be tied to the evaluated case.

### 5. Steering LLMs via Scalable Interactive Oversight — Fudan NLP
**Scalable oversight**: decompose intent into low-burden human decisions so humans "responsibly steer AI on tasks that surpass their ability to verify."
→ **Backs the human-approval node AND the one new agentic node.** The "AI Release Manager Approval" is exactly low-burden interactive oversight. The **gated AI Remediation Proposer** (agent drafts, human approves the expansion) is scalable oversight + Progent's monotonic confinement combined.

### Supporting (threat model & governance framing)
- **Agentic AI Security: Threats, Defenses, Evaluation & Open Challenges** (IEEE Access 2026) — taxonomy for our threat/abuse section; "secure-by-design agent systems."
- **LLM in the Middle: Systematic Review of Threats & Mitigations** — lifecycle threat mapping.
- **A Principled Governance for Emerging AI Regimes (China/EU/US)** — regulatory framing for the governance pitch.

---

## UPDATED plan (replaces "deepen" plan with the research-grounded version)

**Thesis (one line for judges):** *"NEXUS Sentinel applies privilege-controlled, monotonic-confinement governance (Progent) with boundary-aware injection defense (BIPIA) and runtime V&V (Huang 2024) to AI-release recovery — orchestrated in UiPath Maestro with scalable human oversight (Fudan)."*

### P0 (do today — now with citations)
- **P0-1 Real adapter binding** — turn the Evaluate/Verify annotations into runtime calls; map `verdict` → gateway. *(Frame: deterministic privilege check, Progent.)*
- **P0-2 Verdict-bound gateways** — DENY→Escalate, HOLD→Approval, ALLOW→Remediation. *(Frame: monotonic confinement — expansion needs approval.)*
- **P0-3 Real human approval** — assignee = `requiredHumanRole`; capture approver+decision+timestamp+auditId. *(Frame: scalable interactive oversight.)*
- **P0-4 One live loop** — fail→re-entry→closure, recorded. *(Frame: runtime V&V + bounded falsification.)*
- **P0-5 Add ONE gated Agentic node** — "AI Remediation Proposer": agent drafts the remediation, but the action space can only shrink without human approval. *(Frame: Progent × Fudan oversight.)*

### P1 (credibility hardening — now literature-backed)
- **P1-1 Boundary-aware injection defense** (BIPIA) replacing the keyword tripwire — even a documented design note counts. Cite INJECAGENT's 24% as motivation.
- **P1-2 Verify→evaluate linkage** as V&V tie-in (Huang 2024).
- **P1-3 Privilege/auth on routes** (Progent least-privilege).
- **P1-4 Extend adversarial evidence** with a few INJECAGENT-style payloads.

### Submission upgrade (free credibility)
Add a **"Research Grounding / Related Work"** section to SUBMISSION.md citing these 5+3 papers. Almost no hackathon team does this; it signals depth and directly answers "is this real or a toy."

---

## What I did NOT recommend (avoid node-bloat)
The corpus also has self-refinement / reasoning-RL papers (DeepSeek-R1, EVOLVE) — interesting but **off-thesis** for a governance submission. Adding ungoverned AI capability would contradict our whole pitch. We stay disciplined: depth at the gate, one justified agentic node, everything cited.
