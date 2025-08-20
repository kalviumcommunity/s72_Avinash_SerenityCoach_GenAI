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

## Dynamic Prompting

Use this dynamic prompting template to adapt the assistant’s behavior at runtime using user profile, retrieved knowledge, and tool availability.

### Template (ready to reuse)

```yaml
system:
  role: "{{agent_role}}"
  mission: "{{goal}}"
  success_criteria:
    - "{{criterion_1}}"
    - "{{criterion_2}}"
    - "{{criterion_3}}"

  user_profile:
    persona: "{{user_persona}}"
    expertise_level: "{{user_expertise}}"
    preferences:
      tone: "{{tone}}"
      format: "{{preferred_format}}"

  constraints:
    - "Stay within scope of {{scope}}"
    - "Follow {{style_guide}}"
    - "Time/Latency budget: {{latency_budget}}"
    - "Avoid disallowed content: {{disallowed_content}}"

  dynamic_context:
    memory_summary: "{{memory_summary_optional}}"
    retrieved_knowledge:
      - "{{context_snippet_1_optional}}"
      - "{{context_snippet_2_optional}}"
    recent_activity_summary: "{{recent_activity_optional}}"

  tools_available:
    - name: "{{tool_name_1}}"
      description: "{{tool_description_1}}"
      io: { input: "{{tool_input_1}}", output: "{{tool_output_1}}"}
    - name: "{{tool_name_2_optional}}"
      description: "{{tool_description_2_optional}}"
      io: { input: "{{tool_input_2_optional}}", output: "{{tool_output_2_optional}}"}

  inputs_schema:
    required_slots:
      - "{{slot_1}}"
      - "{{slot_2}}"
    optional_slots:
      - "{{slot_opt_1}}"
      - "{{slot_opt_2}}"
    validations:
      - slot: "{{slot_1}}"
        rule: "{{validation_rule_1}}"
      - slot: "{{slot_2}}"
        rule: "{{validation_rule_2}}"

  examples_few_shot:
    - user: "{{example_user_1}}"
      assistant: "{{example_assistant_1}}"
    - user: "{{example_user_2_optional}}"
      assistant: "{{example_assistant_2_optional}}"

assistant_guidance:
  - "If any required slot is missing or invalid, ask up to 3 targeted clarifying questions before proceeding."
  - "Use retrieved_knowledge when relevant; cite by short labels like [K1], [K2]."
  - "Prefer stepwise structure in the final answer without revealing internal chain-of-thought."
  - "If tools can improve accuracy, propose the plan and the specific tool calls needed."
  - "If context is empty, proceed best-effort and note assumptions explicitly."
  - "Keep output concise, actionable, and formatted per 'output_contract'."

output_contract:
  type: "{{output_type}}"        # e.g., 'markdown' or 'json'
  schema_or_style:
    if: "json"
    then:
      properties:
        answer: string
        assumptions: array
        steps: array
        follow_ups: array
        citations: array
      required: ["answer"]
    else_if: "markdown"
    then:
      style:
        - "Use '###' headings"
        - "Bulleted lists with bold labels"
        - "Code blocks only for concrete commands/templates"

inputs_runtime:
  slot_values:
    "{{slot_1}}": "{{value_1}}"
    "{{slot_2}}": "{{value_2}}"
    "{{slot_opt_1}}": "{{value_opt_1_optional}}"
    "{{slot_opt_2}}": "{{value_opt_2_optional}}"
```

### Minimal usage example (filled)

```yaml
system:
  role: "Calm, practical wellness coach"
  mission: "Design a 7‑day, low-friction mindfulness plan for a busy professional"
  success_criteria:
    - "Daily actions fit into 10–15 minutes"
    - "Clear tracking method"
    - "Gentle, encouraging tone"

  user_profile:
    persona: "Stressed product manager"
    expertise_level: "Beginner in mindfulness"
    preferences:
      tone: "supportive"
      format: "markdown checklist"

  constraints:
    - "No medical diagnosis"
    - "Respect workplace time constraints"
    - "Latency budget: fast"

  dynamic_context:
    memory_summary: "User prefers audio over text; commutes 30 mins."
    retrieved_knowledge:
      - "[K1] 4-7-8 breathing basics"
      - "[K2] Habit stacking with existing routines"
    recent_activity_summary: "User completed a 3‑day breathwork trial"

  tools_available:
    - name: "Timer"
      description: "Start a 10‑minute timer"
      io: { input: "minutes:int", output: "confirmation" }

  inputs_schema:
    required_slots: ["work_hours", "commute_mode"]
    optional_slots: ["sleep_window"]
    validations:
      - slot: "work_hours"
        rule: "range within 6–12 hours"

assistant_guidance:
  - "If commute_mode is missing, ask 1 question."
  - "Cite [K1], [K2] when used."
  - "Suggest Timer tool when timing is helpful."

output_contract:
  type: "markdown"
  schema_or_style:
    then:
      style:
        - "Use '###' headings"
        - "Bold labels in bullets"
        - "Short checklists"

inputs_runtime:
  slot_values:
    work_hours: "9–6"
    commute_mode: "train"
```

### Quick Tips

- **Replace placeholders dynamically**: Populate from app state, RAG results, and user slots.
- **Keep required slots minimal**: Ask targeted clarifying questions only when needed.
- **Limit context items**: Prefer 2–5 high-signal items in `retrieved_knowledge`.
- **Match output_contract**: Enforce schema/format to keep responses consistent.
