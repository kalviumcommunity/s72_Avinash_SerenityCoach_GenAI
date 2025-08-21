import os
import requests
import json
import re
import argparse
import sys
from typing import Optional, Tuple
# New imports
import random
try:
    from dotenv import load_dotenv, find_dotenv
except Exception:
    load_dotenv = None
    find_dotenv = None

# ----------------------
# Local function(s) AI can call
# ----------------------

def get_motivation_by_mood(mood: str) -> dict:
    return {
        "mood": mood,
        "quote": "Keep pushing, greatness takes time.",
        "author": "Anonymous",
        "suggested_action": "Write down one thing you're grateful for today."
    }

# Try to import token logger (optional)
try:
    from token_utils import log_tokens_after_call
except Exception:
    def log_tokens_after_call(api_response=None, prompt_text=None, response_text=None, model_name=None):
        def estimate(t): return max(1, int(len(t) / 4)) if t else 0
        pt = estimate(prompt_text or "")
        ct = estimate(response_text or "")
        print(f"[Token estimate] prompt={pt} completion={ct} total={pt+ct}")

# Load environment variables from .env (both CWD and project root as fallback)
if load_dotenv is not None:
    try:
        # Load from nearest .env, if present
        load_dotenv(find_dotenv() if find_dotenv else None)
        # Also try project root relative to this file
        here = os.path.dirname(__file__)
        project_root_env = os.path.normpath(os.path.join(here, "..", ".env"))
        if os.path.exists(project_root_env):
            load_dotenv(project_root_env, override=False)
    except Exception:
        pass

# ----------------------
# Helpers
# ----------------------

def strip_code_fences(text: str) -> str:
    """Remove common markdown code fences like ```json or ``` ... ```."""
    if not text:
        return text
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def extract_first_json(text: str) -> Optional[str]:
    """Find the first balanced { ... } JSON substring."""
    if not text:
        return None
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    for i in range(start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start:i+1]
    return None


def validate_structured_output(obj: dict) -> Tuple[bool, str]:
    """Ensure required keys are present and are non-empty strings."""
    required = ["mood", "quote", "author", "suggested_action"]
    if not isinstance(obj, dict):
        return False, "Output is not a JSON object"
    for k in required:
        if k not in obj:
            return False, f"Missing key: {k}"
        if not isinstance(obj[k], str) or not obj[k].strip():
            return False, f"Invalid or empty value for key: {k}"
    return True, "OK"


def save_last_output(obj: dict, path: str = "last_output.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    print(f"[Saved] structured output -> {path}")

# New helpers for interactivity and fallbacks

def collect_user_context() -> dict:
    print("🧭 Let's get to know you a bit to personalize your motivation.")
    name = input("What's your name (optional)? ").strip()
    primary_concern = input("What's your main concern right now (e.g., anxiety, sadness, overwhelm, focus, motivation, burnout)? ").strip()
    try:
        energy = int(input("On a scale of 1-10, how is your energy today? ").strip())
    except Exception:
        energy = 5
    try:
        stress = int(input("On a scale of 1-10, how stressed do you feel? ").strip())
    except Exception:
        stress = 5
    try:
        sleep = int(input("On a scale of 1-10, how was your sleep last night? ").strip())
    except Exception:
        sleep = 5
    hobbies = input("What hobbies or interests do you enjoy (comma-separated)? ").strip()
    wants_joke = input("Would you like a light joke to brighten the mood? (y/n) ").strip().lower() in {"y", "yes"}
    exercise_pref = input("Prefer a quick breathing exercise, grounding exercise, or a micro-challenge? (breathing/grounding/challenge) ").strip().lower()
    try:
        minutes = int(input("How many minutes do you have right now? ").strip())
    except Exception:
        minutes = 5

    return {
        "name": name or None,
        "primary_concern": primary_concern or None,
        "energy": max(1, min(10, energy)),
        "stress": max(1, min(10, stress)),
        "sleep": max(1, min(10, sleep)),
        "hobbies": [h.strip() for h in hobbies.split(",") if h.strip()] if hobbies else [],
        "wants_joke": wants_joke,
        "exercise_pref": exercise_pref if exercise_pref in {"breathing", "grounding", "challenge"} else "challenge",
        "minutes": max(1, min(60, minutes)),
    }


def get_local_joke() -> str:
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "I tried to catch some fog yesterday. Mist.",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call cheese that isn't yours? Nacho cheese.",
    ]
    return random.choice(jokes)


def get_hobby_suggestion(hobbies: list, minutes: int) -> str:
    if not hobbies:
        return "Take a 5-minute mindful walk and notice three things you can see, hear, and feel."
    hobby = random.choice(hobbies).lower()
    suggestions = {
        "music": f"Listen to one favorite song with full attention for {minutes} minutes.",
        "reading": f"Read a few pages of a comforting book for {minutes} minutes.",
        "writing": f"Do a quick gratitude journal: list 3 things you're thankful for in {minutes} minutes.",
        "drawing": f"Sketch anything you see around you for {minutes} minutes.",
        "gaming": f"Play a cozy, low-stress game for {minutes} minutes to reset.",
        "cooking": f"Make a simple snack and hydrate—small nourishment in {minutes} minutes.",
        "walking": f"Go for a short walk and breathe deeply for {minutes} minutes.",
        "yoga": f"Try gentle stretches or a sun salutation flow for {minutes} minutes.",
    }
    return suggestions.get(hobby, f"Spend {minutes} minutes on '{hobby}' with full presence and no judgment.")


def get_micro_challenge(minutes: int, stress: int) -> str:
    if minutes <= 3:
        return "Do the 4-4-4 breath: inhale 4s, hold 4s, exhale 4s—repeat 3 times."
    if stress >= 8:
        return "5-4-3-2-1 grounding: name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste."
    return "Write a tiny to-do: one task you can finish today. Do it now for 5 minutes."

# Simple safety/risk detection

RISK_KEYWORDS = [
    "suicide", "kill myself", "hurt myself", "self-harm", "end it", "end my life", "hopeless",
    "no reason to live", "die", "can't go on", "harm myself"
]


def is_high_risk(text: str) -> bool:
    if not text:
        return False
    lower = text.lower()
    return any(kw in lower for kw in RISK_KEYWORDS)

# ----------------------
# Google Studio call
# ----------------------

def call_google_studio_structured(prompt_text: str,
                                  api_key: str,
                                  temperature: float = 0.2,
                                  top_k: Optional[int] = None,
                                  top_p: Optional[float] = None,
                                  stop_sequences: Optional[list] = None,
                                  model: str = "gemini-1.5-flash-latest") -> Tuple[dict, str]:
    if not api_key:
        raise RuntimeError("Provide api_key via .env (GOOGLE_API_KEY) or environment variable")

    base = "https://generativelanguage.googleapis.com/v1beta/models"
    url = f"{base}/{model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    generation_config = {"temperature": float(temperature)}
    if top_k is not None:
        generation_config["top_k"] = int(top_k)
    if top_p is not None:
        generation_config["top_p"] = float(top_p)
    if stop_sequences:
        generation_config["stopSequences"] = list(stop_sequences)

    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}],
        "generationConfig": generation_config
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    api_response = resp.json()

    try:
        response_text = api_response["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        response_text = json.dumps(api_response, ensure_ascii=False)

    return api_response, response_text

# ----------------------
# High-level function with function calling
# ----------------------

def get_structured_or_function_call(user_mood: str,
                                    api_key: str,
                                    temperature: float = 0.2,
                                    top_k: Optional[int] = None,
                                    top_p: Optional[float] = None,
                                    user_context: Optional[dict] = None) -> Optional[dict]:

    stop_marker = "<END_JSON>"
    system_instr = f"""
    You are a supportive, trauma-informed motivational and mental-wellbeing assistant.
    Your goals:
    - Validate feelings with warmth and empathy
    - Offer a motivational quote and a practical next step
    - Optionally include: a short clean joke, a hobby-aligned suggestion, and a micro-challenge
    - Keep advice non-clinical, avoid diagnosing. Encourage professional help if risk is high.

    Return a JSON object with keys (required): mood, quote, author, suggested_action
    Optional keys: joke, hobby_suggestion, challenge, affirmation, breathing_exercise, grounding_exercise, resources

    Respond ONLY with valid JSON, no extra text or formatting. End with {stop_marker}.
    """

    context_lines = []
    if user_context:
        if user_context.get("name"):
            context_lines.append(f"Name: {user_context['name']}")
        context_lines.append(f"Energy: {user_context.get('energy', 5)}/10")
        context_lines.append(f"Stress: {user_context.get('stress', 5)}/10")
        context_lines.append(f"Sleep: {user_context.get('sleep', 5)}/10")
        if user_context.get("primary_concern"):
            context_lines.append(f"Primary concern: {user_context['primary_concern']}")
        if user_context.get("hobbies"):
            context_lines.append(f"Hobbies: {', '.join(user_context['hobbies'])}")
        context_lines.append(f"Minutes available: {user_context.get('minutes', 5)}")

    user_line = f'User mood: "{user_mood}".'
    if context_lines:
        user_line += "\n" + "\n".join(context_lines)

    prompt = f"{system_instr}\n{user_line}\nOutput JSON now:\n"

    api_resp, raw = call_google_studio_structured(
        prompt_text=prompt,
        api_key=api_key,
        temperature=temperature,
        top_k=top_k,
        top_p=top_p,
        stop_sequences=[stop_marker]
    )

    log_tokens_after_call(api_response=api_resp, prompt_text=prompt, response_text=raw, model_name="gemini")

    cleaned = strip_code_fences(raw)
    parsed = None

    try:
        parsed = json.loads(cleaned)
    except Exception:
        candidate = extract_first_json(cleaned)
        if candidate:
            try:
                parsed = json.loads(candidate)
            except Exception:
                parsed = None

    if parsed is None:
        print("[Error] Could not parse JSON from model output:\n", raw)
        return None

    # Validate direct structured output
    ok, msg = validate_structured_output(parsed)
    if not ok:
        print(f"[Validation Failed] {msg}")
        return None

    save_last_output(parsed)
    return parsed

# ----------------------
# Live Chat Mode
# ----------------------

CHAT_SYSTEM_PROMPT = (
    "You are a compassionate, trauma-informed mental health companion. "
    "Your role is to listen with empathy, provide comfort, and share simple, practical coping strategies. "
    "Default style: calm, non-judgmental, clear, and supportive. "
    "Do NOT provide medical, diagnostic, or therapeutic advice. "
    "Keep responses concise (2–4 short sentences) and focus on reassurance, grounding techniques, and gentle encouragement. "
    "Offer specific, small suggestions only when appropriate (e.g., breathing, journaling, mindful breaks). "
    "Avoid asking questions unless one short clarification would meaningfully improve your response. "
    "If the user expresses hopelessness, self-harm, or crisis, respond with empathy first, "
    "then encourage them to reach out to trusted people or professional helplines in their country. "
    "Always prioritize emotional safety and validation over problem-solving."
)



def build_chat_prompt(history: list[str]) -> str:
    transcript = []
    for turn in history[-12:]:
        transcript.append(turn)
    transcript_text = "\n".join(transcript)
    return (
        f"{CHAT_SYSTEM_PROMPT}\n\n"
        f"Conversation so far:\n{transcript_text}\n\n"
        f"Assistant:"
    )


def run_live_chat(api_key: str,
                  temperature: float = 0.6,
                  top_k: Optional[int] = None,
                  top_p: Optional[float] = None):
    print("🤝 Live Mental Health Chat (type 'exit' to quit)")
    print("—" * 50)
    print("Start by sharing how you're feeling right now.")
    history: list[str] = []

    while True:
        user_text = input("You: ").strip()
        if not user_text:
            continue
        if user_text.lower() in {"exit", "quit", "q"}:
            print("Assistant: Thanks for sharing your time today. Be kind to yourself.")
            break

        # Safety net
        if is_high_risk(user_text):
            print("Assistant: I'm really glad you shared this. Your safety matters. "
                  "If you feel at risk of harm, please reach out to someone you trust "
                  "or a local helpline right now. You are not alone.")
            history.append(f"User: {user_text}")
            history.append("Assistant: If you'd like, we can focus on grounding for a minute. What's one thing you can see around you?")
            continue

        history.append(f"User: {user_text}")
        prompt = build_chat_prompt(history)
        api_resp, raw = call_google_studio_structured(
            prompt_text=prompt,
            api_key=api_key,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p,
            stop_sequences=None,
        )
        log_tokens_after_call(api_response=api_resp, prompt_text=prompt, response_text=raw, model_name="gemini")

        assistant_msg = raw.strip()
        assistant_msg = re.sub(r"\s*<\/?\w+>\s*$", "", assistant_msg)  # strip any stray tags
        lines = [ln.strip() for ln in assistant_msg.splitlines() if ln.strip()]
        text_out = " ".join(lines)
        print(f"Assistant: {text_out}")
        history.append(f"Assistant: {text_out}")

# ----------------------
# CLI
# ----------------------

def main_cli():
    ap = argparse.ArgumentParser(description="SerenityCoach – Mental Health Companion (CLI)")
    ap.add_argument("--mood", type=str, default=None, help="User mood string (optional)")
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--top_k", type=int, default=None)
    ap.add_argument("--top_p", type=float, default=None)
    ap.add_argument("--chat", action="store_true", help="Start live interactive mental health chat")
    # Keep --api_key for compatibility but do NOT prompt; prefer .env
    ap.add_argument("--api_key", type=str, default=None, help="Google API key; prefer .env GOOGLE_API_KEY")
    args = ap.parse_args()

    # Get API key from args or environment; do not prompt
    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GOOGLE_API_KEY not found. Please create a .env file with:\nGOOGLE_API_KEY=your_key_here")
        sys.exit(1)

    if args.chat:
        run_live_chat(api_key=api_key, temperature=args.temperature, top_k=args.top_k, top_p=args.top_p)
        return

    # Get user mood and richer context
    user_mood = args.mood
    if not user_mood:
        print("🤖 Welcome to SerenityCoach – Your Mental Health Companion!")
        print("=" * 50)
        print("💭 In 1-2 words, how are you feeling today?")
        user_mood = input("Your mood: ").strip()
        if not user_mood:
            print("❌ Error: Please provide your mood.")
            sys.exit(1)
        print()

    user_context = collect_user_context()
    wants_joke = bool(user_context.get("wants_joke"))

    print(f"🎯 Generating motivation for: '{user_mood}'")
    print("⏳ Please wait...")
    print()

    parsed = get_structured_or_function_call(
        user_mood=user_mood,
        api_key=api_key,
        temperature=args.temperature,
        top_k=args.top_k,
        top_p=args.top_p,
        user_context=user_context
    )

    # Fallbacks for extras
    extra_joke = None
    hobby_tip = None
    micro_challenge = None
    if wants_joke:
        extra_joke = get_local_joke()
    if user_context.get("hobbies"):
        hobby_tip = get_hobby_suggestion(user_context["hobbies"], user_context.get("minutes", 5))
    micro_challenge = get_micro_challenge(user_context.get("minutes", 5), user_context.get("stress", 5))

    if parsed:
        print("\n" + "=" * 50)
        print("🌟 YOUR MOTIVATION FOR TODAY 🌟")
        print("=" * 50)
        print(f"💭 Mood: {parsed['mood']}")
        print(f"💬 Quote: \"{parsed['quote']}\"")
        print(f"👤 Author: {parsed['author']}")
        print(f"🎯 Suggested Action: {parsed['suggested_action']}")

        # Optional fields from model
        for key, label in [
            ("joke", "😄 Joke"),
            ("hobby_suggestion", "🎨 Hobby Tip"),
            ("challenge", "🧩 Micro-Challenge"),
            ("affirmation", "🪴 Affirmation"),
            ("breathing_exercise", "🌬️ Breathing"),
            ("grounding_exercise", "🧘 Grounding"),
            ("resources", "📚 Resources"),
        ]:
            if isinstance(parsed.get(key), str) and parsed.get(key).strip():
                print(f"{label}: {parsed[key]}")

        # Local fallbacks if the model didn't provide them
        if wants_joke and not parsed.get("joke") and extra_joke:
            print(f"😄 Joke: {extra_joke}")
        if not parsed.get("hobby_suggestion") and hobby_tip:
            print(f"🎨 Hobby Tip: {hobby_tip}")
        if not parsed.get("challenge") and micro_challenge:
            print(f"🧩 Micro-Challenge: {micro_challenge}")

        # Gentle safety note if stress is high
        if user_context.get("stress", 5) >= 8:
            print("\n🛟 If you're feeling overwhelmed, consider reaching out to someone you trust, or a local helpline. You matter.")

        print("=" * 50)
        print("💪 Keep going, you've got this!")
    else:
        print("\n❌ [Failed to get valid output]")
        print("Please try again or check your API key.")

if __name__ == "__main__":
    main_cli()
