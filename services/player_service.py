import aiosqlite

from config import DATABASE
from models.player import Player


class PlayerService:

    @staticmethod
    async def create_player(
        discord_id: int,
        username: str,
        nickname: str,
        avatar: str | None = None
    ) -> bool:

        async with aiosqlite.connect(DATABASE) as db:

            cursor = await db.execute(
                "SELECT id FROM players WHERE discord_id=?",
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
                VALUES (?, ?, ?, ?)
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
    async def get_player(discord_id: int) -> Player | None:

        async with aiosqlite.connect(DATABASE) as db:

            cursor = await db.execute(
                """
                SELECT
                    id,
                    discord_id,
                    username,
                    nickname,
                    avatar,
                    elo,
                    win,
                    lose,
                    draw,
                    mvp
                FROM players
                WHERE discord_id=?
                """,
                (discord_id,)
            )

            row = await cursor.fetchone()

            if row is None:
                return None

            return Player(*row)

    @staticmethod
    async def get_all_players() -> list[Player]:

        async with aiosqlite.connect(DATABASE) as db:

            cursor = await db.execute(
                """
                SELECT
                    id,
                    discord_id,
                    username,
                    nickname,
                    avatar,
                    elo,
                    win,
                    lose,
                    draw,
                    mvp
                FROM players
                ORDER BY elo DESC
                """
            )

            rows = await cursor.fetchall()

            return [Player(*row) for row in rows]

    @staticmethod
    async def delete_player(discord_id: int):

        async with aiosqlite.connect(DATABASE) as db:

            await db.execute(
                "DELETE FROM players WHERE discord_id=?",
                (discord_id,)
            )

            await db.commit()

    @staticmethod
    async def update_avatar(
        discord_id: int,
        avatar: str
    ):

        async with aiosqlite.connect(DATABASE) as db:

            await db.execute(
                """
                UPDATE players
                SET avatar=?
                WHERE discord_id=?
                """,
                (
                    avatar,
                    discord_id
                )
            )

            await db.commit()

    @staticmethod
    async def update_elo(
        discord_id: int,
        elo: int
    ):

        async with aiosqlite.connect(DATABASE) as db:

            await db.execute(
                """
                UPDATE players
                SET elo=?
                WHERE discord_id=?
                """,
                (
                    elo,
                    discord_id
                )
            )

            await db.commit()