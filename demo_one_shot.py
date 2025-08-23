#!/usr/bin/env python3
"""
Demonstration of One-Shot Prompting in SerenityCoach
Shows how the one-shot prompts work and their benefits.
"""

from prompts import OneShotPrompter, get_motivation_prompt, get_chat_prompt
import json


def demonstrate_motivation_prompt():
    """Demonstrate motivation mode one-shot prompting."""
    print("🌟 MOTIVATION MODE - One-Shot Prompting Demo")
    print("=" * 60)
    
    # Create a one-shot prompt for a tired user
    prompt = get_motivation_prompt(
        mood="tired",
        energy=2,
        stress=7,
        sleep=3,
        hobbies="reading, music, walking",
        time_available=20
    )
    
    print("📝 Generated One-Shot Prompt:")
    print("-" * 40)
    print(prompt)
    
    print("\n💡 Key Benefits of One-Shot Prompting:")
    print("1. Clear Example: Shows exact format and tone expected")
    print("2. Reduced Ambiguity: Model knows exactly what to produce")
    print("3. Consistent Output: Follows the demonstrated pattern")
    print("4. Safety Guidelines: Example includes safety considerations")
    
    # Simulate what the AI would generate
    print("\n🤖 Expected AI Response (JSON):")
    print("-" * 40)
    expected_response = {
        "mood": "tired",
        "quote": "Rest if you must, but don't you quit.",
        "author": "Unknown",
        "suggested_action": "Take a 10-minute gentle walk outside, then rest with a book and tea.",
        "breathing_exercise": "Inhale for 4, hold for 4, exhale for 6 - repeat 5 times.",
        "hobby_suggestion": "Listen to calming music while doing gentle stretches.",
        "challenge": "Write down 3 things you're grateful for today.",
        "resources": "Remember, it's okay to rest and ask for help when needed."
    }
    print(json.dumps(expected_response, indent=2))


def demonstrate_chat_prompt():
    """Demonstrate chat mode one-shot prompting."""
    print("\n\n💬 CHAT MODE - One-Shot Prompting Demo")
    print("=" * 60)
    
    # Create a one-shot prompt for a user message
    prompt = get_chat_prompt(
        user_message="I'm feeling really anxious about my presentation tomorrow",
        energy=4,
        stress=8,
        sleep=5,
        hobbies="yoga, cooking",
        time_available=15
    )
    
    print("📝 Generated One-Shot Prompt:")
    print("-" * 40)
    print(prompt)
    
    print("\n💡 Key Benefits of One-Shot Prompting in Chat:")
    print("1. Tone Consistency: Example shows empathetic, supportive tone")
    print("2. Response Length: Demonstrates 2-4 sentence format")
    print("3. Practical Tips: Shows how to include actionable advice")
    print("4. Safety Integration: Example includes risk assessment")
    
    # Simulate what the AI would generate
    print("\n🤖 Expected AI Response:")
    print("-" * 40)
    expected_response = """I understand that feeling of anxiety before a big presentation—it's completely normal and shows you care about doing well. Try this quick grounding exercise: take 3 deep breaths, then name 5 things you can see around you. For your presentation prep, what's the smallest step you could take right now to feel more prepared? Remember, you've got this!"""
    print(expected_response)


def demonstrate_prompt_comparison():
    """Compare zero-shot vs one-shot prompting."""
    print("\n\n🔄 ZERO-SHOT vs ONE-SHOT PROMPTING COMPARISON")
    print("=" * 60)
    
    print("📊 Zero-Shot Prompting:")
    print("- Only instructions and constraints")
    print("- May produce inconsistent results")
    print("- Higher chance of format errors")
    print("- Less predictable tone")
    
    print("\n📊 One-Shot Prompting:")
    print("- Instructions + constraints + example")
    print("- Consistent, predictable results")
    print("- Lower chance of format errors")
    print("- Guaranteed tone consistency")
    
    print("\n🎯 When to Use Each:")
    print("Zero-Shot: Simple tasks, when you want creative variety")
    print("One-Shot: Complex tasks, when consistency is crucial")
    print("One-Shot: When specific format/tone is required")


def demonstrate_custom_prompts():
    """Show how to create custom one-shot prompts."""
    print("\n\n🔧 CUSTOM ONE-SHOT PROMPT CREATION")
    print("=" * 60)
    
    prompter = OneShotPrompter()
    
    # Create a custom prompt for journaling
    custom_prompt = f"""You are SerenityCoach, helping users with journaling prompts.
Task: Generate a reflective journaling question based on the user's mood.

Example:
User mood: "stressed"
Journaling question: "What's one small thing that brought you joy today, even in the midst of stress?"

Now generate a journaling question for:
User mood: "grateful"

Return only the question:"""
    
    print("📝 Custom Journaling Prompt:")
    print("-" * 40)
    print(custom_prompt)
    
    print("\n💡 Benefits of Custom Prompts:")
    print("1. Tailored to specific use cases")
    print("2. Maintains consistent style")
    print("3. Easy to modify and extend")
    print("4. Reusable across different contexts")


def main():
    """Run all demonstrations."""
    print("🚀 SerenityCoach One-Shot Prompting Demonstration")
    print("=" * 60)
    
    demonstrate_motivation_prompt()
    demonstrate_chat_prompt()
    demonstrate_prompt_comparison()
    demonstrate_custom_prompts()
    
    print("\n\n✅ Demonstration Complete!")
    print("=" * 60)
    print("The one-shot prompting approach ensures:")
    print("• Consistent, high-quality responses")
    print("• Proper format and structure")
    print("• Appropriate tone and style")
    print("• Safety and ethical considerations")
    print("\nTry running 'python main.py' to see it in action!")


if __name__ == "__main__":
    main() 