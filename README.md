# SerenityCoach – Mental Health Companion (CLI)

SerenityCoach is a CLI-based AI companion that supports mental wellbeing through empathetic conversation and personalized micro‑actions. It offers two modes:

- Motivation mode: generates a motivational quote and actionable suggestion tailored to your mood.
- Live chat mode: a concise, supportive conversation where the assistant responds directly to your inputs, with optional brief clarifications and practical tips.

Built as part of learning GenAI agent design, SerenityCoach is engineered like a production prototype with structured prompting, safety checks, and clean ergonomics for developers and recruiters.

---

### Highlights

- Industry‑style CLI agent with clear entrypoints and separation of concerns.
- Robust prompt design for concise, on‑topic, non‑clinical guidance.
- Live multi‑turn chat with risk‑phrase detection and safe escalation guidance.
- Environment‑driven config (no API key prompts) and reproducible setup.
- Extendable architecture for additional tools (journaling, reminders, RAG, etc.).

---

## 🚀 Quick Start Guide

## Features

- Motivation Mode

  - Asks for mood and a few optional context signals (energy, stress, sleep, hobbies, time available)
  - Returns structured JSON (mood, quote, author, suggested_action)
  - Adds hobby‑aligned suggestions, micro‑challenges, and an optional clean joke
  - Saves last output to `last_output.json`

- Live Chat Mode (`--chat`)

  - Direct, concise replies (2–4 short sentences)
  - Avoids questions unless a single clarification improves usefulness
  - Provides small, practical coping strategies (breathing, grounding, journaling)
  - Simple risk detection for self‑harm phrases; responds with empathy and encourages reaching out to trusted support and local helplines

- Safety & Ethics
  - No diagnosis or medical advice
  - Trauma‑informed tone; validation first, tips second
  - Gentle safety note if stress ≥ 8

---

## Architecture Overview

- Entrypoint: `main.py`
- Core flows:
  - Prompt construction for motivation mode with structured JSON output
  - Live chat prompt for concise, on‑topic replies (configurable behavior)
- API Integration: Google Generative Language API (Gemini)
- Configuration: `.env` with `GOOGLE_API_KEY`; `python-dotenv` for loading
- Utilities: token usage logging, simple risk‑keyword detection, local fallbacks for jokes and hobby tips

---

## Installation

### Prerequisites

- Python 3.10+
- Google Generative Language API key (Gemini)

### Setup

1. Clone the repository
2. Create `.env` in the project root:
   ```bash
   GOOGLE_API_KEY=your_api_key_here
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Motivation Mode (Interactive)

```bash
python main.py
```

- Provides a motivational quote, suggested action, optional hobby tip, micro‑challenge, and joke (if requested)

Non‑interactive with mood:

```bash
python main.py --mood "tired"
```

### Live Chat Mode

```bash
python main.py --chat
```

- Type your message, press Enter
- Quit with `exit`

### Environment Variable (alternative to .env)

```bash
# Windows PowerShell
set GOOGLE_API_KEY=your_api_key_here

# macOS/Linux
export GOOGLE_API_KEY="your_api_key_here"
```

---

## Configuration

- `--temperature`, `--top_k`, `--top_p`: tune model generation
- `--mood`: bypass mood prompt in motivation mode
- `--chat`: start live chat mode

---

## Prompting Strategy

- Motivation mode: returns strict JSON (`mood`, `quote`, `author`, `suggested_action`) with optional fields (`joke`, `hobby_suggestion`, `challenge`, `affirmation`, `breathing_exercise`, `grounding_exercise`, `resources`).
- Live chat: directive to answer directly, avoid unnecessary follow‑ups, keep it concise and non‑clinical, surface practical tips when appropriate, add empathetic crisis guidance on risk signals.

---

## Safety Considerations

- No diagnosis/medical advice
- Encourages reaching out to trusted people or professional helplines when risk is detected
- Configurable risk keyword list in `main.py`

---

## Roadmap

- Journaling and mood tracking (local storage + insights)
- RAG over curated coping strategies and crisis resources
- Scheduler for micro‑actions/reminders
- Optional TTS/voice and GUI front‑end

---

## 🚀 Features & Concepts Implemented

### ✅ 1. Prompting

The agent prompts the user:

> "How are you feeling today?"

It uses structured prompts (RFTC) to ensure tone, format, and context are appropriate for delivering supportive motivation.

### ✅ 2. Retrieval-Augmented Generation (RAG)

Instead of relying solely on model memory, the bot retrieves relevant quotes from a local or vector database based on the user's input mood (e.g., "tired", "anxious", "lost").

### ✅ 3. Structured Output

The agent formats its response as structured JSON:

```json
{
  "mood": "tired",
  "quote": "Rest if you must, but don’t you quit.",
  "author": "Unknown",
  "suggested_action": "Take a short walk and hydrate."
}
```

### ✅ 4. Function Calling

The agent uses function calling to trigger post-processing actions like:

Saving the quote to a local file

(Later) Emailing the quote to the user via external API

### 🧪 Tech Stack

Language: Python (CLI-based)

LLM Integration: `Google Studio API` for prompting and generation

Planned Additions: Email reminders, calendar integration, quote history

---

## Final Notes

This project shows how AI can responsibly support mental health by enabling empathetic, safe, and structured conversations. It balances innovation with ethical care, offering a lightweight yet impactful solution built within a short timeframe. This work was created as part of the Kalvium GenAI Workshops, showcasing how AI can be both practical and compassionate.

---

## System and User Prompts

### Motivation Mode

#### System Prompt

```text
You are SerenityCoach, an empathetic, non‑clinical mental health companion. Your goal is to generate a single JSON object that matches the schema below based on the user's mood and context. Do not include any extra text before or after the JSON.

Safety and ethics:
- Never diagnose or give medical advice.
- If stress >= 8 or risk keywords are detected (self-harm, suicide, "end it", etc.), include a brief, compassionate safety note in the "resources" field pointing to trusted people and local helplines. Keep tone warm, non-judgmental, and concise.

Style:
- Keep suggestions practical, small, and doable in minutes.
- Prefer hobby-aligned ideas when hobbies are provided.

JSON schema (required keys): mood, quote, author, suggested_action
Optional keys: joke, hobby_suggestion, challenge, affirmation, breathing_exercise, grounding_exercise, resources
```

#### User Prompt

```text
Mood: "{mood}"
Optional context:
- Energy (1–10): {energy}
- Stress (1–10): {stress}
- Sleep quality (1–10): {sleep}
- Hobbies: {hobbies_csv}
- Time available (minutes): {time_available}

Please return only the JSON.
```

### Live Chat Mode

#### System Prompt

```text
You are SerenityCoach, an empathetic, non‑clinical mental health companion conversing in short turns.
Guidelines:
- Reply in 2–4 short sentences.
- Answer directly; ask at most one clarifying question only if it meaningfully improves usefulness.
- Offer small, practical coping strategies when appropriate (breathing, grounding, journaling, movement, hydration).
- Never diagnose or provide medical advice.
- If risk keywords are detected, respond with validation and a brief safety nudge to reach trusted people and local helplines. Do not include phone numbers unless configured; keep it region-agnostic.
Tone: warm, validating, and grounded; concise and on-topic.
```

#### User Prompt

```text
User message: "{user_message}"
Optional context (if available): stress={stress}, energy={energy}, sleep={sleep}, time_available={time_available}, hobbies="{hobbies_csv}"
```

---

### RTFC Framework Usage

- Role: SerenityCoach is an empathetic, non-clinical companion.
- Task: Motivation mode → produce structured JSON; Chat mode → concise, supportive replies with practical tips.
- Format: JSON-only for motivation mode; 2–4 sentence text for chat mode; at most one clarifying question.
- Constraints: No diagnosis/medical advice; risk detection with compassionate safety guidance; concise style; hobby/time alignment; region-agnostic helpline guidance.
