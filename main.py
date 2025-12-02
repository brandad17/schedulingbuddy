import os
import spacy
from dotenv import load_dotenv
import discord
from discord.ext import commands
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import dateparser
from datetime import datetime, timedelta
import pytz

# Load the spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'.")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# ---------------------------------------------------
# Load tokens from .env
# ---------------------------------------------------
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in .env")

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

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

# ---------------------------------------------------
# NEW: Title Summarization Function
# ---------------------------------------------------
def summarize_event_title(text: str) -> str:
    """Uses spaCy to find the most relevant noun or verb near the trigger words."""
    doc = nlp(text)
    
    # These are the nouns or verbs we want to capture (e.g., 'call', 'meeting', 'lunch')
    target_nouns = {"meeting", "call", "lunch", "dinner", "appointment", "chat", "project"}
    
    # Default summary if nothing specific is found
    default_summary = "Scheduled Event"

    # 1. Search for a direct target noun
    for token in doc:
        if token.lemma_.lower() in target_nouns:
            # Capitalize the first letter for a clean summary
            return token.text.capitalize()

    # 2. Search for a scheduling verb and its object (fallback for action phrases)
    for token in doc:
        # Check for core verbs like 'schedule' or 'plan'
        if token.lemma_.lower() in {"schedule", "plan", "set"}:
            # Find the direct object (dobj) or a noun phrase following the verb
            for child in token.children:
                # If the child is a noun or a compound noun (like 'project meeting')
                if child.dep_ in ("dobj", "attr", "compound") and child.pos_ in ("NOUN", "VERB"):
                    # Use the noun as the summary
                    return child.text.capitalize()
    
    # 3. If the message was a command, use the first few words
    if text.startswith('!'):
        return text.split()[1].capitalize() if len(text.split()) > 1 else default_summary

    # Return the default if the NLP fails to find a good summary
    return default_summary

# ---------------------------------------------------
# Core Event Creation Logic
# ---------------------------------------------------
async def create_calendar_event(channel, event_text: str):
    """
    Handles the parsing and creation of a Google Calendar event.
    """
    await channel.send("Detected a potential event! Parsing and creating...")

    # --- Generate the Concise Summary ---
    concise_summary = summarize_event_title(event_text)
    
    # Use spaCy to find all DATE and TIME entities in the message
    doc = nlp(event_text)
    
    # AGGRESSIVE PARSING: Concatenate only the entities recognized as time or date
    time_entities = [ent.text for ent in doc.ents if ent.label_ in ("DATE", "TIME")]
    
    if time_entities:
        parsing_string = " ".join(time_entities)
    else:
        # Fallback to the original text (cleaned, if needed)
        parsing_string = event_text
    
    # Get current Eastern Time (EST/EDT)
    eastern = pytz.timezone("America/New_York")
    now_est = datetime.now(eastern)

    # Parse the date/time from text using EST as reference
    parsed_time = dateparser.parse(
        parsing_string, 
        settings={
            'PREFER_DATES_FROM': 'future',
            'RELATIVE_BASE': now_est,
            'TIMEZONE': 'America/New_York',
            'RETURN_AS_TIMEZONE_AWARE': True
        },
        languages=['en']
    )
    
    print(f"DEBUG: Parsing string used: '{parsing_string}'")

    if not parsed_time:
        await channel.send(
            f"❌ Sorry, I couldn't find a valid time in: **{event_text}** (Parsed against: '{parsing_string}')"
        ) 
        return

    # Check for all-day event
    if parsed_time.hour == 0 and parsed_time.minute == 0 and parsed_time.second == 0 and 'hour' not in parsing_string.lower():
        start_date_only = parsed_time.strftime('%Y-%m-%d')
        end_date_only = (parsed_time + timedelta(days=1)).strftime('%Y-%m-%d')
        is_all_day = True
    else:
        start_time = parsed_time.isoformat()
        end_time = (parsed_time + timedelta(hours=1)).isoformat()
        is_all_day = False
    
    try:
        service = get_google_calendar_service()

        if is_all_day:
            event = {
                "summary": concise_summary, # <-- USE CONCISE SUMMARY
                "description": event_text,  # <-- Store full text in description
                "start": {"date": start_date_only},
                "end": {"date": end_date_only},
            }
        else:
            event = {
                "summary": concise_summary, # <-- USE CONCISE SUMMARY
                "description": event_text,  # <-- Store full text in description
                "start": {"dateTime": start_time, "timeZone": "America/New_York"},
                "end": {"dateTime": end_time, "timeZone": "America/New_York"},
            }

        created_event = service.events().insert(calendarId="primary", body=event).execute()

        await channel.send(
            f"✅ Event created!\n**{created_event['summary']}**\nLink: {created_event.get('htmlLink')}"
        )

    except Exception as e:
        await channel.send(f"❌ Error creating event: {e}")


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
# 1. Traditional !schedule command
# ---------------------------------------------------
@bot.command()
async def schedule(ctx, *, text):
    """Creates a calendar event with natural language via command."""
    if not text:
        await ctx.send("Please tell me what to schedule.")
        return
    
    await create_calendar_event(ctx, text)

# ---------------------------------------------------
# 2. AI-like Detection (on_message) - With Debug Prints
# ---------------------------------------------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith(bot.command_prefix):
        print("DEBUG: Processing as command. Stopping NLP check.")
        await bot.process_commands(message) 
        return 

    doc = nlp(message.content)

    schedule_triggers = {"schedule", "meeting", "call", "event", "plan", "set up", "appointment"}

    has_time_entity = any(ent.label_ in ("DATE", "TIME") for ent in doc.ents)
    has_trigger_word = any(token.lemma_.lower() in schedule_triggers for token in doc)
    
    print(f"\nDEBUG: Message received: '{message.content}'")
    print(f"DEBUG: Has Time/Date Entity: {has_time_entity}")
    print(f"DEBUG: Has Trigger Word: {has_trigger_word}")

    if has_time_entity and has_trigger_word:
        print("DEBUG: Both conditions met. Creating event.")
        await create_calendar_event(message.channel, message.content)
    else:
        print("DEBUG: Conditions not met. Ignoring message.")
    

# ---------------------------------------------------
# Start the bot
# ---------------------------------------------------
bot.run(TOKEN)