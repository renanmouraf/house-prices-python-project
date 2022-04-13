from passlib.context import CryptContext
from model.jwt_user import JWTUser
from datetime import datetime, timedelta
from utils.properties import (
    JWT_EXPIRATION_TIME_MINUTES,
    JWT_ALGORITHM,
    JWT_SECRET_KEY
)
from utils.messages import (
    JWT_EXPIRED_MSG,
    JWT_INVALID_MSG,
    JWT_WRONG_ROLE
)
import jwt
from fastapi import Depends, HTTPException
from starlette.requests import Request
from fastapi.security import OAuth2PasswordBearer
import time
from db.security_db import db_check_token_user, db_check_jwt_username
from starlette.status import HTTP_401_UNAUTHORIZED
from loguru import logger


pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/security/token")


def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(e)
        return False

# Authenticate username and password to give JWT token
async def authenticate_users(user: JWTUser):
    potential_users = await db_check_token_user(user)
    is_valid = False
    for db_user in potential_users:
        if verify_password(user.password, db_user["password"]):
            is_valid = True

    if is_valid:
        user.role = "admin"
        return user

    return None

async def authenticate_user(user: JWTUser):
    db_user = await db_check_token_user(user)
    try:
        db_user = db_user[0]
        is_valid = False
        if verify_password(user.password, db_user["password"]):
            is_valid = True

        if is_valid:
            user.role = db_user["role"]
            user.user_id = db_user["id"]
            return user
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    return None

# Create access JWT token
def create_jwt_token(user: JWTUser):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {"user_id": user.user_id, "sub": user.username, "role": user.role, "exp": expiration}
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return jwt_token

async def get_user_id(request: Request):
    jwt_token = request.headers["Authorization"].split("Bearer ")[1]
    user_data: JWTUser = decode_jwt_token(jwt_token)
    return user_data["user_id"]

def decode_jwt_token(token: str) -> JWTUser:
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_data = {
            "user_id": jwt_payload.get("user_id"),
            "username": jwt_payload.get("sub"),
            "role": jwt_payload.get("role"),
            "expiration": jwt_payload.get("exp"),
            }
    except Exception as e:
        logger.error(e)
    return user_data

# Check whether JWT token is correct
async def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            is_valid = await db_check_jwt_username(username)
            if is_valid:
                return True
            else:
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED, detail=JWT_INVALID_MSG
                )
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED, detail=JWT_EXPIRED_MSG
            )
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
