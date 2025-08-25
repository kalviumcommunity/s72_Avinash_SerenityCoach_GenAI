import argparse
from typing import Optional, Dict, Any

from dynamic_prompter import (
    build_motivation_system_prompt,
    build_motivation_user_prompt,
    build_chat_system_prompt,
    build_chat_user_prompt,
)


def print_section(title: str, content: str) -> None:
    line = "=" * len(title)
    print(title)
    print(line)
    print(content)
    print()


def run_motivation_flow(args: argparse.Namespace) -> None:
    system_prompt = build_motivation_system_prompt()
    user_prompt = build_motivation_user_prompt(
        mood=args.mood or "neutral",
        energy=args.energy,
        stress=args.stress,
        sleep=args.sleep,
        hobbies_csv=args.hobbies,
        time_available=args.time,
    )

    print_section("[Motivation] System Prompt", system_prompt)
    print_section("[Motivation] User Prompt", user_prompt)
    print("[Note] Integrate these prompts with your LLM call (e.g., Gemini/OpenAI) and request JSON-only output.\n")


def run_chat_flow(args: argparse.Namespace) -> None:
    system_prompt = build_chat_system_prompt()
    context: Dict[str, Any] = {
        "stress": args.stress,
        "energy": args.energy,
        "sleep": args.sleep,
        "time_available": args.time,
        "hobbies_csv": args.hobbies,
    }
    user_prompt = build_chat_user_prompt(args.message or "Hi", context)

    print_section("[Chat] System Prompt", system_prompt)
    print_section("[Chat] User Prompt", user_prompt)
    print("[Note] Pipe these prompts into your chat completion API and display the model's short reply.\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SerenityCoach CLI with safe CoT prompting")

    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Motivation mode
    p_mot = subparsers.add_parser("motivation", help="Build prompts for motivation mode")
    p_mot.add_argument("--mood", type=str, default=None)
    p_mot.add_argument("--energy", type=int, default=None)
    p_mot.add_argument("--stress", type=int, default=None)
    p_mot.add_argument("--sleep", type=int, default=None)
    p_mot.add_argument("--hobbies", type=str, default=None)
    p_mot.add_argument("--time", type=int, default=None, help="Minutes available")

    # Chat mode
    p_chat = subparsers.add_parser("chat", help="Build prompts for live chat mode")
    p_chat.add_argument("--message", type=str, default=None)
    p_chat.add_argument("--energy", type=int, default=None)
    p_chat.add_argument("--stress", type=int, default=None)
    p_chat.add_argument("--sleep", type=int, default=None)
    p_chat.add_argument("--hobbies", type=str, default=None)
    p_chat.add_argument("--time", type=int, default=None, help="Minutes available")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.mode == "motivation":
        run_motivation_flow(args)
    elif args.mode == "chat":
        run_chat_flow(args)
    else:
        raise SystemExit("Unknown mode")


if __name__ == "__main__":
    main() 