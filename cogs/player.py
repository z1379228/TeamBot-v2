import discord
from discord import app_commands
from discord.ext import commands

from services.player_service import PlayerService
from views.player_modal import PlayerModal


class Player(commands.GroupCog, group_name="player"):
    """玩家管理"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="add",
        description="新增玩家"
    )
    async def add(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        image: discord.Attachment | None = None
    ):
        """新增玩家"""

        await interaction.response.send_modal(
            PlayerModal(member, image)
        )

    @app_commands.command(
        name="list",
        description="查看所有玩家"
    )
    async def list(
        self,
        interaction: discord.Interaction
    ):

        players = await PlayerService.get_all_players()

        if len(players) == 0:

            await interaction.response.send_message(
                "目前沒有任何玩家。",
                ephemeral=True
            )

            return

        embed = discord.Embed(
            title="👥 玩家列表",
            description=f"共有 **{len(players)}** 位玩家",
            color=discord.Color.blue()
        )

        for player in players:

            embed.add_field(
                name=player.nickname,
                value=(
                    f"🎯 ELO：{player.elo}\n"
                    f"🏆 勝場：{player.win}\n"
                    f"❌ 敗場：{player.lose}\n"
                    f"⭐ MVP：{player.mvp}"
                ),
                inline=False
            )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="profile",
        description="查看玩家資料"
    )
    async def profile(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        player = await PlayerService.get_player(member.id)

        if player is None:

            await interaction.response.send_message(
                "找不到這位玩家。",
                ephemeral=True
            )

            return

        embed = discord.Embed(
            title=f"{player.nickname} 的資料",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Discord",
            value=member.mention,
            inline=False
        )

        embed.add_field(
            name="ELO",
            value=str(player.elo),
            inline=True
        )

        embed.add_field(
            name="勝",
            value=str(player.win),
            inline=True
        )

        embed.add_field(
            name="敗",
            value=str(player.lose),
            inline=True
        )

        embed.add_field(
            name="平",
            value=str(player.draw),
            inline=True
        )

        embed.add_field(
            name="MVP",
            value=str(player.mvp),
            inline=True
        )

        embed.set_thumbnail(
            url=member.display_avatar.url
        )

        await interaction.response.send_message(
            embed=embed
        )

    @app_commands.command(
        name="remove",
        description="刪除玩家"
    )
    async def remove(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ):

        player = await PlayerService.get_player(member.id)

        if player is None:

            await interaction.response.send_message(
                "找不到這位玩家。",
                ephemeral=True
            )

            return

        await PlayerService.delete_player(member.id)

        await interaction.response.send_message(
            f"✅ 已刪除玩家 **{player.nickname}**。"
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Player(bot))