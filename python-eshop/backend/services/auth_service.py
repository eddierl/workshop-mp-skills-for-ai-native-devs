from datetime import datetime, timedelta

import bcrypt
from jose import jwt

from config import settings
from db.client import DatabaseClient
from db.seed import hash_password
from services.basket_service import BasketService


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

        if anonymous_basket_id and anonymous_basket_id != user.email:
            self.basket_service.transfer_basket(anonymous_basket_id, user.email)

        token = self._create_token(user.email)
        return token, user.email

    def login(
        self, email: str, password: str, anonymous_basket_id: str | None = None
    ) -> tuple[str, str]:
        user = self.db.get_user_by_email(email)
        if not user or not self._verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        if anonymous_basket_id and anonymous_basket_id != user.email:
            self.basket_service.transfer_basket(anonymous_basket_id, user.email)

        token = self._create_token(user.email)
        return token, user.email

    def _verify_password(self, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"), password_hash.encode("utf-8")
        )

    def _create_token(self, email: str) -> str:
        expire = timedelta(minutes=settings.jwt_expire_minutes)
        payload = {"sub": email, "exp": datetime.utcnow() + expire}
        return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
