# Antigravity/Gemini handoff — YouTube video for NEXUS Sentinel AgentHack

> **Read time:** 4 min. **Time to execute:** 30-45 min. **End deliverable:** one public YouTube URL the user pastes into the Devpost form.

## Why you are reading this

The user (Canberk) is racing the 06:00 GMT+3 deadline. The Devpost form is mostly filled, but the **Video demo link** field requires a valid YouTube URL. We (the Claude Code lane) have just produced `assets/video/yt-elevator-pitch/PLAN.md` — a shot-by-shot script for a 60-72 second replacement video. Your job is to **execute that plan**: record, edit, caption, upload to YouTube, and return the URL to the user.

## What you have

- **PLAN.md** at `assets/video/yt-elevator-pitch/PLAN.md` — the script, titles, captions, tools, and recording steps.
- **Existing demo footage** at `assets/video/agenthack-demo-evidence-narrated.mp4` — you can pull clips from this for shots 4-5 (the live curl calls).
- **Live adapter** at `https://nexus-sentinel-policy-adapter.onrender.com` — for re-recording the curl shots if you want crisper 4K.
- **Live instance evidence** at `artifacts/instance-timeline/SUMMARY.md` — for the verdict-chain visual at shot 6.
- **GitHub repo:** github.com/specimba/NEXUS_UiPathAgentHack (for shot 8's URL).

## What you do

1. **Open PLAN.md** and read the 8-shot script.
2. **Record the live demo shots** (4, 5) in 1080p using OBS Studio. For each:
   - Open a terminal.
   - Run the 4 sample curl calls (samples/01..04.json) against the live adapter.
   - Capture both the request and response.
3. **Edit the video in CapCut** (free, has auto-captions):
   - Cut to the 8 shots in order, total 60-72 seconds.
   - Burn in the captions from PLAN.md's SRT section.
   - Add the verdict-chain visual at shot 6 (can be a screenshot of SUMMARY.md or a re-render).
4. **Record the voiceover** (ElevenLabs free tier or your own voice). Keep it conversational — the plan gives the exact wording per shot.
5. **Export** as 1080p MP4, h.264, < 100 MB.
6. **Upload to YouTube** (unlisted):
   - Title: use option 1 from PLAN.md (the most clickable).
   - Description: include the GitHub URL, the live URL, the 5-paper reference list, and "Made for UiPath AgentHack 2026".
   - Tags: NEXUS Sentinel, UiPath, BPMN, AI governance, prompt injection, audit chain.
   - Thumbnail: use the concept from PLAN.md §2.
7. **Hand back to user:** the YouTube URL, plus a 1-line note ("uploaded unlisted, ready to paste into Devpost").

## What you do NOT do

- Do not edit the Devpost form. The user handles that.
- Do not touch the BPMN canvas. The Opus lane owns that.
- Do not push any commits. The Claude Code lane handles git.
- Do not run any tests. The tests are green (30 passing).
- Do not write any new docs. The docs are done (RESEARCH-GROUNDING, PRODUCT-FEEDBACK, SUBMISSION, JUDGE_QA, TWEET-THREAD).

## If you get stuck

- OBS Studio won't record: try Windows Game Bar (Win+G).
- CapCut auto-captions are wrong: manually type the captions from PLAN.md's SRT section.
- ElevenLabs quota is exhausted: record the voiceover on your phone, import to CapCut.
- YouTube upload fails: save the MP4 to assets/video/yt-elevator-pitch/final.mp4 and report the file path — the user can upload from their own channel.

## End state

A YouTube URL like `https://youtu.be/XXXXX` that the user pastes into the Devpost Video demo link field. That's the entire task.