# eShopOnWeb — Python Tutorial Edition

A first-year-friendly Python rewrite of the eShopOnWeb storefront. It demonstrates a minimal clean architecture:

**Router → Service → Database Client → SQLite**

The React frontend talks to a FastAPI backend over JSON. Scope matches the original storefront: catalog, basket, auth, checkout, and orders — no admin, no payment gateway, no product detail page.

## Architecture

```
python-eshop/
├── backend/
│   ├── routers/      # HTTP layer (FastAPI APIRouter)
│   ├── services/     # Business logic
│   ├── db/           # DatabaseClient + schema + seed
│   └── models/       # Pydantic schemas + dataclasses
└── frontend/         # Vite + React + Tailwind SPA
```

| Python layer | Original C# project | Responsibility |
|---|---|---|
| `routers/` | `Web/` pages & controllers | HTTP, validation, auth headers |
| `services/` | `ApplicationCore/` | Basket merge, checkout rules |
| `db/client.py` | `Infrastructure/` | All SQL queries |
| SQLite file | SQL Server CatalogDb | Persistent storage |

## Prerequisites

- Python 3.11+ (tested with 3.14)
- Node.js 18+

## Quick start

Open two terminals.

### 1. Backend

```powershell
cd python-eshop/backend
py -m pip install -r requirements.txt
py run.py
```

- API: http://127.0.0.1:8765
- Swagger docs: http://127.0.0.1:8765/docs
- Static product images: http://127.0.0.1:8765/static/images/products/

> **Note:** Do not use bare `uvicorn main:app --reload` — that defaults to port 8000, which may already be in use. Always use `py run.py`.

### 2. Frontend

```powershell
cd python-eshop/frontend
npm install
npm run dev
```

- App: http://127.0.0.1:4321

The Vite dev server proxies `/api` and `/static` to the backend.

## Demo account

| Email | Password |
|---|---|
| `demouser@microsoft.com` | `Pass@word1` |

## Shopping flow

1. Browse the catalog — filter by brand/type, paginate (10 items per page)
2. Add items to basket — works anonymously via `X-Basket-Id` stored in `localStorage`
3. Login or register — anonymous basket merges into your account
4. Checkout — review order, click **Pay now** (uses a hardcoded shipping address like the original)
5. View orders — **My Orders** in the header

## API overview

| Method | Route | Auth |
|---|---|---|
| GET | `/api/catalog/items` | Public |
| GET | `/api/catalog/brands` | Public |
| GET | `/api/catalog/types` | Public |
| GET | `/api/basket` | JWT or `X-Basket-Id` |
| POST | `/api/basket/items` | JWT or `X-Basket-Id` |
| PUT | `/api/basket/items` | JWT or `X-Basket-Id` |
| POST | `/api/auth/register` | Public |
| POST | `/api/auth/login` | Public |
| POST | `/api/orders` | JWT required |
| GET | `/api/orders` | JWT required |
| GET | `/api/orders/{id}` | JWT required |

## Teaching notes

- **Start with `routers/catalog.py`** — thinnest layer, easy to read
- **Then `services/basket_service.py`** — shows business rules without SQL
- **Then `db/client.py`** — all database access in one place
- **No ORM** — SQL is explicit so students can see what the database does

## Out of scope

- Admin catalog CRUD (BlazorAdmin / PublicApi)
- Real payment processing
- Account management (2FA, password change)
- Docker / Azure deployment
