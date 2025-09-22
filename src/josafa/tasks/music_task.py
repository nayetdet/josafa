import asyncio
import discord
import logging
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from discord import Guild, VoiceClient
from discord.ext import commands

@dataclass
class MusicTaskData:
    queue: asyncio.Queue[Tuple[commands.Context, str, str, str]]
    task: Optional[asyncio.Task[None]]

class MusicTask:
    __data: Dict[int, MusicTaskData] = {}

    @classmethod
    async def display(cls, ctx: commands.Context, title: str, thumbnail: str, url: str, on_queue: bool = False) -> None:
        data: Optional[MusicTaskData] = cls.__data.get(ctx.guild.id)
        queue_size: int = data.queue.qsize() if data else 0
        embed: discord.Embed = discord.Embed(
            title=title,
            url=url,
            description="🎶 **Tocando agora!**" if not on_queue else f"⏱️ **Adicionada à fila!**\n📌 Posição na fila: {queue_size}",
            color=discord.Color.blurple() if not on_queue else discord.Color.blue()
        )

        embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=f"Pedido por {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @classmethod
    async def add(cls, ctx: commands.Context, title: str, thumbnail: str, url: str) -> None:
        guild: Guild = ctx.guild
        data: MusicTaskData = cls.__data.setdefault(guild.id, MusicTaskData(queue=asyncio.Queue(), task=None))
        await data.queue.put((ctx, title, thumbnail, url))
        if not data.task or data.task.done():
            data.task = asyncio.create_task(cls.play(guild))
        await cls.display(ctx, title=title, thumbnail=thumbnail, url=url, on_queue=True)

    @classmethod
    async def remove(cls, guild: Guild) -> None:
        await cls.clear(guild)
        cls.__data.pop(guild.id, None)

    @classmethod
    async def play(cls, guild: Guild) -> None:
        data: MusicTaskData = cls.__data[guild.id]
        queue: asyncio.Queue = data.queue

        try:
            while True:
                voice_client: Optional[VoiceClient] = guild.voice_client
                if not voice_client:
                    await asyncio.sleep(1)
                    continue

                ctx, title, thumbnail, url = await queue.get()
                try:
                    voice_client.play(
                        discord.FFmpegPCMAudio(
                            url,
                            before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                            options="-filter:a volume=0.1"
                        )
                    )

                    await cls.display(ctx, title=title, thumbnail=thumbnail, url=url, on_queue=False)
                    while voice_client.is_playing():
                        await asyncio.sleep(1)
                except Exception as e: logging.error(f"[MusicTask] Music playback failed: {e}")
                finally: queue.task_done()
        except asyncio.CancelledError as e:
            voice_client: Optional[VoiceClient] = guild.voice_client
            if voice_client and voice_client.is_playing():
                voice_client.stop()

            data.queue = asyncio.Queue()
            data.task = None
            raise e

    @classmethod
    async def stop(cls, guild: Guild) -> None:
        voice_client: Optional[VoiceClient] = guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()

    @classmethod
    async def clear(cls, guild: Guild) -> None:
        if (data := cls.__data.get(guild.id)) and (task := data.task):
            task.cancel()
            try: await task
            except asyncio.CancelledError:
                pass

            data.task = None
        await cls.stop(guild)
