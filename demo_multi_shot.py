#!/usr/bin/env python3
"""
Multi-shot Prompting Demonstration Script

This script demonstrates how multi-shot prompting improves AI responses
by providing multiple examples for different scenarios.
"""

import json
from multi_shot_prompter import MultiShotPrompter, PromptExample


def demonstrate_multi_shot_prompts():
    """Demonstrate the power of multi-shot prompting."""
    print("🚀 Multi-shot Prompting Demonstration for SerenityCoach")
    print("=" * 60)
    
    prompter = MultiShotPrompter()
    
    # Show example counts
    print(f"\n📊 Available Examples:")
    counts = prompter.get_example_count()
    for category, count in counts.items():
        print(f"  • {category.title()}: {count} examples")
    
    print("\n" + "=" * 60)
    
    # Demonstrate motivation prompt generation
    print("\n🎯 MOTIVATION MODE - Multi-shot Prompt Example:")
    print("-" * 40)
    
    motivation_prompt = prompter.get_motivation_prompt(
        mood="stressed",
        energy=3,
        stress=8,
        sleep=4,
        hobbies="reading, yoga",
        time_available=15
    )
    
    print("Generated prompt structure:")
    print(motivation_prompt[:800] + "..." if len(motivation_prompt) > 800 else motivation_prompt)
    
    print("\n" + "=" * 60)
    
    # Demonstrate chat prompt generation
    print("\n💬 CHAT MODE - Multi-shot Prompt Example:")
    print("-" * 40)
    
    chat_prompt = prompter.get_chat_prompt(
        user_message="I'm feeling really overwhelmed with work and can't focus",
        stress=8,
        energy=2,
        sleep=3,
        time_available=10,
        hobbies="music, walking"
    )
    
    print("Generated prompt structure:")
    print(chat_prompt[:800] + "..." if len(chat_prompt) > 800 else chat_prompt)
    
    print("\n" + "=" * 60)
    
    # Show specific examples
    print("\n🔍 DETAILED EXAMPLES:")
    print("-" * 40)
    
    print("\n1. ANXIOUS MOOD EXAMPLE:")
    anxious_example = prompter.motivation_examples[0]
    print(f"Input: {anxious_example.inputs}")
    print(f"Output: {anxious_example.output}")
    
    print("\n2. CRISIS RESPONSE EXAMPLE:")
    crisis_example = prompter.crisis_examples[0]
    print(f"Input: {crisis_example.inputs}")
    print(f"Output: {crisis_example.output}")
    
    print("\n" + "=" * 60)


def demonstrate_custom_prompt():
    """Demonstrate creating custom multi-shot prompts."""
    print("\n🎨 CUSTOM MULTI-SHOT PROMPT CREATION:")
    print("-" * 40)
    
    prompter = MultiShotPrompter()
    
    # Create custom examples for a specific task
    custom_examples = [
        PromptExample(
            inputs={"emotion": "frustrated", "context": "work deadline"},
            output="Take a 5-minute break, then break the task into 3 smaller steps. Start with the easiest one.",
            description="Work frustration"
        ),
        PromptExample(
            inputs={"emotion": "lonely", "context": "weekend alone"},
            output="Call a friend or family member, or try a new hobby activity. You're not alone in feeling this way.",
            description="Weekend loneliness"
        ),
        PromptExample(
            inputs={"emotion": "excited", "context": "new opportunity"},
            output="Channel your energy into planning and preparation. Write down your goals and celebrate this moment.",
            description="New opportunity excitement"
        )
    ]
    
    # Generate custom prompt
    custom_prompt = prompter.get_custom_prompt(
        examples=custom_examples,
        task_description="Provide emotional support and practical advice for various emotional states.",
        constraints="Keep responses under 2 sentences. Focus on actionable steps. Be empathetic and encouraging.",
        user_input="emotion='confused', context='career decision'"
    )
    
    print("Custom multi-shot prompt:")
    print(custom_prompt)
    
    print("\n" + "=" * 60)


def demonstrate_prompt_comparison():
    """Demonstrate the difference between different prompting approaches."""
    print("\n📈 PROMPTING APPROACH COMPARISON:")
    print("-" * 40)
    
    prompter = MultiShotPrompter()
    
    # Zero-shot approach (no examples)
    zero_shot = """You are SerenityCoach, an empathetic mental health companion.
Task: Generate a motivational quote and action for someone feeling tired.
Constraints: Keep it under 100 words, be encouraging.
Input: mood="tired", energy=2, stress=6"""
    
    # One-shot approach (single example)
    one_shot = """You are SerenityCoach, an empathetic mental health companion.
Task: Generate a motivational quote and action for someone feeling tired.
Constraints: Keep it under 100 words, be encouraging.

Example:
Input: mood="anxious", energy=4, stress=7
Output: "Feelings are waves; you can ride them without being swept away." - Unknown
Action: Try deep breathing for 2 minutes, then do one small thing you've been putting off.

Now respond to: mood="tired", energy=2, stress=6"""
    
    # Multi-shot approach (multiple examples)
    multi_shot = prompter.get_motivation_prompt("tired", 2, 6, 5, "gaming", 10)
    
    print("1. ZERO-SHOT (No examples):")
    print(zero_shot)
    print(f"\nLength: {len(zero_shot)} characters")
    
    print("\n2. ONE-SHOT (Single example):")
    print(one_shot)
    print(f"\nLength: {len(one_shot)} characters")
    
    print("\n3. MULTI-SHOT (Multiple examples):")
    print(multi_shot[:500] + "..." if len(multi_shot) > 500 else multi_shot)
    print(f"\nLength: {len(multi_shot)} characters")
    
    print("\n💡 Key Benefits of Multi-shot:")
    print("  • More consistent responses across different scenarios")
    print("  • Better handling of edge cases (high stress, crisis situations)")
    print("  • Improved understanding of tone and style")
    print("  • More reliable JSON formatting in motivation mode")
    print("  • Better crisis detection and response")
    
    print("\n" + "=" * 60)


def demonstrate_adding_examples():
    """Demonstrate how to add new examples to the prompter."""
    print("\n➕ ADDING NEW EXAMPLES:")
    print("-" * 40)
    
    prompter = MultiShotPrompter()
    
    # Show current counts
    print(f"Current motivation examples: {len(prompter.motivation_examples)}")
    
    # Add a new example
    new_example = PromptExample(
        inputs={
            "mood": "grateful",
            "energy": 9,
            "stress": 1,
            "sleep": 8,
            "hobbies": "gardening, cooking",
            "time_available": 20
        },
        output=json.dumps({
            "mood": "grateful",
            "quote": "Gratitude turns what we have into enough.",
            "author": "Melody Beattie",
            "suggested_action": "Write down 3 things you're grateful for, then spend 15 minutes in your garden or kitchen.",
            "hobby_suggestion": "Plant something new or try a new recipe with ingredients you love.",
            "affirmation": "Your gratitude is a beautiful light that touches others."
        }, indent=2),
        description="Positive grateful mood"
    )
    
    prompter.add_example("motivation", new_example)
    
    print(f"Added new example for 'grateful' mood")
    print(f"New motivation examples count: {len(prompter.motivation_examples)}")
    
    # Show the new example
    print(f"\nNew example output:")
    print(new_example.output)
    
    print("\n" + "=" * 60)


def main():
    """Main demonstration function."""
    try:
        demonstrate_multi_shot_prompts()
        demonstrate_custom_prompt()
        demonstrate_prompt_comparison()
        demonstrate_adding_examples()
        
        print("\n🎉 Multi-shot Prompting Demonstration Complete!")
        print("\nTo use SerenityCoach with multi-shot prompting:")
        print("  python main.py                    # Interactive motivation mode")
        print("  python main.py --chat             # Live chat mode")
        print("  python main.py --examples         # Show examples")
        print("  python main.py --mood 'tired'     # Quick motivation")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")


if __name__ == "__main__":
    main() 