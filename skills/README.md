# NEXUS Sentinel — AgentHack Skill Bundle (v1)

Three replayable skills, packaged for distribution to all agents (codex, antigravity/gemini, Claude Code) and any CLI consumer of the SimuLang runtime.

## What's in here
- perform-adversarial-system-review/  — Adversarial L2 review of a governed service/API.
- search-and-synthesize-research-papers/  — Mine a local PDF corpus for project-grounded refinement.
- generate-project-handoff-documentation/  — 12-section handoff doc with owner-assignment and end-state checklist.

Each folder has:
- SKILL.md  — full instructions + parameters (Simular skill-registry format)
- skill.json — parameter schema + runtime metadata

## Install paths
- Simular registry (current user): the skills are already saved there (createSkill). They show up in the user's Available Skills catalog and are usable by that user's agents.
- Simular registry (organization/team): requires an account admin to promote; this bundle is the import payload.
- CLI agents (claude, codex, antigravity): copy each folder's contents into the agent's skills directory (e.g. ~/.claude/skills/, ~/.codex/skills/). They run as plain Markdown + SimuLang JS.
- ZIP upload (one-shot): zip the three folders + this README and use createSkill({skillZipPath: ...}) or the registry's Import flow.

## Safety
All three skills are read-only over project paths. Only the artifacts they produce are written (review doc, abstracts file, handoff doc). They never submit, commit, push, deploy, or change permissions.

## Provenance
Generated 2026-07-01 ~00:14 GMT+3 by Sai (opusmanSEEKv4 verification lane). Three skills were first created via createSkill in this session; this bundle is the distributable artifact.
