import os
import discord
import random
from typing import List, Optional
from discord.ext import commands
from src.josafa.repositories.guild_config_repository import GuildConfigRepository

class MiscellaneousService:
    @classmethod
    async def send(cls, ctx: commands.Context, arg: str, delete_after: Optional[int] = None) -> None:
        assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets"))
        images_path: List[str] = [x for x in os.listdir(assets_dir) if x.lower().endswith((".png", ".webp", ".jpg", ".jpeg"))]
        if not images_path:
            return

        image_path: str = random.choice(images_path)
        await ctx.channel.send(
            embed=discord.Embed().set_author(name=arg, icon_url=f"attachment://{image_path}"),
            file=discord.File(os.path.join(assets_dir, image_path), filename=image_path),
            delete_after=delete_after
        )

    @classmethod
    async def react(cls, ctx: commands.Context) -> None:
        await ctx.message.add_reaction("☑")

    @classmethod
    async def help(cls, ctx: commands.Context) -> None:
        prefix: str = ctx.prefix
        embed: discord.Embed = discord.Embed(
            title="🤖 Josafá - Comandos disponíveis",
            description=f"Use `{prefix}help` para ver esta mensagem a qualquer momento."
        )

        embed.add_field(
            name="🎧 Música",
            value=(
                f"`{prefix}play <texto>` — Reproduz sua música\n"
                f"`{prefix}stop` — Para a música atual imediatamente\n"
                f"`{prefix}clear` — Esvazia toda a fila de músicas\n"
            ),
            inline=False
        )

        embed.add_field(
            name="🔊 Canal de Voz",
            value=(
                f"`{prefix}join` — Faz o bot entrar no seu canal de voz\n"
                f"`{prefix}leave` — Remove o bot do canal de voz"
            ),
            inline=False
        )

        embed.add_field(
            name="⚙️ Configurações do Servidor",
            value=(
                f"`{prefix}prefix <prefixo>` — Altera o prefixo do bot neste servidor"
            ),
            inline=False
        )

        embed.set_footer(text="Josafá • Um bot de música bem carequinha ao seu dispor!!!")
        await ctx.send(embed=embed)
        await cls.react(ctx)

    @classmethod
    async def prefix(cls, ctx: commands.Context, *, arg: str) -> None:
        max_len: int = 3
        if not arg or len(arg) > max_len:
            await MiscellaneousService.send(ctx, arg=f"Por favor, insira um prefixo válido (máx. {max_len} caracteres)!")
            return

        if ctx.prefix == arg:
            await MiscellaneousService.send(ctx, arg="Este prefixo já está definido neste servidor!")
            return

        await GuildConfigRepository.update_prefix(ctx.guild.id, arg)
        await cls.react(ctx)
