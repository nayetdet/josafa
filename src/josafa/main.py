import asyncio
import discord
import logging
from discord.ext import commands
from src.josafa.cogs import register_cogs
from src.josafa.config import Config
from src.josafa.database import init_mongodb
from src.josafa.models.guild_config import GuildConfig
from src.josafa.repositories.guild_config_repository import GuildConfigRepository

async def get_prefix(_: commands.Bot, message: discord.Message) -> str:
    guild_config: GuildConfig = await GuildConfigRepository.get(message.guild.id, auto_create=True)
    return guild_config.get_prefix()

bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all(), help_command=None)
discord.utils.setup_logging()

@bot.event
async def on_ready() -> None:
    for guild in bot.guilds:
        await GuildConfigRepository.get(guild.id, auto_create=True)

    await bot.tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Leno Brega"))
    logging.info("Josafá started successfully")

async def main() -> None:
    await init_mongodb()
    await register_cogs(bot)
    await bot.start(Config.BOT_DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
