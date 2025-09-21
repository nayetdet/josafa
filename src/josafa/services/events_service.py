import asyncio
import discord
import logging
from typing import Optional
from discord import VoiceChannel
from discord.ext import commands
from src.josafa.models.guild_config import GuildConfig
from src.josafa.repositories.guild_config_repository import GuildConfigRepository
from src.josafa.services.miscellaneous_service import MiscellaneousService
from src.josafa.tasks.music_task import MusicTask

class EventsService:
    @classmethod
    async def on_guild_join(cls, guild: discord.Guild) -> None:
        await GuildConfigRepository.get(guild.id, auto_create=True)

    @classmethod
    async def on_guild_remove(cls, guild: discord.Guild) -> None:
        await MusicTask.remove(guild)
        await GuildConfigRepository.delete(guild.id)

    @classmethod
    async def on_message(cls, bot: commands.Bot, message: discord.Message) -> None:
        if message.author.bot:
            return

        if bot.user.mention == message.content.strip():
            guild_config: GuildConfig = await GuildConfigRepository.get(message.guild.id, auto_create=True)
            embed: discord.Embed = discord.Embed(
                title="📑 | Informações do servidor:",
                description=(
                    f"✨ | Prefixo: `{guild_config.get_prefix()}`"
                ),
            )

            embed.set_footer(text=f"ID do servidor: {message.guild.id}")
            embed.timestamp = message.created_at
            await message.channel.send(embed=embed)

    @classmethod
    async def on_voice_state_update(cls, bot: commands.Bot, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
        voice_channel: Optional[VoiceChannel] = after.channel or before.channel
        if not voice_channel:
            return

        if bot.user == member and after.channel != before.channel:
            await MusicTask.clear(voice_channel.guild)

        if bot.user in voice_channel.members:
            for _ in range(60):
                if any(not x.bot for x in voice_channel.members):
                    return
                await asyncio.sleep(1)

            if voice_channel.guild.voice_client:
                await voice_channel.guild.voice_client.disconnect(force=True)

    @classmethod
    async def on_command_error(cls, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            await MiscellaneousService.send(ctx, arg="Por favor, insira um comando válido!")
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await MiscellaneousService.send(ctx, arg="Por favor, passe os argumentos do seu comando corretamente!")
            return

        if isinstance(error, commands.MissingPermissions):
            await MiscellaneousService.send(ctx, arg="Você não tem permissão para usar este comando!")
            return

        logging.error(error)
