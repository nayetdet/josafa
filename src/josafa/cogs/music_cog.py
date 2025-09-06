import logging
from discord.ext import commands
from src.josafa.services.music_service import MusicService

class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("Music Cog has been loaded!")

    @commands.command(aliases=["p"])
    async def play(self, ctx: commands.Context, *, arg: str) -> None:
        await MusicService.play(ctx, arg=arg)

    @commands.command(aliases=["s"])
    async def stop(self, ctx: commands.Context) -> None:
        await MusicService.stop(ctx)

    @commands.command(aliases=["c"])
    async def clear(self, ctx: commands.Context) -> None:
        await MusicService.clear(ctx)
