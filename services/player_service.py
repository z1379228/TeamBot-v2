from __future__ import annotations

from typing import Optional

from models.player import Player
from services.database import Database


class PlayerService:
    """玩家資料服務"""

    @staticmethod
    async def create_player(
        discord_id: int,
        username: str,
        nickname: str,
        avatar: str | None = None
    ) -> bool:
        """
        建立玩家

        Returns:
            True  建立成功
            False 玩家已存在
        """

        async with await Database.connect() as db:

            cursor = await db.execute(
                """
                SELECT id
                FROM players
                WHERE discord_id = ?
                """,
                (discord_id,)
            )

            if await cursor.fetchone():
                return False

            await db.execute(
                """
                INSERT INTO players
                (
                    discord_id,
                    username,
                    nickname,
                    avatar
                )
                VALUES
                (
                    ?, ?, ?, ?
                )
                """,
                (
                    discord_id,
                    username,
                    nickname,
                    avatar
                )
            )

            await db.commit()

            return True

    @staticmethod
    async def get_player(
        discord_id: int
    ) -> Optional[Player]:
        """取得單一玩家"""

        async with await Database.connect() as db:

            cursor = await db.execute(
                """
                SELECT *
                FROM players
                WHERE discord_id = ?
                """,
                (discord_id,)
            )

            row = await cursor.fetchone()

            if row is None:
                return None

            return Player(
                id=row["id"],
                discord_id=row["discord_id"],
                username=row["username"],
                nickname=row["nickname"],
                avatar=row["avatar"],
                elo=row["elo"],
                win=row["win"],
                lose=row["lose"],
                draw=row["draw"],
                mvp=row["mvp"],
                created_at=row["created_at"]
            )

    @staticmethod
    async def get_all_players() -> list[Player]:
        """取得全部玩家"""

        async with await Database.connect() as db:

            cursor = await db.execute(
                """
                SELECT *
                FROM players
                ORDER BY elo DESC,
                         nickname ASC
                """
            )

            rows = await cursor.fetchall()

            players: list[Player] = []

            for row in rows:

                players.append(
                    Player(
                        id=row["id"],
                        discord_id=row["discord_id"],
                        username=row["username"],
                        nickname=row["nickname"],
                        avatar=row["avatar"],
                        elo=row["elo"],
                        win=row["win"],
                        lose=row["lose"],
                        draw=row["draw"],
                        mvp=row["mvp"],
                        created_at=row["created_at"]
                    )
                )

            return players