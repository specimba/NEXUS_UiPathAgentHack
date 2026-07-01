# YouTube Elevator Pitch — NEXUS Sentinel (60-72s replacement video)

Production plan for a short, punchy demo video to link in the Devpost form.
Replaces the longer `agenthack-demo-evidence-narrated.mp4` (too slow for judges).

Live facts used throughout (from the recorded run, case `CASE-2026-9821`):
verdict chain **HOLD → ALLOW → VERIFICATION_FAILED → VERIFICATION_PASSED**, 2.6s total,
audit IDs `350181f…` (HOLD), `e4aa8d3…` (ALLOW), `d7793d2…` (verify failed),
`5edb88f…` (verify passed). GitHub: `github.com/specimba/NEXUS_UiPathAgentHack`.

---

## 1. Title options (3 alternatives)

1. **NEXUS Sentinel: The AI Recovery Gate That Doesn't Guess** (52 chars)
2. **NEXUS Sentinel — Stop, Prove, Recover: AI Release Safety in 60s** (63 chars)
3. **NEXUS Sentinel: We Made AI Failures Replayable, Not Guesswork** (61 chars)

**Pick: Option 1** — shortest, leads with the product name, and "doesn't guess" is a
concrete, curiosity-opening hook that survives mobile truncation.

## 2. Thumbnail concept

- **Subject:** a single terminal window showing the verdict chain frozen mid-run, with
  the four verdicts stacked and color-coded.
- **Text overlay:** **"IT DOESN'T GUESS"** (3 words, huge, top-left).
- **Background:** near-black (#0B0B0F) with the chain in high-contrast — HOLD amber
  (#F5A623), ALLOW green (#2ECC71), FAILED red (#E74C3C), PASSED green (#2ECC71).

Specify: a **still image** (not a frame grab — a clean composited PNG), text overlay
**"IT DOESN'T GUESS"**, palette **black + amber + green + red**.

## 3. Hook (first 3 seconds, mandatory)

- **On-screen text:** `AI just failed. Now what?`
- **Narrator's first sentence:** "Every time an AI system fails, someone guesses at the fix."
- **Why it works:** it names a pain every builder has felt and refuses the usual logo
  intro, so the viewer stays past second three.

## 4. Shot-by-shot script (64 seconds total)

**Shot 1 — Hook**
- **Timestamp:** 0:00-0:03
- **Visual:** black screen, a red "AI FAILED" alert flashes on.
- **On-screen text:** `AI just failed. Now what?`
- **Narration:** "Every time an AI system fails, someone guesses at the fix."

**Shot 2 — Problem framing**
- **Timestamp:** 0:03-0:09
- **Visual:** messy Slack/log montage, fast cuts, a human shrugging.
- **On-screen text:** `Slow. Messy. Unprovable.`
- **Narration:** "Recovery is slow, it's messy, and nobody can prove what happened."

**Shot 3 — The 5-stage loop**
- **Timestamp:** 0:09-0:24
- **Visual:** clean static diagram of the loop (ASCII below), each box lights up in turn.
- **On-screen text:** `One gate. Five steps. Every time.`
- **Narration:** "So we built a gate. It checks, routes, waits for a human, verifies, repeats."

```
  EVALUATE ──▶ ROUTE ──▶ APPROVE ──▶ VERIFY ──▶ CLOSE
     ▲                                   │
     └────────────── REWORK ◀────────────┘
        (failed verification re-enters)
```

**Shot 4 — Live evaluate call**
- **Timestamp:** 0:24-0:33
- **Visual:** terminal, a `curl` POST to `/case/evaluate`, JSON response scrolls in.
- **On-screen text:** `One call in. One verdict out.`
- **Narration:** "Here it runs live — one call in, one clear verdict out."

**Shot 5 — Live verify call**
- **Timestamp:** 0:33-0:42
- **Visual:** terminal, a `curl` POST to `/case/verify`, response shows `verified: false`.
- **On-screen text:** `It's honest when the fix fails.`
- **Narration:** "After the fix, it checks again — and it's honest when the fix fails."

**Shot 6 — The verdict chain**
- **Timestamp:** 0:42-0:54
- **Visual:** four verdicts stack with their audit IDs and timestamps, chain arrow drawn.
- **On-screen text:** `HOLD → ALLOW → FAILED → PASSED`
- **Narration:** "Watch it: HOLD, then ALLOW, verification failed once, passed, case closed."

  On-screen detail to show:
  ```
  HOLD    audit-350181f…   00:04:45
  ALLOW   audit-e4aa8d3…   00:04:46
  FAILED  audit-d7793d2…   00:04:47   (re-enters)
  PASSED  audit-5edb88f…   00:04:47   ✓ closed   — chain integrity: TRUE
  ```

**Shot 7 — Why this matters**
- **Timestamp:** 0:54-1:00
- **Visual:** split screen — "model" greyed out, "typed contract" glowing.
- **On-screen text:** `The model never makes the call.`
- **Narration:** "The model never makes the call — a typed contract does, and it's replayable."

**Shot 8 — What is next + GitHub**
- **Timestamp:** 1:00-1:04
- **Visual:** GitHub URL large on screen over the closed chain.
- **On-screen text:** `github.com/specimba/NEXUS_UiPathAgentHack`
- **Narration:** "Next, we wire it into live approvals. Try it yourself."

## 5. Tools the user needs

- **Screen recorder (free):** OBS Studio — record the terminal shots in 4K, 60fps.
- **Video editor (free):** CapCut — has auto-captions and easy large text overlays.
- **YouTube channel:** the user's existing channel, or a new free one.
- **AI voice (free):** ElevenLabs free tier for the narration, OR record your own voice —
  own voice is warmer and reads as more authentic for a hackathon.

## 6. Step-by-step recording instructions

1. Open OBS Studio → Sources → add "Display Capture" → set canvas to 3840×2160 (4K).
2. In a large-font terminal (18pt+), run the evaluate `curl` from `docs/CANVAS-BINDING-SPEC.md`
   and record ~10 seconds; do a second take for the verify call. (Re-record live rather
   than reusing `agenthack-demo-evidence-narrated.mp4` — you control the pacing and it's
   crisp 4K.) Keep the old MP4 as backup source for shots 4-5 if a live take fails.
3. Stop OBS; the clips save to your OBS video folder.
4. Open CapCut → New Project → drag in the two terminal clips.
5. Build shots 1-3, 6-8 as text-over-color cards: CapCut → Text → "Add default text",
   paste each on-screen caption, set font to bold, size ~120, white on the dark palette.
6. Drop the narration audio (ElevenLabs export or your own recording) onto the audio track;
   nudge each clip so the caption lands with the spoken line.
7. CapCut → Captions → Auto-captions → generate, then correct any wrong words; make sure
   the burned-in text matches Section 7 exactly.
8. Trim the total to 60-72 seconds; confirm the verdict-chain shot (6) is the longest beat.
9. Export at 1080p or 4K, 30fps, MP4.
10. Save the export as `assets/video/yt-elevator-pitch/nexus-sentinel-60s.mp4` for the repo.

## 7. Captions file (SRT-ready)

```
0:00:00,000 --> 0:00:03,000
AI just failed. Now what?

0:00:03,000 --> 0:00:09,000
Recovery is slow, messy, and unprovable.

0:00:09,000 --> 0:00:24,000
One gate. Five steps. Every time.

0:00:24,000 --> 0:00:33,000
One call in. One clear verdict out.

0:00:33,000 --> 0:00:42,000
It's honest when the fix fails.

0:00:42,000 --> 0:00:54,000
HOLD, ALLOW, FAILED, PASSED, closed.

0:00:54,000 --> 0:01:00,000
The model never makes the call.

0:01:00,000 --> 0:01:04,000
github.com/specimba/NEXUS_UiPathAgentHack
```

## 8. YouTube upload checklist

- [ ] **Title set** — "NEXUS Sentinel: The AI Recovery Gate That Doesn't Guess"
- [ ] **Description set** — include GitHub `github.com/specimba/NEXUS_UiPathAgentHack`,
      live URL `https://nexus-sentinel-policy-adapter.onrender.com`, and "Made for UiPath AgentHack"
- [ ] **Tags set** — NEXUS Sentinel, UiPath, BPMN, AI governance, prompt injection
- [ ] **Thumbnail uploaded** — the "IT DOESN'T GUESS" still from Section 2
- [ ] **Visibility: Unlisted** — so the link can go in Devpost before the final public reveal
