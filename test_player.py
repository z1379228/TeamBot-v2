import asyncio

from services.database import Database
from services.player_service import PlayerService


async def main():

    # 初始化資料庫
    await Database.initialize()

    # 建立玩家
    success = await PlayerService.create_player(
        discord_id=123456789,
        username="TestUser",
        nickname="測試玩家"
    )

    print("建立玩家：", success)

    # 查詢玩家
    player = await PlayerService.get_player(
        123456789
    )

    print(player)

    # 查詢全部玩家
    players = await PlayerService.get_all_players()

    print(players)


asyncio.run(main())