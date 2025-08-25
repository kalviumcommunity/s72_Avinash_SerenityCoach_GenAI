# dynamic_prompter.py

from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class GenerationConfig:
    temperature: float = 0.7
    top_k: int = 40
    top_p: float = 0.9


COT_ADDON_MOTIVATION = (
    "Deliberate reasoning (hidden): Think step-by-step to select a mood-aligned quote and one practical micro-action. "
    "Consider user context (energy, stress, sleep, hobbies, time). Check for risk signals and, if present, add a brief, compassionate resource note. "
    "Do not include your reasoning or steps in the output. Return only the JSON that matches the required schema."
)

COT_ADDON_CHAT = (
    "Use an internal scratchpad to reason about the user's message and pick at most one clarifying question only if needed. "
    "Offer one or two practical tips. Do not reveal your chain-of-thought; reply in 2-4 short sentences."
)


def build_motivation_system_prompt() -> str:
    return (
        "You are SerenityCoach, an empathetic, non-clinical mental health companion. "
        "Your goal is to generate a single JSON object that matches the schema below based on the user's mood and context. "
        "Do not include any extra text before or after the JSON.\n\n"
        "Safety and ethics:\n"
        "- Never diagnose or give medical advice.\n"
        "- If stress >= 8 or risk keywords are detected (self-harm, suicide, 'end it', etc.), include a brief, compassionate safety note in the 'resources' field pointing to trusted people and local helplines. "
        "Keep tone warm, non-judgmental, and concise.\n\n"
        "Style:\n"
        "- Keep suggestions practical, small, and doable in minutes.\n"
        "- Prefer hobby-aligned ideas when hobbies are provided.\n\n"
        "JSON schema (required keys): mood, quote, author, suggested_action\n"
        "Optional keys: joke, hobby_suggestion, challenge, affirmation, breathing_exercise, grounding_exercise, resources\n\n"
        f"{COT_ADDON_MOTIVATION}"
    )


def build_motivation_user_prompt(
    mood: str,
    energy: Optional[int] = None,
    stress: Optional[int] = None,
    sleep: Optional[int] = None,
    hobbies_csv: Optional[str] = None,
    time_available: Optional[int] = None,
) -> str:
    def _fmt(val: Optional[Any]) -> str:
        return "" if val is None else str(val)

    return (
        f"Mood: \"{mood}\"\n"
        "Optional context:\n"
        f"- Energy (1-10): {_fmt(energy)}\n"
        f"- Stress (1-10): {_fmt(stress)}\n"
        f"- Sleep quality (1-10): {_fmt(sleep)}\n"
        f"- Hobbies: {_fmt(hobbies_csv)}\n"
        f"- Time available (minutes): {_fmt(time_available)}\n\n"
        "Please return only the JSON."
    )


def build_chat_system_prompt() -> str:
    return (
        "You are SerenityCoach, an empathetic, non-clinical mental health companion conversing in short turns.\n"
        "Guidelines:\n"
        "- Reply in 2-4 short sentences.\n"
        "- Answer directly; ask at most one clarifying question only if it meaningfully improves usefulness.\n"
        "- Offer small, practical coping strategies when appropriate (breathing, grounding, journaling, movement, hydration).\n"
        "- Never diagnose or provide medical advice.\n"
        "- If risk keywords are detected, respond with validation and a brief safety nudge to reach trusted people and local helplines. "
        "Do not include phone numbers unless configured; keep it region-agnostic.\n"
        "Tone: warm, validating, and grounded; concise and on-topic.\n\n"
        f"{COT_ADDON_CHAT}"
    )


def build_chat_user_prompt(
    user_message: str,
    context: Optional[Dict[str, Any]] = None,
) -> str:
    context = context or {}
    stress = context.get("stress")
    energy = context.get("energy")
    sleep = context.get("sleep")
    time_available = context.get("time_available")
    hobbies_csv = context.get("hobbies_csv")

    parts = [f"User message: \"{user_message}\""]
    ctx_bits = []
    if stress is not None:
        ctx_bits.append(f"stress={stress}")
    if energy is not None:
        ctx_bits.append(f"energy={energy}")
    if sleep is not None:
        ctx_bits.append(f"sleep={sleep}")
    if time_available is not None:
        ctx_bits.append(f"time_available={time_available}")
    if hobbies_csv:
        ctx_bits.append(f"hobbies=\"{hobbies_csv}\"")

    if ctx_bits:
        parts.append("Optional context (if available): " + ", ".join(ctx_bits))

    return "\n".join(parts)


__all__ = [
    "GenerationConfig",
    "build_motivation_system_prompt",
    "build_motivation_user_prompt",
    "build_chat_system_prompt",
    "build_chat_user_prompt",
] 