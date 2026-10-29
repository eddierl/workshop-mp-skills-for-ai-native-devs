# eShop: new features with Matt Pocock's skills

This branch, `mash/part-2-new-features`, is the starting point for Part 2 of the Perth AI workshop on Matt Pocock's skills for AI coding agents. Part 1 runs from `main`.

**Setup guide:** https://perth-ai.github.io/workshop-mp-skills-for-ai-native-devs/ · [skills cheat sheet](https://perth-ai.github.io/workshop-mp-skills-for-ai-native-devs/skills.html) · [slides](https://perth-ai.github.io/workshop-mp-skills-for-ai-native-devs/slides.html)

## The story

In Part 1 you were handed a buggy, vibe-coded online store and triaged it. Those bugs are now fixed, with tests. The client is happy, and now they want new features. Your job is to build one properly: grill the idea, write a spec, break it into tickets, implement it test-first, and get it reviewed and merged.

## Get your own copy

1. Click **Use this template** → **Create a new repository** at the top of this page, and tick **Include all branches**.
2. Clone your new repo and switch to Part 2. Already have a copy from Part 1? Run `git stash -u` and `git fetch` first.

   ```bash
   git switch mash/part-2-new-features
   ```

3. Run `/setup-matt-pocock-skills` in your coding agent. Choose GitHub issues if you're signed in to `gh`, or local files if not.

Your copy has its own issues, and pull requests go into your own `mash/part-2-new-features`.

## Run the app

The full guide is in [`python-eshop/README.md`](python-eshop/README.md). In short, in two terminals:

```bash
cd python-eshop/backend && uv sync && uv run python run.py
cd python-eshop/frontend && npm install && npm run dev
```

Open http://127.0.0.1:4321 and sign in with `demouser@perthai.com.au` / `Pass@word1`.

## Run the tests

```bash
cd python-eshop/backend && uv run pytest
```

## What's here for the review step

- [`AGENTS.md`](AGENTS.md): project context your agent loads every session (Codex, Cursor, Copilot and others read it; `CLAUDE.md` points Claude Code at it).
- [`REVIEW.md`](REVIEW.md): what a reviewer, human or `/code-review`, should care about in this repo.
- [`.github/pull_request_template.md`](.github/pull_request_template.md): every PR says how it was tested, how risky it is and how to revert it.

## Credits

The app comes from Part 1 of this workshop, on `main`, by Rafael Avigad and Raj Saddi. Released under CC0, like the original.
