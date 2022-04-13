from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import RedirectResponse
from utils.messages import TOKEN_INVALID_CREDENTIALS_MSG
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from service.security_service import authenticate_user, create_jwt_token, check_jwt_token
from model.jwt_user import JWTUser
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import Request, status
from loguru import logger
import os


security_api = APIRouter()

@security_api.get("/status",
description="returns 'OK' if the API is up and running")
async def health_check():
    return {"OK"}

@security_api.post("/token",
description="It checks username and password if they are true, it returns JWT token to you.", 
summary="It returns JWT token.")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user = JWTUser(username= form_data.username, password= form_data.password)
    user = await authenticate_user(jwt_user)

    if user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=TOKEN_INVALID_CREDENTIALS_MSG
        )

    jwt_token = create_jwt_token(user)
    return {"username": user.username, "roles": user.role, "access_token": jwt_token}

@security_api.post("/token/validate",
description="Validate Token",
summary="Checks if the token is Valid")
async def validate_token(token: str = Body(..., embed=True)):
    try:
        is_valid = await check_jwt_token(token)
        if is_valid == True:
            return {"valid": "true"}
        else:
            return {"valid": "false"}

    except Exception as e:
        logger.error(e)
        return {"valid": "false"}
