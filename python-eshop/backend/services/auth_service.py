from datetime import datetime, timedelta, timezone

from jose import jwt

from config import settings
from db.client import DatabaseClient
from services.basket_service import BasketService, parse_anonymous_basket_id
from services.passwords import hash_password, verify_password


class AuthService:
    def __init__(self, db: DatabaseClient, basket_service: BasketService):
        self.db = db
        self.basket_service = basket_service

    def register(
        self, email: str, password: str, anonymous_basket_id: str | None = None
    ) -> tuple[str, str]:
        existing = self.db.get_user_by_email(email)
        if existing:
            raise ValueError("Email already registered")

        user = self.db.create_user(email, hash_password(password))

        self._merge_anonymous_basket(anonymous_basket_id, user.email)

        token = self._create_token(user.email)
        return token, user.email

    def login(
        self, email: str, password: str, anonymous_basket_id: str | None = None
    ) -> tuple[str, str]:
        user = self.db.get_user_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        self._merge_anonymous_basket(anonymous_basket_id, user.email)

        token = self._create_token(user.email)
        return token, user.email

    def _merge_anonymous_basket(self, anonymous_basket_id: str | None, email: str) -> None:
        if not anonymous_basket_id:
            return
        anonymous_id = parse_anonymous_basket_id(anonymous_basket_id)
        if anonymous_id is not None:
            self.basket_service.transfer_basket(anonymous_id, email)

    def _create_token(self, email: str) -> str:
        expire = timedelta(minutes=settings.jwt_expire_minutes)
        payload = {"sub": email, "exp": datetime.now(timezone.utc) + expire}
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
