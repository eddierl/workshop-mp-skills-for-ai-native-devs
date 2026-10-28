from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import settings
from db.ensure_assets import ensure_product_images
from db.seed import seed_database, sync_picture_uris
from dependencies import get_db, init_dependencies
from routers import auth, basket, catalog, orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_path = str(Path(__file__).parent / settings.database_path)
    init_dependencies(db_path)
    ensure_product_images()
    seed_database(get_db())
    sync_picture_uris(get_db())
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(catalog.router)
app.include_router(basket.router)
app.include_router(auth.router)
app.include_router(orders.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
