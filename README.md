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

**clone**
git clone https://github.com/<your-username>/schedulingbuddy.git
cd schedulingbuddy

**create & activate venv**
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

**install dependencies**
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

**run**
python main.py


---





The Scheduling Buddy will require:

1. Strong Language and Understanding
   The model will identify tasks, events, dates/times, people, commitments, suggestions buried in chat/emailed text.
2. Good context window
   Email and conversation threads may be monitored across the day. This requires a model that can handle decent history so it doesn't lose earlier context.
3. Prompting and/or fine-tuning and customization
   This will require custom prompts to train this model, such as prompting a meeting request or commitment; extracting event + date/time + participants + location and propose adding to the calendar.

This project may potentially use retrieval-augmented generation (RAG) to pull user-specific data (current calendar, past meeting patterns) so suggestions are relevant.

This will all be a LLM (Large Language Model) simliar to GPT or Gemini.
