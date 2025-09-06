from typing import Optional
from discord import VoiceClient
from discord.ext import commands
from src.josafa.services.miscellaneous_service import MiscellaneousService
from src.josafa.services.voice_channel_service import VoiceChannelService
from src.josafa.tasks.music_task import MusicTask
from src.josafa.utils.youtube_utils import YoutubeUtils

class MusicService:
    @classmethod
    async def play(cls, ctx: commands.Context, *, arg: str) -> None:
        if not await VoiceChannelService.join(ctx, notify_on_success=False):
            return

        title, thumbnail, url = YoutubeUtils.extract_url(arg)
        await MusicTask.add(ctx, title=title, thumbnail=thumbnail, url=url)
        await MiscellaneousService.react(ctx)

    @classmethod
    async def stop(cls, ctx: commands.Context) -> None:
        voice_client: Optional[VoiceClient] = await VoiceChannelService.ensure_voice(ctx)
        if not voice_client:
            return

        await MiscellaneousService.react(ctx)
        await MusicTask.stop(ctx.guild)

    @classmethod
    async def clear(cls, ctx: commands.Context) -> None:
        voice_client: Optional[VoiceClient] = await VoiceChannelService.ensure_voice(ctx)
        if not voice_client:
            return

        await MiscellaneousService.react(ctx)
        await MusicTask.clear(ctx.guild)
