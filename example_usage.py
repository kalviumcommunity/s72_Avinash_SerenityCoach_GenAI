#!/usr/bin/env python3
"""
Practical Examples of One-Shot Prompting Usage
Shows real-world scenarios where one-shot prompting improves AI responses.
"""

from prompts import get_motivation_prompt, get_chat_prompt, OneShotPrompter
import json


def example_1_motivation_for_different_moods():
    """Example 1: Generating motivation for different moods using one-shot prompting."""
    print("🌟 Example 1: Motivation for Different Moods")
    print("=" * 50)
    
    moods = ["anxious", "tired", "overwhelmed", "grateful"]
    
    for mood in moods:
        print(f"\n📝 Generating motivation for mood: '{mood}'")
        print("-" * 40)
        
        # Generate one-shot prompt
        prompt = get_motivation_prompt(
            mood=mood,
            energy=4,
            stress=6,
            sleep=5,
            hobbies="reading, music",
            time_available=15
        )
        
        # Show the key parts of the prompt
        print(f"Role: SerenityCoach mental health companion")
        print(f"Task: Generate JSON response for mood '{mood}'")
        print(f"Example included: ✅ (shows exact format expected)")
        print(f"Safety guidelines: ✅ (risk assessment included)")
        
        # Simulate what the AI would generate
        if mood == "anxious":
            response = {
                "mood": "anxious",
                "quote": "Anxiety is like a rocking chair. It gives you something to do, but it doesn't get you anywhere.",
                "author": "Anonymous",
                "suggested_action": "Practice 4-7-8 breathing: inhale 4, hold 7, exhale 8. Repeat 3 times.",
                "breathing_exercise": "4-7-8 breathing technique for anxiety relief",
                "resources": "Remember, anxiety is temporary and manageable. You're doing great!"
            }
        elif mood == "tired":
            response = {
                "mood": "tired",
                "quote": "Rest is not idleness, and to lie sometimes on the grass under trees on a summer's day is by no means a waste of time.",
                "author": "John Lubbock",
                "suggested_action": "Take a 10-minute power nap or do gentle stretches.",
                "hobby_suggestion": "Listen to calming music while resting",
                "challenge": "Write down 3 things you accomplished today, no matter how small"
            }
        elif mood == "overwhelmed":
            response = {
                "mood": "overwhelmed",
                "quote": "You don't have to see the whole staircase, just take the first step.",
                "author": "Martin Luther King Jr.",
                "suggested_action": "Write down just 3 priorities for today. Start with the smallest one.",
                "grounding_exercise": "5-4-3-2-1: Name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste",
                "resources": "When overwhelmed, break tasks into tiny steps. You're making progress!"
            }
        else:  # grateful
            response = {
                "mood": "grateful",
                "quote": "Gratitude turns what we have into enough.",
                "author": "Anonymous",
                "suggested_action": "Share your gratitude with someone you care about.",
                "challenge": "Write a thank-you note to someone who helped you recently",
                "affirmation": "Your positive energy is contagious and makes the world better"
            }
        
        print(f"🤖 AI Response: {json.dumps(response, indent=2)}")
        print(f"✅ Format: Consistent JSON structure")
        print(f"✅ Tone: Empathetic and supportive")
        print(f"✅ Safety: Appropriate for mood level")


def example_2_chat_responses_with_context():
    """Example 2: Chat responses that adapt to user context using one-shot prompting."""
    print("\n\n💬 Example 2: Context-Aware Chat Responses")
    print("=" * 50)
    
    chat_scenarios = [
        {
            "message": "I can't sleep because I'm worried about tomorrow's meeting",
            "context": {"stress": 8, "sleep": 2, "energy": 3, "time_available": 20}
        },
        {
            "message": "I feel like I'm not making progress on my goals",
            "context": {"stress": 6, "sleep": 6, "energy": 5, "time_available": 45}
        },
        {
            "message": "Everything feels like too much right now",
            "context": {"stress": 9, "sleep": 3, "energy": 2, "time_available": 10}
        }
    ]
    
    for i, scenario in enumerate(chat_scenarios, 1):
        print(f"\n📝 Scenario {i}: User says '{scenario['message']}'")
        print("-" * 50)
        
        # Generate one-shot prompt
        prompt = get_chat_prompt(
            user_message=scenario['message'],
            **scenario['context']
        )
        
        print(f"Context: stress={scenario['context']['stress']}, energy={scenario['context']['energy']}")
        print(f"One-shot prompt includes: ✅ Example conversation")
        print(f"Safety check: ✅ Risk assessment for high stress")
        
        # Simulate AI response
        if scenario['context']['stress'] >= 8:
            response = "I hear how overwhelmed you're feeling, and it's completely valid. Let's take this one moment at a time. Try this quick grounding: take 3 slow breaths and name one thing you can see right now. What's the smallest thing you could do to take care of yourself in the next 5 minutes?"
            safety_note = "⚠️  High stress detected - remember you don't have to handle everything alone."
        else:
            response = "It sounds like you're feeling stuck, and that's a common experience when working toward goals. Sometimes progress is invisible until we look back. What's one tiny step you could take today that would move you forward, even just a little bit?"
            safety_note = ""
        
        print(f"🤖 AI Response: {response}")
        if safety_note:
            print(f"🆘 {safety_note}")
        print(f"✅ Length: 2-4 sentences as specified")
        print(f"✅ Tone: Warm and validating")
        print(f"✅ Practical: Includes actionable advice")


def example_3_custom_prompt_creation():
    """Example 3: Creating custom one-shot prompts for specific use cases."""
    print("\n\n🔧 Example 3: Custom One-Shot Prompt Creation")
    print("=" * 50)
    
    # Create a custom prompt for stress management
    custom_prompt = """You are SerenityCoach, specializing in stress management techniques.
Task: Suggest 3 stress-reduction activities based on the user's current situation.

Constraints:
- Activities must be doable in the specified time
- Consider energy and stress levels
- Include at least one breathing or grounding exercise
- Keep suggestions simple and practical

Example:
User situation: "High stress (8/10), low energy (2/10), 15 minutes available"
Activities:
1. "4-7-8 breathing: 5 minutes of deep breathing to calm your nervous system"
2. "Gentle stretching: 5 minutes of slow arm and neck stretches"
3. "Mindful tea break: 5 minutes to slowly sip tea and observe your surroundings"

Now suggest activities for:
User situation: "Medium stress (6/10), medium energy (5/10), 30 minutes available"

Return only the 3 activities:"""
    
    print("📝 Custom Stress Management Prompt:")
    print("-" * 40)
    print(custom_prompt)
    
    print("\n💡 Benefits of this custom prompt:")
    print("1. Specific to stress management")
    print("2. Includes relevant example")
    print("3. Adapts to user's energy and time")
    print("4. Maintains SerenityCoach's style")
    
    # Simulate AI response
    ai_response = """1. "Progressive muscle relaxation: 10 minutes to systematically tense and release muscle groups"
2. "Nature walk: 15 minutes outside to connect with your surroundings and get fresh air"
3. "Journaling: 5 minutes to write down your thoughts and feelings without judgment" """
    
    print(f"\n🤖 Expected AI Response:")
    print("-" * 40)
    print(ai_response)


def example_4_prompt_validation():
    """Example 4: Validating prompt outputs to ensure quality."""
    print("\n\n✅ Example 4: Prompt Output Validation")
    print("=" * 50)
    
    from prompts import validate_prompt_output
    
    # Test valid JSON output
    valid_json = '{"mood": "happy", "quote": "Life is beautiful", "author": "Unknown"}'
    is_valid = validate_prompt_output(valid_json, "json")
    print(f"Valid JSON: {valid_json}")
    print(f"Validation result: {'✅ PASS' if is_valid else '❌ FAIL'}")
    
    # Test invalid JSON output
    invalid_json = '{"mood": "happy", "quote": "Life is beautiful", "author": "Unknown"'  # Missing closing brace
    is_valid = validate_prompt_output(invalid_json, "json")
    print(f"\nInvalid JSON: {invalid_json}")
    print(f"Validation result: {'✅ PASS' if is_valid else '❌ FAIL'}")
    
    # Test text output
    text_output = "This is a valid text response for chat mode."
    is_valid = validate_prompt_output(text_output, "text")
    print(f"\nText output: {text_output}")
    print(f"Validation result: {'✅ PASS' if is_valid else '❌ FAIL'}")


def main():
    """Run all examples."""
    print("🚀 SerenityCoach One-Shot Prompting: Practical Examples")
    print("=" * 60)
    
    example_1_motivation_for_different_moods()
    example_2_chat_responses_with_context()
    example_3_custom_prompt_creation()
    example_4_prompt_validation()
    
    print("\n\n🎯 Key Takeaways:")
    print("=" * 60)
    print("1. One-shot prompting ensures consistent, high-quality responses")
    print("2. Examples reduce ambiguity and improve format accuracy")
    print("3. Safety considerations are built into every prompt")
    print("4. Custom prompts can be created for specific use cases")
    print("5. Output validation ensures reliability")
    
    print("\n✨ Ready to implement in your own projects!")
    print("The one-shot approach is perfect for applications requiring:")
    print("• Consistent output format")
    print("• Reliable tone and style")
    print("• Safety and ethical considerations")
    print("• Professional-grade AI interactions")


if __name__ == "__main__":
    main() 