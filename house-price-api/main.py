from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS, HTTP_200_OK
from db.object_db import db_security
from service.predict_service import HousePriceService
from service.security_service import check_jwt_token, decode_jwt_token
from service.user_logging_service import log_user_history
from service.rate_limit_service import rate_limit_per_user
from apis.security_api import security_api
from utils.properties import TESTING
from model.jwt_user import JWTUser
from datetime import datetime
from loguru import logger
import json


app = FastAPI()

app.include_router(
    security_api,
    prefix="/api/security",
)

model = HousePriceService("static/model.pkl")

@app.get("/api/status")
def root():
    return {"status": "online"}

@app.on_event("startup")
async def init():
    await db_security.connect()

@app.on_event("shutdown")
async def finalize():
    await db_security.disconnect()

@app.post("/api/predict")
async def predict(request: Request, inputs: dict):
    pred = model.predict(inputs)[0]
    await log_user_history(request, "house-api", json.dumps(inputs), charge=True)
    return pred

@app.middleware("http")
async def middleware(request: Request, call_next):
    
    if (not TESTING) and (not any(word in str(request.url) for word in [
    "/api/status",
    "/api/security/status","/api/logging/status", 
    "/api/security/token", "/api/security/token/validate", 
    "/docs", "openapi.json"]) ):
        try:
            jwt_token = request.headers["Authorization"].split("Bearer ")[1]
            is_valid = await check_jwt_token(jwt_token)
        except Exception as e:
            logger.info(e)
            is_valid = False

        if not is_valid:
            return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)

        #control rate limit
        user_data: JWTUser = decode_jwt_token(jwt_token)
        too_many_requests = await rate_limit_per_user(user_data["user_id"])
        if too_many_requests:
            return Response("Too many requests", status_code=HTTP_429_TOO_MANY_REQUESTS)

    response = await call_next(request)
    return response


# Enable frontend requests
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)