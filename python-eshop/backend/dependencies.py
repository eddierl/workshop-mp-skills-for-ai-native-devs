from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt

from config import settings
from db.client import DatabaseClient
from services.auth_service import AuthService
from services.basket_service import BasketService
from services.catalog_service import CatalogService
from services.order_service import OrderService

_db: DatabaseClient | None = None
_basket_service: BasketService | None = None
_catalog_service: CatalogService | None = None
_auth_service: AuthService | None = None
_order_service: OrderService | None = None


def init_dependencies(database_path: str) -> None:
    global _db, _basket_service, _catalog_service, _auth_service, _order_service
    _db = DatabaseClient(database_path)
    _basket_service = BasketService(_db)
    _catalog_service = CatalogService(_db)
    _auth_service = AuthService(_db, _basket_service)
    _order_service = OrderService(_db, _basket_service)


def get_db() -> DatabaseClient:
    assert _db is not None
    return _db


def get_catalog_service() -> CatalogService:
    assert _catalog_service is not None
    return _catalog_service


def get_basket_service() -> BasketService:
    assert _basket_service is not None
    return _basket_service


def get_auth_service() -> AuthService:
    assert _auth_service is not None
    return _auth_service


def get_order_service() -> OrderService:
    assert _order_service is not None
    return _order_service


@dataclass
class Buyer:
    id: str
    is_authenticated: bool


def _decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        email = payload.get("sub")
        return email if isinstance(email, str) else None
    except JWTError:
        return None


def get_current_user_email(
    authorization: str | None = Header(default=None),
) -> str | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.removeprefix("Bearer ").strip()
    return _decode_token(token)


def get_buyer(
    x_basket_id: str | None = Header(default=None),
    user_email: str | None = Depends(get_current_user_email),
) -> Buyer:
    if user_email:
        return Buyer(id=user_email, is_authenticated=True)
    if x_basket_id:
        return Buyer(id=x_basket_id, is_authenticated=False)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="X-Basket-Id header or authentication required",
    )


def require_authenticated_user(
    user_email: str | None = Depends(get_current_user_email),
) -> str:
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )
    return user_email
