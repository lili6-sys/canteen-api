from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.security import create_access_token, verify_password
from app.users import get_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", summary="Đăng nhập, nhận access token")
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user(form.username)
    if user is None or not verify_password(form.password,
                                           user["password_hash"]):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Sai tên đăng nhập hoặc mật khẩu",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(user["username"], user["role"])
    return {"access_token": token, "token_type": "bearer"}
