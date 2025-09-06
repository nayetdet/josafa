import asyncio
import discord
from typing import Optional, Dict, Tuple
from discord import Guild, VoiceClient
from discord.ext import commands

class MusicTask:
    __queues: Dict[int, asyncio.Queue[Tuple[commands.Context, str, str, str]]] = {}
    __tasks: Dict[int, asyncio.Task[None]] = {}

    @classmethod
    async def display(cls, ctx: commands.Context, title: str, thumbnail: str, url: str, on_queue: bool = False) -> None:
        queue_size: int = cls.__queues[ctx.guild.id].qsize()
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
        if guild.id not in cls.__queues:
            cls.__queues[guild.id] = asyncio.Queue()

        await cls.__queues[guild.id].put((ctx, title, thumbnail, url))
        if guild.id not in cls.__tasks or cls.__tasks[guild.id].done():
            cls.__tasks[guild.id] = asyncio.create_task(cls.play(guild))
        await cls.display(ctx, title=title, thumbnail=thumbnail, url=url, on_queue=True)

    @classmethod
    async def remove(cls, guild: Guild) -> None:
        await cls.clear(guild)
        if guild.id in cls.__queues:
            del cls.__queues[guild.id]

        if guild.id in cls.__tasks:
            del cls.__tasks[guild.id]

    @classmethod
    async def play(cls, guild: Guild) -> None:
        queue: asyncio.Queue = cls.__queues[guild.id]
        voice_client: Optional[VoiceClient] = guild.voice_client
        if not voice_client:
            return

        while True:
            ctx, title, thumbnail, url = await queue.get()
            if not voice_client or not voice_client.is_connected():
                queue.task_done()
                await asyncio.sleep(1)
                continue

            voice_client.play(discord.FFmpegPCMAudio(url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"))
            await cls.display(ctx, title=title, thumbnail=thumbnail, url=url, on_queue=False)
            while voice_client.is_playing():
                await asyncio.sleep(1)

            queue.task_done()

    @classmethod
    async def stop(cls, guild: Guild) -> None:
        voice_client: Optional[VoiceClient] = guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()

    @classmethod
    async def clear(cls, guild: Guild) -> None:
        cls.__queues[guild.id] = asyncio.Queue()
        await cls.stop(guild)
