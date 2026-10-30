from typing import Any, List, Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from models.events import Event
from models.users import User


class Settings(BaseSettings):
    DATABASE_URL: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")

    async def initialize_database(self):
        client = AsyncIOMotorClient(self.DATABASE_URL)
        await init_beanie(
            database=client.get_default_database(),
            document_models=[Event, User],
        )


class Database:
    def __init__(self, model, key: Optional[str] = None):
        # key — имя поля для поиска (например "number").
        # Если не задан, поиск идёт по обычному _id (ObjectId).
        self.model = model
        self.key = key

    async def _find(self, id: Any) -> Any:
        if self.key:
            return await self.model.find_one({self.key: id})
        return await self.model.get(id)

    async def save(self, document) -> None:
        await document.create()

    async def get(self, id: Any) -> Any:
        doc = await self._find(id)
        if doc:
            return doc
        return False

    async def get_all(self) -> List[Any]:
        return await self.model.find_all().to_list()

    async def update(self, id: Any, body: BaseModel) -> Any:
        doc = await self._find(id)
        if not doc:
            return False
        fields = body.model_dump(exclude_none=True)
        if fields:
            await doc.update({"$set": fields})
        return doc

    async def delete(self, id: Any) -> bool:
        doc = await self._find(id)
        if not doc:
            return False
        await doc.delete()
        return True
