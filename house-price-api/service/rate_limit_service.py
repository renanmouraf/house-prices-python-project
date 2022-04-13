from loguru import logger
from db.security_db import db_total_requests_per_user_per_hour

async def rate_limit_per_user(user_id: int):
    try:
        total_requests = await db_total_requests_per_user_per_hour(user_id)
        if total_requests["count"] > 10000:
            logger.info(f"Too many requests for user with ID: {user_id}")
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)
        logger.error("Error trying to get the total count of requests of the user")
