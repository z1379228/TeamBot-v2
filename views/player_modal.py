import discord

from services.player_service import PlayerService
from services.image import ImageService


class PlayerModal(discord.ui.Modal, title="新增玩家"):

    def __init__(
        self,
        member: discord.Member,
        image: discord.Attachment | None = None
    ):
        super().__init__()

        self.member = member
        self.image = image

        self.nickname = discord.ui.TextInput(
            label="遊戲暱稱",
            placeholder="請輸入玩家名稱",
            required=True,
            max_length=32
        )

        self.add_item(self.nickname)

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        avatar_path = None

        if self.image:
            avatar_path = await ImageService.save_attachment(
                self.image,
                self.member.id
            )
        else:
            avatar_path = await ImageService.download_avatar(
                self.member
            )

        success = await PlayerService.create_player(
            discord_id=self.member.id,
            username=self.member.name,
            nickname=str(self.nickname),
            avatar=avatar_path
        )

        if not success:

            await interaction.response.send_message(
                "❌ 此玩家已存在。",
                ephemeral=True
            )

            return

        embed = discord.Embed(
            title="✅ 玩家新增成功",
            color=discord.Color.green()
        )

        embed.add_field(
            name="Discord",
            value=self.member.mention,
            inline=False
        )

        embed.add_field(
            name="遊戲名稱",
            value=str(self.nickname),
            inline=False
        )

        embed.add_field(
            name="初始 ELO",
            value="1000",
            inline=False
        )

        embed.set_thumbnail(
            url=self.member.display_avatar.url
        )

        await interaction.response.send_message(
            embed=embed
        )