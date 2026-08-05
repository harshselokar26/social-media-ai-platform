from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
)
from app.schemas.user import UserResponse

from app.services.auth_service import AuthService

from app.exceptions.auth import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)
from app.core.permissions import require_admin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.register(request)

    except EmailAlreadyExistsException:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )


@router.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        return service.login(
            request.email,
            request.password,
        )

    except InvalidCredentialsException:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )


@router.get("/me", response_model=UserResponse)
def me(current_user=Depends(get_current_user)):
    return current_user


@router.get("/admin-test")
def admin_test(current_user=Depends(require_admin)):
    return {"message": "admin access granted", "user": current_user.name}