import os
from dotenv import load_dotenv
import discord
import re
from dateutil import parser as dateparser  # NEW: natural language datetime parsing


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Discord intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot is online as {client.user}")

@client.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return
    # Detect a natural-language date and time in the user's message
    try:
        dt = dateparser.parse(message.content, fuzzy=True)

        if dt:
            formatted = dt.strftime('%A, %B %d at %I:%M %p')
            response = (
                f"📅 I detected a possible date/time: **{formatted}**.\n"
                "Would you like me to add this to the calendar?"
            )
            await message.channel.send(response)
            return

    except Exception:
        # If the parser can't make sense of the message, just ignore
        pass

    # If nothing useful found, bot stays silent
    return
    # await message.channel.send(f"You said: {message.content}")

client.run(TOKEN)
