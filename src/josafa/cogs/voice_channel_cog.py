import logging
from discord.ext import commands
from src.josafa.services.voice_channel_service import VoiceChannelService

class VoiceChannelCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("Voice Channel Cog has been loaded!")

    @commands.command(aliases=["j"])
    async def join(self, ctx: commands.Context) -> None:
        await VoiceChannelService.join(ctx)

    @commands.command(aliases=["l"])
    async def leave(self, ctx: commands.Context) -> None:
        await VoiceChannelService.leave(ctx)
