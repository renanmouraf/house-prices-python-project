from loguru import logger
from db.security_db import db_insert_user_history
from service.security_service import decode_jwt_token
from model.jwt_user import JWTUser
from starlette.requests import Request
from model.log_params import LogParams
from utils.string_utils import check_string_empty_or_none

async def log_user_history(request: Request, server: str, search_values: str, charge: bool):
    try:
        jwt_token = request.headers["Authorization"].split("Bearer ")[1]
        user_data: JWTUser = decode_jwt_token(jwt_token)
        params = LogParams(
            user_id=user_data["user_id"],
            jwt_token=jwt_token,
            server=server,
            endpoint=request.url.path, 
            search_values=search_values,
            ip=request.client.host,
            charge=charge)
        await log_user_history_with_params(params)
    except Exception as e: #just log the exception, logging should not break the application
        logger.error(e)
        logger.error("Error trying to log user history")

async def log_user_history_with_params(params: LogParams):
    try:
        if not check_string_empty_or_none(params.user_id):
            user_data: JWTUser = decode_jwt_token(params.jwt_token)
            params.user_id = user_data["user_id"]
        await db_insert_user_history(params.user_id, 
                                    params.server ,params.endpoint, 
                                    params.search_values, params.ip, 
                                    params.charge
                                    )
    except Exception as e:
        logger.error(e)
        logger.error("Error trying to log user history")
