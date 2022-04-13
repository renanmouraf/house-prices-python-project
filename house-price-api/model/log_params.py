from pydantic import BaseModel

class LogParams(BaseModel):
    user_id: int = None
    jwt_token: str
    server: str
    endpoint: str
    search_values: str
    ip: str
    charge: bool