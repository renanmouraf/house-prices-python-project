from fastapi.testclient import TestClient
from main import app
import asyncio
from db.functions_db import execute
from db.object_db import db_security
from service.security_service import hash_password
import pytest

client = TestClient(app)
loop = asyncio.get_event_loop()


@pytest.fixture
def setup_user():
    Helpers.insert_user() #run before the test
    yield #run the test itself
    Helpers.delete_user() #run after the test

@pytest.fixture
def helpers():
    return Helpers

class Helpers:
    @staticmethod
    def insert_user():
        query = """insert into users(username,password, mail) values(:username,:password, :mail)"""
        hashed_password = hash_password("pass2")
        values = {"username": "user2", 
                "password": hashed_password,
                "mail": "user2@email.com"}

        loop.run_until_complete(execute(db_security, query, False, values))

    @staticmethod
    def delete_user():
        query = """delete from users where username = :username"""
        values = {"username": "user2"}

        loop.run_until_complete(execute(db_security, query, False, values))

    @staticmethod
    def get_jwt_token():
        response = client.post("/api/security/token", dict(username="user2", password="pass2"))
        jwt_token = response.json()["access_token"]
        return jwt_token
