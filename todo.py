# todo.py
from fastapi import APIRouter, Path
from model import Todo

todo_router = APIRouter()
todo_list = []

@todo_router.post("/todo")
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {"message": "Отлично! Ваша новая задача успешно добавлена."}

@todo_router.get("/todo")
async def retrieve_todos() -> dict:
    return {"todos": todo_list}

@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., title="Идентификатор задачи, которую нужно получить.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}
    return {"message": f"Увы, задача с ID {todo_id} не найдена в вашем списке."}

@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: Todo, todo_id: int = Path(...)) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.id = todo_data.id
            todo.item = todo_data.item
            return {"message": "Ваша задача успешно обновлена!"}
    return {"message": "Задача для обновления не найдена."}

@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int = Path(...)) -> dict:
    for index in range(len(todo_list)):
        if todo_list[index].id == todo_id:
            todo_list.pop(index)
            return {"message": "Задача успешно удалена из вашего списка!"}
    return {"message": "Задача для удаления не найдена."}