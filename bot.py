import discord
from discord.ext import commands

import config
from services.database import Database


class TeamBot(commands.Bot):
    def __init__(self):

        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):

        # 初始化資料庫
        await Database.initialize()

        # 載入所有 Cog
        extensions = [
            "cogs.player",
            "cogs.team",
            "cogs.rank",
            "cogs.admin"
        ]

        for extension in extensions:
            try:
                await self.load_extension(extension)
                print(f"✅ 已載入 {extension}")
            except Exception as e:
                print(f"❌ 載入失敗 {extension}")
                print(e)

        # 同步 Slash Commands
        await self.tree.sync()

        print("✅ Slash Commands 已同步")

    async def on_ready(self):

        print("--------------------------")
        print(f"登入成功：{self.user}")
        print(f"Bot ID：{self.user.id}")
        print("--------------------------")


bot = TeamBot()

bot.run(config.TOKEN)