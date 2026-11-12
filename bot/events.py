
from pathlib import Path

import discord
from discord.ext import commands

from config import (
    ALLOWED_IMAGE_EXTENSIONS,
    FAT_CHECK_CHANNEL_ID,
    MAX_IMAGE_SIZE_BYTES,
    MAX_IMAGE_SIZE_MB,
)


class MessageEvents(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Ignore bots and messages outside servers
        if message.author.bot or message.guild is None:
            return

        # Only watch the configured channel
        if message.channel.id != FAT_CHECK_CHANNEL_ID:
            return

        if not message.attachments:
            return

        valid_images = []

        for attachment in message.attachments:
            extension = Path(attachment.filename).suffix.lower()

            if extension not in ALLOWED_IMAGE_EXTENSIONS:
                await message.reply(
                    "Please upload a JPG, JPEG, PNG, or WEBP image."
                )
                return

            if attachment.size > MAX_IMAGE_SIZE_BYTES:
                await message.reply(
                    f"That image is too large. The limit is {MAX_IMAGE_SIZE_MB} MB."
                )
                return

            valid_images.append(attachment)

        if valid_images:
            await message.reply(
                "Image received! Image processing will be added in a later step."
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(MessageEvents(bot))
