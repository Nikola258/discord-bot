
import discord
from discord.ext import commands

from config import DISCORD_TOKEN


class FatCheckerBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("bot.events")


intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True

bot = FatCheckerBot(
    command_prefix="!",
    intents=intents,
)


@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")
    print(f"Bot ID: {bot.user.id}")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
