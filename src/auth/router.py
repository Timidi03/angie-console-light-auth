import jwt
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.auth.schemas import User
from src.auth.utils import (
    verify_password,
    get_access_token,
    get_refresh_token,
    validate_access_token,
    update_tokens,
)

router = APIRouter(
    tags=["Auth"],
)


@router.post("/login")
def login(user: User):
    if verify_password(user.email, user.password):
        from src.database import redis

        access_token = get_access_token(user.email)
        refresh_token = get_refresh_token(user.email)
        response = JSONResponse(content={'status': 'OK'})
        response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True)
        redis.set(user.email, refresh_token)
        return response
    response = JSONResponse(content={'status': 'Error'})
    response.set_cookie(key='status', value='Error', httponly=True, secure=True)
    return response


@router.get("/verify-token")
def verify_token(request: Request):
    access_token = request.cookies.get('access_token')
    check = validate_access_token(access_token)
    if check:
        return JSONResponse(content={'status': 'ok'})
    else:
        refresh_token = request.cookies.get('refresh_token')
        new_tokens = update_tokens(access_token, refresh_token)
        if new_tokens:
            response = JSONResponse(content={'status': 'ok'})
            response.set_cookie(key="access_token", value=new_tokens['access_token'], httponly=True, secure=True)
            response.set_cookie(key="refresh_token", value=new_tokens['refresh_token'], httponly=True, secure=True)
            return response
    return JSONResponse(content={'status': 'error'})






