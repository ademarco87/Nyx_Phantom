# cogs/scheduler.py
import discord
import asyncio
import schedule
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
SPACE_ID = int(os.getenv("SPACE_ID"))

class Scheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.task = self.bot.loop.create_task(self.scheduler())  # Track the background task
        self.schedule_tasks()

    def cog_unload(self):
        print("🛑 Unloading scheduler... stopping all tasks.")
        schedule.clear()  # ✅ Remove all scheduled jobs
        if hasattr(self, "task") and self.task:
            self.task.cancel()  # ✅ Stop the scheduler loop
            print("✅ Background scheduler task cancelled.")


    def schedule_tasks(self):
        schedule.every().monday.at("09:00").do(lambda: asyncio.create_task(
            self.send_scheduled_message("🚀 Motivation:", "Motivation Monday",
                                        "New week, new goals! Let's get started!",
                                        discord.Color.blue(), "🚀")
        ))

        schedule.every().wednesday.at("08:10").do(lambda: asyncio.create_task(
            self.send_text_with_image("🐱 Good morning Umbra! It's Wednesday, Don't forget to put mustard on the Cat!", "images/CatWed.jpg")
        ))

        schedule.every().thursday.at("08:05").do(lambda: asyncio.create_task(
            self.send_text_with_image("🐱 Good morning Umbra! Today is Thursday, Don't forget to clean the Cat!", "images/CatThursday.jpg")
        ))

        schedule.every().friday.at("15:30").do(lambda: asyncio.create_task(
            self.send_scheduled_message("🎉 Reminder:", "Weekend Countdown",
                                        "The weekend is almost here! Hang in there!",
                                        discord.Color.purple(), "🎉")
        ))

        schedule.every().saturday.at("09:00").do(lambda: asyncio.create_task(
            self.send_scheduled_message("🔥 Fun Reminder:", "Saturday Fun!",
                                        "Enjoy your weekend and take a break!",
                                        discord.Color.red(), "🔥")
        ))

        schedule.every().sunday.at("17:30").do(lambda: asyncio.create_task(
            self.send_scheduled_message("☀️ Reminder:", "Sunday Reminder",
                                        "Good Afternoon! It's Sunday afternoon, make sure to get rest for Monday!",
                                        discord.Color.gold(), "☀️")
        ))

        # SPACE Reminder
        schedule.every().tuesday.at("06:00").do(lambda: asyncio.create_task(
        self.send_space_message(
            "***Incoming Transmission from Squadron HQ, Crimson Hollow***",
            "Happy Chewsday Pilots!",
            "As a reminder, space PvP starts at 10pm GMT (<t:1743957600:R> / <t:1743957600:F>). Prepare to group up and head to Deep Space!",
            discord.Color.dark_red(),
            "<:TieDefender:682583044783341570>",
            "images/abyssal_squadron_banner.jpg"
        )))

        schedule.every().tuesday.at("16:00").do(lambda: asyncio.create_task(
        self.send_space_message(
            "***Incoming Transmission from Squadron HQ, Crimson Hollow***",
            "Chewsday Night Approaches!",
            "Chewsday night Space PvP is about to start! Let's get ready to rumble and meet in Deep Space <t:1743957600:R>.",
            discord.Color.dark_red(),
            "<:TieDefender:682583044783341570>",
            "images/abyssal_squadron_banner.jpg"
        )))

        schedule.every().friday.at("10:00").do(lambda: asyncio.create_task(
        self.send_space_message(
            "***Incoming Transmission from Squadron HQ, Crimson Hollow***",
            "Friday Night Fights!",
            "Good morning Pilots! Friday Night Fights is on. Calling all US Pilots to Deep Space <t:1746838800:R>. Group up and head to Deep Space!",
            discord.Color.dark_red(),
            "<:TieDefender:682583044783341570>",
            "images/abyssal_squadron_banner.jpg"
        )))

        schedule.every().friday.at("19:00").do(lambda: asyncio.create_task(
        self.send_space_message(
            "***Incoming Transmission from Squadron HQ, Crimson Hollow***",
            "Weapons Hot!",
            "Time to stock up on missiles and chaff pilots as Friday Night Fights is kicking off <t:1746838800:R>. Go get 'em!",
            discord.Color.dark_red(),
            "<:TieDefender:682583044783341570>",
            "images/abyssal_squadron_banner.jpg"
        )))


    async def scheduler(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            schedule.run_pending()
            await asyncio.sleep(60)

    async def send_scheduled_message(self, standard_message, title, message, color, emoji):
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(standard_message)
            embed = discord.Embed(title=title, description=message, color=color)
            embed.set_footer(text="📅 Scheduled Notification")
            sent_message = await channel.send(embed=embed)
            await sent_message.add_reaction(emoji)
        else:
            print(f"⚠️ Channel with ID {CHANNEL_ID} not found!")

    async def send_text_with_image(self, text_message, image_path):
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            try:
                await channel.send(text_message, file=discord.File(image_path))
            except Exception as e:
                print(f"⚠️ Error sending image: {e}")
        else:
            print(f"⚠️ Channel with ID {CHANNEL_ID} not found!")

    async def send_space_message(self, standard_message, title, message, color, emoji, image_path):
        channel = self.bot.get_channel(SPACE_ID)
        if channel:
            filename = image_path.split('/')[-1]
            embed = discord.Embed(title=title, description=message, color=color)
            embed.set_footer(text="📅 Scheduled Notification")
            embed.set_image(url=f"attachment://{filename}")
            file = discord.File(image_path, filename=filename)
            sent_message = await channel.send(content=standard_message, embed=embed, file=file)
            await sent_message.add_reaction(emoji)
        else:
            print(f"⚠️ Channel with ID {SPACE_ID} not found!")

async def setup(bot):
    await bot.add_cog(Scheduler(bot))
