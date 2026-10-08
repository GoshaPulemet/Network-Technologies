from pydantic import BaseModel
from typing import List
from fastapi import Form

class TodoItem(BaseModel):
    item: str

    

    class Config:
        schema_extra = {
            "example": {
                "item": "Пофиксить критический баг на проде"
            }
        }

class Todo(BaseModel):
    id: int
    item: str

    @classmethod
    def as_form(cls, item: str = Form(...)):
        return cls(id=0, item=item)
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "item": "Написать юнит-тесты для контроллера"
            }
        }

class TodoItems(BaseModel):
    todos: List[TodoItem]

    class Config:
        schema_extra = {
            "example": {
                "todos": [
                    {"item": "Настроить CI/CD пайплайн"},
                    {"item": "Обновить документацию API"}
                ]
            }
        }