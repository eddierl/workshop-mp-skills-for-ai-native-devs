# Facilitator Guide

Detailed run sheet for the workshop summarised in the [top-level README](../README.md). Pair this with [presentation.html](presentation.html), which carries the slides for each segment below.

## Suggested pacing

The session runs 2.5–3 hours end to end, including the practical exercise. Segments are listed in order; adjust the practical steps to the time remaining rather than rushing the discussion segments.

## 1. Warm-up

Poll the room (via Particify or similar) on their current experience with AI coding tools, agents, and skills — comfort level, what they've tried, and any concerns. Keep this live and visible; it sets the baseline for the "what went wrong" discussion later and gives you a read on the room's skill level.

## 2. Introduce the scenario

Walk through the [scenario](../README.md#scenario): a non-technical client vibe-coded a Python rewrite of their legacy C# store, it mostly works, but it's buggy, and they want it fixed without a rewrite.

Open the app locally (see the [python-eshop README](../python-eshop/README.md)) and let attendees click through the shopping flow so the scenario is concrete before the discussion.

## 3. Retro: what went wrong

Poll the room again: why do they think the vibe coding went wrong, and how would they have approached it differently? Let a few people share before moving on — this discussion is what makes the skills pitch land in the next segment.

## 4. Introduce the skills approach

Introduce Matt Pocock's skill set for Claude Code and how it addresses the failure modes just discussed — structured workflows instead of unstructured prompting — as well as where it still falls short (it doesn't replace understanding the codebase or good judgement about scope).

Cover, at a minimum:

- **Ask Matt** — a routing skill that points you to whichever skill fits your situation.
- **Grill with Docs** *(recommended for every attendee)* — a structured interview that sharpens a plan or design and produces artifacts (ADRs, a glossary) as it goes. It's worth treating as close to mandatory: it forces attendees to understand the codebase before touching it, and everyone leaves with a real artifact rather than just a demo.
- Two or three more selected from **Triage**, **Wayfinder**, **Code Review**, **Implement**, and **Prototype**, depending on room size and time. Don't attempt a tour of the full skill set — going deep on a handful beats a shallow pass over many.

## 5. Practical component

### Step 1 — Set up the skills

Attendees install the skills selected in segment 4. Have them discuss or write down (time permitting) what the setup actually did — the goal is that they understand what got installed, not that they just followed steps blindly.

Open the TOML header of a couple of skills together and use it to explain:

- Skills run manually, not automatically — the model chooses to invoke them, or the attendee does.
- Skills are an augmentation on top of the model, not a replacement for it.
- Skills load progressively (the header first, full instructions only when invoked), which is why context management matters when composing several of them.

### Step 2 — Triage a bug

Attendees pick a bug from the client's app and work it through a triage skill. Use this segment to discuss harnesses and scaling — how the same workflow holds up whether you're fixing one bug or working through a backlog.

### Step 3 — Implement the fix

Attendees implement the fix and push it to a branch, using the skills set up in Step 1 (e.g. an implement/code-review skill for the build-and-check loop).

### Step 4 — Discuss and reflect

Close the practical component with a group discussion: what did the skills catch that plain prompting wouldn't have, where did they get in the way, and what would attendees change about their setup going forward.

## 6. Beyond today

If time remains, point attendees at other skills worth exploring on their own — for example Grill with Docs' broader family, Teach, and Wayfinder — and encourage them to keep experimenting after the workshop.
