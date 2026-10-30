from typing import List

from fastapi import APIRouter, HTTPException, status

from database.connection import Database
from models.events import Event, EventCreate, EventOut, EventUpdate

event_router = APIRouter(
    tags=["Events"]
)

# key="number": документы ищутся по порядковому номеру, а не по ObjectId
event_database = Database(Event, key="number")


@event_router.get("/", response_model=List[EventOut])
async def retrieve_all_events() -> List[Event]:
    return await event_database.get_all()


@event_router.get("/{id}", response_model=EventOut)
async def retrieve_event(id: int) -> Event:
    event = await event_database.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return event


@event_router.post("/new")
async def create_event(body: EventCreate) -> dict:
    # следующий номер = максимальный существующий + 1
    last = await Event.find_all().sort("-number").limit(1).to_list()
    number = last[0].number + 1 if last else 1

    event = Event(number=number, task=body.task)
    await event_database.save(event)
    return {
        "message": "Event created successfully",
        "id": number
    }


@event_router.put("/{id}", response_model=EventOut)
async def update_event(id: int, body: EventUpdate) -> Event:
    updated_event = await event_database.update(id, body)
    if not updated_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return updated_event


@event_router.delete("/{id}")
async def delete_event(id: int) -> dict:
    event = await event_database.delete(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )
    return {
        "message": "Event deleted successfully"
    }
