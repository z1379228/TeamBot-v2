import os
import aiosqlite

DATABASE_PATH = "database/teambot.db"


class Database:

    @staticmethod
    async def initialize():

        # 建立資料夾
        os.makedirs("database", exist_ok=True)
        os.makedirs("images/players", exist_ok=True)
        os.makedirs("images/exports", exist_ok=True)
        os.makedirs("logs", exist_ok=True)

        async with aiosqlite.connect(DATABASE_PATH) as db:

            # 玩家資料
            await db.execute("""
            CREATE TABLE IF NOT EXISTS players(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                discord_id INTEGER UNIQUE NOT NULL,

                username TEXT NOT NULL,

                nickname TEXT NOT NULL,

                avatar TEXT,

                elo INTEGER DEFAULT 1000,

                win INTEGER DEFAULT 0,

                lose INTEGER DEFAULT 0,

                draw INTEGER DEFAULT 0,

                mvp INTEGER DEFAULT 0,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            # 對戰紀錄
            await db.execute("""
            CREATE TABLE IF NOT EXISTS matches(

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                winner_team INTEGER,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)

            await db.commit()

        print("✅ Database initialized")