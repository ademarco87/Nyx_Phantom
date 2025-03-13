import discord
from discord import app_commands
from discord.ext import commands
import importlib
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OWNER_ID = int(os.getenv("BOT_OWNER_ID"))  # Get the owner ID securely from .env

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Define allowed roles
    ALLOWED_ROLES = ["Leader", "Militia", "Officer", "Senior Officer", "Council Member"]

    @app_commands.command(name="reload", description="Reload bot modules (Owner & Leadership Roles Only)")
    async def reload(self, interaction: discord.Interaction):
        # Check if user is the bot owner OR has an allowed role
        user_roles = [role.name for role in interaction.user.roles]
        if interaction.user.id == OWNER_ID or any(role in self.ALLOWED_ROLES for role in user_roles):
            try:
                # Reload the bot dynamically
                module_name = "bot"  # Assuming bot.py is the main bot file
                if module_name in sys.modules:
                    importlib.reload(sys.modules[module_name])

                await interaction.response.send_message("♻️ Bot reloaded successfully!", ephemeral=True)
            except Exception as e:
                await interaction.response.send_message(f"⚠️ Reload failed: {e}", ephemeral=True)
        else:
            await interaction.response.send_message("❌ You do not have permission to use this command.", ephemeral=True)

# Function to load this cog
async def setup(bot):
    await bot.add_cog(Admin(bot))
