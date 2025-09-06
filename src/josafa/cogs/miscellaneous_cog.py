import logging
from discord.ext import commands
from src.josafa.services.miscellaneous_service import MiscellaneousService

class MiscellaneousCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logging.info("Miscellaneous Cog has been loaded!")

    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        await MiscellaneousService.help(ctx)

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def prefix(self, ctx: commands.Context, *, arg: str) -> None:
        await MiscellaneousService.prefix(ctx, arg=arg)
