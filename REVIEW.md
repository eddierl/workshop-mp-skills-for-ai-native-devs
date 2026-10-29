# REVIEW.md

What matters when reviewing a change to this repo:

- **Baskets and auth:** a failure is "one shopper can see or change another shopper's basket or orders". Check every new route for who can reach it.
- **Checkout:** a failure is "an order and a basket disagree". Order writes and basket changes must stay in one transaction.
- **Tests:** every behaviour change has a test that would fail without it. No test, no merge.
- **Frontend:** errors must be shown, never disguised as an empty state.
- At most 3 nits per review. Skip `uv.lock`, `package-lock.json` and `static/images`.
- Cite `file:line` for every finding. No findings from names alone.
- Start the summary with a count of findings. If nothing needs fixing, say so.
