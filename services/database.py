from pathlib import Path
import aiosqlite

DATABASE_PATH = Path("database") / "teambot.db"


class Database:

    @staticmethod
    async def initialize():

        DATABASE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        async with aiosqlite.connect(DATABASE_PATH) as db:

            await db.execute("PRAGMA foreign_keys = ON;")

            await db.execute("""
            CREATE TABLE IF NOT EXISTS players(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                discord_id INTEGER UNIQUE NOT NULL,

                username TEXT NOT NULL,

                nickname TEXT NOT NULL,

                avatar TEXT,

                elo INTEGER NOT NULL DEFAULT 1000,

                win INTEGER NOT NULL DEFAULT 0,

                lose INTEGER NOT NULL DEFAULT 0,

                draw INTEGER NOT NULL DEFAULT 0,

                mvp INTEGER NOT NULL DEFAULT 0,

                created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
            )
            """)

            await db.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_players_discord
            ON players(discord_id)
            """)

            await db.commit()

        print("✅ Database initialized")

    @staticmethod
    async def connect():

        db = await aiosqlite.connect(DATABASE_PATH)

        await db.execute("PRAGMA foreign_keys = ON;")

        db.row_factory = aiosqlite.Row

        return db