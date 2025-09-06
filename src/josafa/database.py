from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from src.josafa.models.guild_config import GuildConfig
from src.josafa.config import Config

async def init_mongodb() -> None:
    mongo_uri: str = f"mongodb://{Config.MONGODB_USERNAME}:{Config.MONGODB_PASSWORD}@{Config.MONGODB_HOST}/{Config.MONGODB_DATABASE}?authSource=admin"
    client = AsyncIOMotorClient(mongo_uri)
    await init_beanie(database=client[Config.MONGODB_DATABASE], document_models=[GuildConfig])
