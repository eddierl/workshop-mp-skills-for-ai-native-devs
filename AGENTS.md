# eShop: Perth AI workshop, Part 2

A small online store used for the Perth AI "Matt Pocock skills" workshop. The bugs from Part 1 are fixed; Part 2 is about adding features with a disciplined workflow.

## Stack

- `python-eshop/backend`: FastAPI + SQLite, layered as Router → Service → DB client (`db/client.py` holds all SQL).
- `python-eshop/frontend`: React + Vite + Tailwind, talking to the backend over JSON via `src/api/client.js`.

## Commands

- Backend: `cd python-eshop/backend && uv sync && uv run python run.py` (port 8765)
- Frontend: `cd python-eshop/frontend && npm install && npm run dev` (port 4321)
- Tests: `cd python-eshop/backend && uv run pytest`

## Conventions

- Every behaviour change lands with a backend test in `python-eshop/backend/tests/`. Use the `client` fixture; it runs the API against a throwaway database.
- Keep HTTP concerns in `routers/`, rules in `services/`, SQL in `db/client.py`.
- Anonymous baskets are keyed by a UUID, signed-in baskets by email. Never let one address the other.
- Store times as timezone-aware UTC.
- Show evidence: run the tests and paste the output before saying something works.

## Non-goals

No payment gateway, admin area or real shipping address. Keep changes small enough to review in one sitting.
