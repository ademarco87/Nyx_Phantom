# cogs/admin.py
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OWNER_ID = int(os.getenv("BOT_OWNER_ID"))

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ALLOWED_ROLES = ["Leader", "Militia", "Officer", "Senior Officer", "Council Member"]

    @app_commands.command(name="reload", description="Reload scheduler cog (Owner & Leadership Roles Only)")
    async def reload(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)  # ✅ Correct way to defer

        async def do_reload():
            user_roles = [role.name for role in interaction.user.roles]
            print(f"👤 {interaction.user} roles: {user_roles}")

            if interaction.user.id == OWNER_ID or any(role in self.ALLOWED_ROLES for role in user_roles):
                try:
                    await self.bot.unload_extension("cogs.scheduler")  # ✅ Unload first
                    await self.bot.load_extension("cogs.scheduler")  # ✅ Reload fresh
                    await interaction.followup.send("♻️ Scheduler reloaded successfully!", ephemeral=True)  # ✅ Respond AFTER reload
                    print("✅ Scheduler fully reloaded.")
                except Exception as e:
                    await interaction.followup.send(f"⚠️ Reload failed: {e}", ephemeral=True)
                    print(f"❌ Reload failed: {e}")
            else:
                await interaction.followup.send("❌ You do not have permission to use this command.", ephemeral=True)

        self.bot.loop.create_task(do_reload())  # ✅ Now correctly inside `reload()`

# Function to add the cog
async def setup(bot):
    await bot.add_cog(Admin(bot))
