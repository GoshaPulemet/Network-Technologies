from fastapi import APIRouter, Request, Path, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from model import Todo, TodoItem, TodoItems

templates = Jinja2Templates(directory="templates/")

todo_router = APIRouter()
todo_list = []

@todo_router.post("/todo")
async def add_todo(
    request: Request,
    todo: Todo = Depends(Todo.as_form)
):
    todo.id = len(todo_list) + 1
    todo_list.append(todo)

    # ПОПРАВИЛИ СИНТАКСИС ТУТ:
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"todos": todo_list}
    )

@todo_router.get("/todo")
async def retrieve_todo(request: Request):
    # И ТУТ:
    return templates.TemplateResponse(
        request=request,
        name="todo.html",
        context={"todos": todo_list}
    )

@todo_router.get("/todo/{todo_id}")
async def get_single_todo(
    request: Request,
    todo_id: int = Path(..., title="The ID of the todo to retrieve.")
):
    for todo in todo_list:
        if todo.id == todo_id:
            # И ТУТ:
            return templates.TemplateResponse(
                request=request,
                name="todo.html",
                context={"todo": todo}
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist"
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