from dynamic_prompter import (
    build_motivation_system_prompt,
    build_motivation_user_prompt,
    build_chat_system_prompt,
    build_chat_user_prompt,
)


def demo_motivation():
    system_prompt = build_motivation_system_prompt()
    user_prompt = build_motivation_user_prompt(
        mood="overwhelmed",
        energy=4,
        stress=7,
        sleep=6,
        hobbies_csv="reading, walking",
        time_available=10,
    )
    print("[DEMO] Motivation System Prompt:\n" + system_prompt + "\n")
    print("[DEMO] Motivation User Prompt:\n" + user_prompt + "\n")


def demo_chat():
    system_prompt = build_chat_system_prompt()
    user_prompt = build_chat_user_prompt(
        user_message="I feel anxious about tomorrow",
        context={"stress": 7, "time_available": 5, "hobbies_csv": "music"},
    )
    print("[DEMO] Chat System Prompt:\n" + system_prompt + "\n")
    print("[DEMO] Chat User Prompt:\n" + user_prompt + "\n")


if __name__ == "__main__":
    demo_motivation()
    demo_chat() 