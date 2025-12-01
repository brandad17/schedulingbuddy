# Scheduling Buddy
**Author:** Brandon Morrow  
**Course:** CSI-4130 - Artificial Intelligence  

---

Scheduling Buddy is an AI program that helps you keep schedule throughout the day, reading your messages and emails to ensure your calendar stays up to date with everything you commit to.

**Problem Statement**

People often agree to lunches, dinners, meetings, events, etc. through Discord, but forget to actually add them to their calendar. This leads to chronic forgetfulness and flakiness due to never fully committing to these events.
Scheduling Buddy solves this by turning a simple message like:

**!schedule lunch tomorrow at noon**

into a real Google Calendar event.

**Proposed Method**

- Discord bot listens for !schedule commands

- Natural-language time parsing (dateparser)

- Creates events in Google Calendar API

- Optional OpenAI integration for deeper language understanding

- Google OAuth performs secure account authentication


**Data Sources**

- Discord messages provided by the user as trigger words for SchedulingBuddy to activate
- Google Calendar Events via an API
- OpenAI LLM for advanced parsing

**Project Structure**

```
schedulingbuddy/
├── main.py
├── requirements.txt
├── README.md
├── .env               # DO NOT COMMIT
├── .gitignore
├── credentials.json   # DO NOT COMMIT
└── token.json         # DO NOT COMMIT

```

Users should avoid committing .env, credentials.json, and token.json. These files contain information that should be stored in a safe place, not in a public repo.

# Quick Start Guide

```
# clone
git clone https://github.com/<your-username>/schedulingbuddy.git
cd schedulingbuddy

# create & activate venv
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

# install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# run
python main.py
```

**Setup Instructions:**

## 1) Install Python
- Add Python to PATH

Verify installation:
```
python --version
py -3.11 --version
```

2. Create and activate a virtual environment
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1


(You should now see (venv) in your terminal.)

3. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt


If needed:

python -m pip install discord.py python-dotenv dateparser pytz google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 openai

4. Create your .env file

Create a file named .env in the project root.

DISCORD_TOKEN=your_discord_token_here
OPENAI_API_KEY=your_openai_api_key_here


❗ No quotes
❗ No spaces before or after =
❗ Never commit this file

