from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config.settings import settings
from models import gather_models


async def init_db() -> None:
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME], document_models=gather_models()
    )
