# Skills for AI-Native Devs

A Perth AI Club workshop on using structured skills — rather than unstructured prompting — to work productively and safely in an unfamiliar, AI-generated codebase.

## Scenario

Our client runs a legacy (C#) online store they built a decade ago. They're commercial people, not engineers — but they'd heard about vibe coding, knew a bit of Python, and used it to build a modern Python alternative to their legacy shop. It looked fine at first, but it's turned out to be pretty buggy.

They won't rewrite from scratch — they've already invested in custom styling and don't want to lose it. They've brought us in to fix the bugs and to set up a workflow that lets them keep using AI, with more guardrails and a better chance of success.

The buggy Python storefront lives in [`python-eshop/`](python-eshop/README.md).

## Workshop Overview

The session opens with a warm-up poll on the room's experience with AI coding, agents, and skills, followed by the scenario above. Attendees then discuss why they think the vibe coding went wrong and how they'd approach it — before we introduce Matt Pocock's skills for Claude Code, what they help with, and where the gaps still are.

The practical component follows:

1. **Set up the skills** — install a small, focused shortlist rather than the full set, and understand what setup actually did.
2. **Triage a bug** — pick a bug from the storefront and work it through a triage skill, with a discussion on harnesses and scaling.
3. **Implement the fix** — build the fix and push it to a branch.
4. **Discuss and reflect** — what the skills caught, where they got in the way, and what to change next time.

Attendees who finish early are encouraged to explore further skills and capabilities on their own.

See the [workshop folder](workshop/README.md) for the detailed facilitator run sheet and [slides](workshop/presentation.html).
