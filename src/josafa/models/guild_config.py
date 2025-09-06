from typing import Optional
from beanie import Document
from src.josafa.config import Config

class GuildConfig(Document):
    guild_id: int
    prefix: Optional[str]

    class Settings:
        name: str = "guild_configs"

    def get_prefix(self) -> str:
        return self.prefix if self.prefix else Config.BOT_DEFAULT_PREFIX
