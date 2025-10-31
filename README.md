# Scheduling Buddy

Scheduling Buddy is an AI program that helps you keep schedule throughout the day, reading your messages and emails to ensure your calendar stays up to date with everything you commit to.

The Scheduling Buddy will require:

1) Strong Language and Understanding
   The model will identify tasks, events, dates/times, people, commitments, suggestions buried in chat/emailed text.
2) Good context window
   Email and conversation threads may be monitored across the day. This requires a model that can handle decent history so it doesn't lose earlier context.
3) Prompting and/or fine-tuning and customization
   This will require custom prompts to train this model, such as prompting a meeting request or commitment; extracting event + date/time + participants + location and propose adding to the calendar.

This project may potentially use retrieval-augmented generation (RAG) to pull user-specific data (current calendar, past meeting patterns) so suggestions are relevant.

This will all be a LLM (Large Language Model) simliar to GPT or Gemini.
