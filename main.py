import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ---------------------------------------------------
# Load tokens from .env
# ---------------------------------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# ---------------------------------------------------
# Google API Setup
# ---------------------------------------------------
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_google_calendar_service():
    """
    Loads saved Google credentials or runs OAuth login if needed.
    Returns an authenticated Google Calendar API service object.
    """
    creds = None

    # token.json stores the user's access/refresh tokens
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If no creds or expired, run OAuth login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save creds for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Build Google Calendar API service
    return build("calendar", "v3", credentials=creds)

# ---------------------------------------------------
# Discord Bot Setup
# ---------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Scheduling Buddy is online as {bot.user}")

# ---------------------------------------------------
# !schedule command
# ---------------------------------------------------
@bot.command()
async def schedule(ctx, *, text):
    """
    Creates a calendar event with simple natural language:
    !schedule Lunch tomorrow at noon
    """

    # Basic sanity check
    if not text:
        await ctx.send("Please tell me what to schedule.")
        return

    await ctx.send("Creating your event...")

    try:
        service = get_google_calendar_service()

        # Example: Just set event title to user input
        event = {
            "summary": text,
            "start": {
                "dateTime": "2025-01-01T12:00:00",
                "timeZone": "America/New_York",
            },
            "end": {
                "dateTime": "2025-01-01T13:00:00",
                "timeZone": "America/New_York",
            },
        }

        created_event = service.events().insert(calendarId="primary", body=event).execute()

        await ctx.send(f"Event created!\n**{created_event['summary']}**\nLink: {created_event.get('htmlLink')}")

    except Exception as e:
        await ctx.send(f"Error creating event: {e}")

# ---------------------------------------------------
# Start the bot
# ---------------------------------------------------
bot.run(TOKEN)
