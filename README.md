# Jarvis AI Assistant

A Python voice assistant that recognizes speech, opens selected websites and
local apps, reports the time and date, reads news headlines, and answers other
questions with the OpenAI API.

## Setup

Requires Python 3. Install the packages used by the project:

```bash
python -m pip install SpeechRecognition PyAudio pyttsx3 requests openai gTTS pygame
```

Set API keys in environment variables before starting the assistant:

- `OPENAI_API_KEY` for AI responses.
- `NEWSAPI_API_KEY` for news headlines.

Do not put API keys in source files or commit them to GitHub.

For example, in PowerShell:

```powershell
$env:OPENAI_API_KEY = "your-key"
$env:NEWSAPI_API_KEY = "your-key"
python jarvis.py
```

The assistant needs microphone access and an internet connection for speech
recognition, text-to-speech, news, and AI responses.

## Safety

Shutdown, restart, and log-off commands require you to type an exact
confirmation into the console. Spoken words alone cannot trigger those actions.
