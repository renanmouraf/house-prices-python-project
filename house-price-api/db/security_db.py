from click import command
from db.functions_db import execute, fetch
from db.object_db import db_security
from typing import List
from model.user import User

async def db_check_token_user(user: str):
    query = """SELECT * FROM users WHERE username = :username"""
    values = {"username": user.username}
    result = await fetch(db_security, query, False, values)
    if result is None:
        return None
    else:
        return result


async def db_check_jwt_username(username: str):
    query = """SELECT * FROM users WHERE username = :username"""
    values = {"username": username}

    result = await fetch(db_security, query, True, values)
    if result is None:
        return False
    else:
        return True

async def db_insert_user_history(user_id: int, server: str, endpoint: str, search_values: str, ip: str, charge: str):
    command = """INSERT INTO user_history 
    (user_id, server, endpoint, search_values, ip, charge) 
    VALUES (:user_id, :server, :endpoint, :search_values, :ip, :charge)"""

    values = {"user_id": user_id, 
            "server": server,"endpoint": endpoint, 
            "search_values": search_values, "ip": ip,
            "charge": charge}
    
    await execute(db_security, command, False, values)  

async def db_total_requests_per_user_per_hour(user_id: int):
    query="""SELECT COUNT(*) 
            FROM user_history uh 
            WHERE uh.date_time >= NOW() - INTERVAL '1 hour' 
            AND uh.user_id = :user_id
            AND uh.charge = true"""
    
    values = {"user_id": user_id}

    result = await fetch(db_security, query, True, values)
    if result is None:
        return None
    else:
        return result

