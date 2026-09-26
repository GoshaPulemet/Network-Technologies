# api.py
from fastapi import FastAPI
from todo import todo_router

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {"message": "Добро пожаловать в мое авторское API для списка задач!"}

app.include_router(todo_router)