from typing import Optional

from beanie import Document, Indexed
from pydantic import BaseModel


class Event(Document):
    # Порядковый номер (1, 2, 3...) — по нему работают маршруты.
    # Внутренний _id (ObjectId) MongoDB создаёт сам, наружу мы его не отдаём.
    number: Indexed(int, unique=True)
    task: str

    class Settings:
        name = "events"


class EventCreate(BaseModel):
    """Тело запроса POST /event/new (номер присваивается сервером)."""
    task: str

    model_config = {
        "json_schema_extra": {
            "example": {"task": "FastAPI Book Launch"}
        }
    }


class EventOut(BaseModel):
    """Что возвращаем клиенту: только номер и задача."""
    number: int
    task: str

    model_config = {"from_attributes": True}


class EventUpdate(BaseModel):
    task: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "example": {"task": "Новое описание задачи"}
        }
    }
