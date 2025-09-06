from typing import Optional
from src.josafa.models.guild_config import GuildConfig

class GuildConfigRepository:
    @classmethod
    async def get(cls, guild_id: int, auto_create: bool = False) -> Optional[GuildConfig]:
        guild_config: Optional[GuildConfig] = await GuildConfig.find_one(GuildConfig.guild_id == guild_id)
        if auto_create and not guild_config:
            guild_config = GuildConfig(
                guild_id=guild_id,
                prefix=None,
                voice=None
            )

            guild_config = await guild_config.save()
        return guild_config

    @classmethod
    async def update_prefix(cls, guild_id: int, prefix: str) -> Optional[GuildConfig]:
        guild_config: GuildConfig = await cls.get(guild_id, auto_create=True)
        guild_config.prefix = prefix
        return await guild_config.save()

    @classmethod
    async def update_voice(cls, guild_id: int, voice: str) -> Optional[GuildConfig]:
        guild_config: GuildConfig = await cls.get(guild_id, auto_create=True)
        guild_config.voice = voice
        return await guild_config.save()

    @classmethod
    async def delete(cls, guild_id: int) -> None:
        guild_config: Optional[GuildConfig] = await cls.get(guild_id)
        if guild_config:
            await guild_config.delete()
