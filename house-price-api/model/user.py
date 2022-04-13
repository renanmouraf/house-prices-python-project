from pydantic import BaseModel
import enum
from fastapi import Query


class Role(str, enum.Enum):
    admin: str = "ADMIN"
    personel: str = "PERSONEL"


class User(BaseModel):
    id: int = None
    username: str = None
    password: str = None
    mail: str = Query(
        ..., regex="^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
    )
    role: Role = None
    first_name: str = None
    last_name: str = None
    address: str = None
    city: str = None
    country: str = None
    postal_code: str = None
    company: str = None
