# NEXUS Sentinel — "Show the Real Build" Demo Video Plan
_Replaces the dry voiceover-over-static-slides cut. Goal: prove it's real by SHOWING the live system + actual agent workspace, not narrating over nothing._

## Why the change
The committed cut (`assets/video/nexus-sentinel-narration.mp3`, 4:25) has good, honest narration — but the picture shows nothing. Judges reward **evidence on screen**. We already have all the live assets; we just need to film them.

## Assets we already own (recovered from git)
- Narration audio: `assets/video/nexus-sentinel-narration.mp3` (1.59 MB) — reuse as the voice track.
- Captions: `assets/video/nexus-sentinel-captions.srt` / `.vtt` (176 lines, timed) — burn in for accessibility.
- Live endpoint: https://nexus-sentinel-policy-adapter.onrender.com (keep-warm active).
- Full BPMN: uipath/NEXUSSentinelBPMN/Process.bpmn (12 nodes, 15 conditional flows).
- Adapter source + 14 passing tests; the adversarial L2 probe transcript.

## The shot list — each narration beat gets REAL footage behind it
| Time | Narration beat (existing audio) | WHAT TO SHOW on screen (the fix) |
|---|---|---|
| 0:00–0:10 | "NEXUS Sentinel Recovery is a governed AI release incident workflow…" | Title card → hard cut to the **Maestro canvas with the FULL process** (after injection) zoomed to show all branches |
| 0:10–0:35 | "Enterprise AI releases don't fail in one predictable way…" | Slow pan across the BPMN: Verdict gateway → HOLD/ALLOW/DENY arms, the rework loop, escalation arm |
| 0:35–1:05 | Policy verdict / deterministic decision | **Split screen:** terminal firing `curl /api/v1/case/evaluate` LEFT, JSON verdict (ALLOW) returning RIGHT — real, live |
| 1:05–1:35 | Prompt-injection containment → DENY | Terminal sends the injection payload; show **DENY · CRITICAL · SECURITY_INCIDENT_MANAGER · Escalated** appear live |
| 1:35–2:02 | Human approval / HOLD | Maestro **process instance** view: token paused at the AI Release Manager approval task |
| 2:02–2:35 | Verify → second gateway, rework loop | Fire `/verify` fail → show **Rework Required / reentry:Investigation**; then `/verify` pass → **Closure** |
| 2:35–3:05 | Audit / provenance | `GET /api/v1/audit/{id}` returns record with **sha256 fingerprint + UTC + policy_version**; show 404 on missing id |
| 3:05–3:45 | **Where NEXUS expertise lives** | Cut to the **codex/agent workspace**: git log (9 commits), the adapter source, 14 tests passing, the adversarial L2 review doc scrolling |
| 3:45–4:25 | Close: governed AI ops on UiPath | Back to Maestro: re-run one instance end-to-end (ALLOW→remediate→verify→closure), audit id shown. Honest caveat caption: "approval gate now bound (was auto-complete in v1.0.1)." |

## Capture mechanics (fast, no fancy editing)
1. **OBS** (you already run it on port-9222 Chrome) — one scene, 1080p, capture the browser + a terminal window side by side.
2. Record **three raw takes** straight through (canvas pan, live curl probes, agent workspace) — ~5 min of footage total.
3. Drop the existing **narration.mp3** as the audio track; align the 3 takes to the table above (timestamps already match the .srt).
4. Burn in the **.srt** captions. Export. Done.

## Honesty rule (keeps us credible — and is itself feedback-award material)
- Show the live probes actually returning — don't fake JSON.
- One caption disclosing the v1.0.1 cloud gap and that it's now fixed (verdict→gateway bound, real approval) — judges trust teams who show the seam.

## Dependency
This plan's strongest 6 shots need the **full BPMN visible in the cloud Maestro canvas** (the injection). Until that lands, we can still film the live-adapter + agent-workspace shots (3 of 9 beats) immediately.
