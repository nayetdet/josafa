from discord.ext import commands
from src.josafa.cogs.events_cog import EventsCog
from src.josafa.cogs.miscellaneous_cog import MiscellaneousCog
from src.josafa.cogs.music_cog import MusicCog
from src.josafa.cogs.voice_channel_cog import VoiceChannelCog

async def register_cogs(bot: commands.Bot):
    await bot.add_cog(EventsCog(bot))
    await bot.add_cog(MiscellaneousCog(bot))
    await bot.add_cog(MusicCog(bot))
    await bot.add_cog(VoiceChannelCog(bot))
