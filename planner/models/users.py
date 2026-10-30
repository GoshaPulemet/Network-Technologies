from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

from models.events import Event


class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[Link[Event]]] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "student@mail.com",
                "password": "strong",
                "events": [],
            }
        }
    }

    class Settings:
        name = "users"


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "student@mail.com",
                "password": "strong",
            }
        }
    }