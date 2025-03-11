import discord
import os
import asyncio
import schedule
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# Set up bot with correct intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix="!", intents=intents)

# Function to send an embedded message
async def send_scheduled_message(standard_message, title, message, color, emoji):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # Send the standard message first
        await channel.send(standard_message)

        # Create an embed message
        embed = discord.Embed(
            title=title,
            description=message,
            color=color
        )
        embed.set_footer(text="📅 Scheduled Notification")

        # Send the embed message
        sent_message = await channel.send(embed=embed)

        # React with the specified emoji
        await sent_message.add_reaction(emoji)
    else:
        print(f"⚠️ Channel with ID {CHANNEL_ID} not found!")

# Function to send a normal text message with an image
async def send_text_with_image(text_message, image_path):
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            # Send text message with image
            await channel.send(text_message, file=discord.File(image_path))

        except Exception as e:
            print(f"⚠️ Error sending image: {e}")
    else:
        print(f"⚠️ Channel with ID {CHANNEL_ID} not found!")

# Schedule messages on specific days/times
def schedule_tasks():
    # Standard Embedded Messages
    schedule.every().sunday.at("22:26").do(lambda: asyncio.create_task(
        send_scheduled_message("☀️ Reminder:", "Sunday Reminder",
                               "Good Afternoon! It's Sunday afternoon, make sure to get rest for Monday!",
                               discord.Color.gold(), "☀️")
    ))

    schedule.every().friday.at("17:30").do(lambda: asyncio.create_task(
        send_scheduled_message("🎉 Reminder:", "Weekend Countdown",
                               "The weekend is almost here! Hang in there!",
                               discord.Color.purple(), "🎉")
    ))

    schedule.every().monday.at("09:00").do(lambda: asyncio.create_task(
        send_scheduled_message("🚀 Motivation:", "Motivation Monday",
                               "New week, new goals! Let's get started!",
                               discord.Color.blue(), "🚀")
    ))

    schedule.every().saturday.at("18:00").do(lambda: asyncio.create_task(
        send_scheduled_message("🔥 Fun Reminder:", "Saturday Fun!",
                               "Enjoy your weekend and take a break!",
                               discord.Color.red(), "🔥")
    ))

    # Mustard the Cat (Text + Image, No Embed)
    # Mustard Cat Wednesday
    schedule.every().wednesday.at("08:10").do(lambda: asyncio.create_task(
         send_text_with_image("🐱 Good morning Umbra! It's Wednesday, Don't forget to put mustard the Cat!", "CatWed.jpg")
    ))

    # Clean the damn Cat
    schedule.every().thursday.at("08:05").do(lambda: asyncio.create_task(
        send_text_with_image("🐱 Good morning Umbra! Today is Thursday, Don't forget to clean the Cat!", "CatThursday.jpg")
    ))

# Background task to run the scheduler
async def scheduler():
    while True:
        schedule.run_pending()
        await asyncio.sleep(60)  # Check every minute

# Combined on_ready() function
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    # Send startup message
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        print(f"✅ Found channel: {channel.name} ({CHANNEL_ID})")
        await channel.send("🚀 Hello! I am **Nyx_Phantom**, your dedicated event notifier! I'm now online and ready to keep Umbra informed about all upcoming events. Stay tuned for updates!")
    else:
        print(f"⚠️ Channel with ID {CHANNEL_ID} not found!")

    # Start scheduling tasks
    schedule_tasks()
    bot.loop.create_task(scheduler())  # Start the scheduler

# Run bot
bot.run(TOKEN)
