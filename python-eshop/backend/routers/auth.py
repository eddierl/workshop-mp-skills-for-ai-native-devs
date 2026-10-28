from fastapi import APIRouter, Depends, Header, HTTPException, status

from dependencies import get_auth_service, require_authenticated_user
from models.schemas import AuthResponse, LoginRequest, RegisterRequest
from services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
def register(
    body: RegisterRequest,
    x_basket_id: str | None = Header(default=None),
    service: AuthService = Depends(get_auth_service),
):
    try:
        token, email = service.register(body.email, body.password, x_basket_id)
        return AuthResponse(access_token=token, email=email)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/login", response_model=AuthResponse)
def login(
    body: LoginRequest,
    x_basket_id: str | None = Header(default=None),
    service: AuthService = Depends(get_auth_service),
):
    try:
        token, email = service.login(body.email, body.password, x_basket_id)
        return AuthResponse(access_token=token, email=email)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
