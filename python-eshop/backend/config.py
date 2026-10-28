from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "eShopOnWeb Python"
    database_path: str = "eshop.db"
    jwt_secret: str = "tutorial-secret-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24
    catalog_page_size: int = 10
    api_host: str = "127.0.0.1"
    api_port: int = 8765
    frontend_port: int = 4321
    cors_origins: list[str] = [
        "http://localhost:4321",
        "http://127.0.0.1:4321",
    ]


settings = Settings()
