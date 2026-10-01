from fastapi import APIRouter, Path, HTTPException, status
from model import Todo, TodoItem, TodoItems

todo_router = APIRouter()
todo_list = []

@todo_router.post("/todo", status_code=status.HTTP_201_CREATED)
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {
        "message": "Привет, кодер! Твоя задача успешно добавлена в бэклог."
    }

@todo_router.get("/todo", response_model=TodoItems)
async def retrieve_todo() -> dict:
    return {
        "todos": todo_list
    }

@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., title="ID задачи разработчика")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ошибка 404: Коллега, таска с таким ID не найдена в базе!"
    )

@todo_router.put("/todo/{todo_id}")
async def update_todo(todo_data: TodoItem, todo_id: int = Path(..., title="ID задачи для обновления")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = todo_data.item
            return {
                "message": "Шеф, задача обновлена, продолжаем коммитить!"
            }
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ошибка 404: Не могу обновить. Таски с таким ID не существует."
    )

@todo_router.delete("/todo/{todo_id}")
async def delete_single_todo(todo_id: int) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == todo_id:
            todo_list.pop(index)
            return {
                "message": "Ветка закрыта! Задача успешно удалена."
            }
            
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Ошибка 404: Удалять нечего, такой задачи нет."
    )

@todo_router.delete("/todo")
async def delete_all_todo() -> dict:
    todo_list.clear()
    return {
        "message": "Релиз успешен! Бэклог полностью очищен."
    }