# Slide Deck Outline: NEXUS Sentinel Recovery

Use this slide deck structure to prepare your hackathon presentation.

---

## Slide 1: Title Slide
*   **Slide Title:** NEXUS Sentinel: Governed AI Release Recovery
*   **Subtitle:** Building Safe, Auditable, and Cost-Effective Agentic Workflows
*   **Visual:** Architecture overview icon showing UiPath Cloud linked to NEXUS OS.
*   **Presenter Notes:** Introduce the team and state the core focus: bridging the gap between local AI prototypes and production-grade governed automations.

---

## Slide 2: The Enterprise Agentic Gap
*   **Slide Title:** Why AI Agents Fail in Production
*   **Key Points:**
    *   *Security Risks:* Direct database access leaves systems vulnerable to indirect prompt injections (CSI/ALSB) hidden in user inputs.
    *   *Lack of Control:* Purely autonomous LLM chains make decisions in black-box environments with no human-override gates.
    *   *Auditability Gaps:* Regulated enterprises require strict compliance trails for every model decision.
*   **Visual:** A warning icon next to a list of vulnerabilities.

---

## Slide 3: The Architecture Split
*   **Slide Title:** Control Plane vs. Reasoning Plane
*   **Key Points:**
    *   **Control & Execution Plane (UiPath Automation Cloud):** Runs the BPMN process, verdict gateways, approval step, recovery loop, and deployment trace.
    *   **Reasoning & Governance Plane (NEXUS OS):** Sanitized policy adapter evaluating release safety, model hash validation, and outputting audit fingerprints.
*   **Visual:** Mermaid diagram showing the flow between UiPath Cloud and the Policy Adapter.

---

## Slide 4: Sentinel Recovery Workflow (Track 2)
*   **Slide Title:** Governed AI-Release Recovery Flow
*   **Key Points:**
    *   *Intake & Triage:* Robot ingests the release request; adapter identifies mismatched model hashes and issues a `HOLD` verdict.
    *   *Human-in-the-Loop:* The BPMN flow contains an AI Release Manager Approval user task before remediation.
    *   *Remediation & Loop Recovery:* Robot executes safe rollback. If post-deployment verification fails, the case loops back to Investigation rather than failing silently.
*   **Visual:** Screen capture of the published Maestro BPMN process and Orchestrator trace.

---

## Slide 5: The Coding Agent Synergy
*   **Slide Title:** Built with UiPath for Coding Agents
*   **Key Points:**
    *   Development speed boosted by combining low-code components with specialized coding agents (Codex, Gemini, Kilo Code, and Cline).
    *   Coding agents read codebase schemas to generate contract tests, build JSON-RPC payloads, and scaffold the Fast API service.
    *   Adversarial probes cover instruction/data confusion while preserving two known obfuscation gaps as expected failures.
*   **Visual:** Command line terminal showing the reproduced result: `30 passed, 2 xfailed`.

---

## Slide 6: Business ROI & Production Feasibility
*   **Slide Title:** Value Delivered to the Enterprise
*   **Key Points:**
    *   *Literature-Grounded:* Architecture maps 1:1 onto peer-reviewed research (Progent's monotonic privilege confinement, Microsoft's BIPIA boundary awareness, Huang's safety V&V).
    *   *Bounded execution:* The policy adapter advises; UiPath remains the execution authority.
    *   *Auditability:* Adapter decisions generate a SHA-256 input fingerprint and `audit_id`; durable enterprise storage remains roadmap work.
    *   *Enterprise Feasibility:* Fully decoupled from GPU requirements, allowing immediate, lightweight deployment to standard container services (Docker).
*   **Presenter Notes:** Summarize the submission and wrap up for Q&A.
