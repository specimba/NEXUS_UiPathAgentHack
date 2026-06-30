---
name: Search and synthesize research papers
description: Ground a project in a local research-paper corpus: inventory the PDFs, theme-keyword match filenames against the project's pillars/gaps, extract abstracts (pymupdf, UTF-8-safe), confirm theme/paper selection via a decision yield, and return structured per-theme abstracts so the agent can write a grounded refinement/related-work synthesis. Read-only over the corpus.
---

## When to use
Use when the user has a local corpus of papers (PDFs) and wants to mine it for ideas that improve a specific project — e.g. "check our papers database and see what we can do," "find related work for X," "ground our design in the literature."

## What it does
1. Inventory the corpus (file counts, extensions, subfolders).
2. Theme-match filenames against a themes map (theme → keyword regex) tuned to the project's pillars and gaps.
3. Decision yield — confirms/refines theme list and which papers to extract.
4. Extract abstracts via pymupdf (fitz), writing to a UTF-8 file (avoids Windows cp1252 crashes).
5. Return structured perTheme data so the agent writes the synthesis narrative.

## Parameters
papersDir, projectContext, themesJson (optional override), topPerTheme, toolsDir, outputDir.

## Driving the replay
At the decision yield: confirm or refine per-theme filename matches. On completed: write the grounded synthesis from perTheme abstracts.

## Notes
Read-only. Requires Python with pymupdf.
