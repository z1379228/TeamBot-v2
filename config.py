import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

GUILD_ID = int(os.getenv("GUILD_ID"))

DATABASE = "database/teambot.db"

PLAYER_FOLDER = "images/players"

EXPORT_FOLDER = "images/exports"