import os
import aiohttp
import aiofiles
import discord

from config import PLAYER_FOLDER


class ImageService:

    @staticmethod
    async def save_attachment(
        attachment: discord.Attachment,
        discord_id: int
    ) -> str:

        os.makedirs(PLAYER_FOLDER, exist_ok=True)

        ext = attachment.filename.split(".")[-1].lower()

        filename = f"{discord_id}.{ext}"

        filepath = os.path.join(
            PLAYER_FOLDER,
            filename
        )

        await attachment.save(filepath)

        return filepath

    @staticmethod
    async def download_avatar(
        member: discord.Member
    ) -> str:

        os.makedirs(PLAYER_FOLDER, exist_ok=True)

        filename = f"{member.id}.png"

        filepath = os.path.join(
            PLAYER_FOLDER,
            filename
        )

        url = member.display_avatar.url

        async with aiohttp.ClientSession() as session:

            async with session.get(url) as response:

                if response.status == 200:

                    data = await response.read()

                    async with aiofiles.open(filepath, "wb") as f:

                        await f.write(data)

        return filepath

    @staticmethod
    def get_player_image(discord_id: int):

        exts = [
            "png",
            "jpg",
            "jpeg",
            "webp"
        ]

        for ext in exts:

            path = os.path.join(
                PLAYER_FOLDER,
                f"{discord_id}.{ext}"
            )

            if os.path.exists(path):

                return path

        return None