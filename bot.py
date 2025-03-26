# bot.py
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Required for role checks

class NyxBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension("cogs.admin")
        await self.load_extension("cogs.scheduler")
        print("✅ All cogs loaded.")

bot = NyxBot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    await bot.tree.sync()

bot.run(TOKEN)
