#!/usr/bin/env python3
"""
Example script demonstrating how to use the SerenityCoach prompt system.
This script shows how to construct prompts for different modes and contexts.
"""

from prompts import (
    get_system_prompt,
    build_motivation_prompt,
    build_chat_prompt,
    format_prompt_for_api,
    validate_prompt_length,
    sanitize_prompt
)

def demonstrate_motivation_mode():
    """Demonstrate motivation mode prompt construction."""
    print("=" * 60)
    print("MOTIVATION MODE EXAMPLE")
    print("=" * 60)
    
    # Get the system prompt
    system_prompt = get_system_prompt('motivation')
    print(f"System Prompt Length: {len(system_prompt)} characters")
    
    # Create user context
    user_context = {
        'energy': 6,
        'stress': 7,
        'sleep': 5,
        'hobbies': 'reading, yoga, walking',
        'time_available': 20,
        'primary_concern': 'work deadlines and anxiety'
    }
    
    # Build the user prompt
    user_prompt = build_motivation_prompt("overwhelmed", user_context)
    
    # Format complete prompt
    complete_prompt = format_prompt_for_api(system_prompt, user_prompt)
    
    print(f"\nUser Context: {user_context}")
    print(f"\nUser Prompt:\n{user_prompt}")
    print(f"\nComplete Prompt Length: {len(complete_prompt)} characters")
    
    # Validate prompt length
    if validate_prompt_length(complete_prompt):
        print("✅ Prompt length is within acceptable limits")
    else:
        print("⚠️  Prompt may be too long for optimal performance")
    
    return complete_prompt

def demonstrate_chat_mode():
    """Demonstrate chat mode prompt construction."""
    print("\n" + "=" * 60)
    print("CHAT MODE EXAMPLE")
    print("=" * 60)
    
    # Get the system prompt
    system_prompt = get_system_prompt('chat')
    print(f"System Prompt Length: {len(system_prompt)} characters")
    
    # Create user context
    user_context = {
        'stress': 8,
        'energy': 4,
        'sleep': 6,
        'time_available': 15,
        'hobbies': 'music, meditation'
    }
    
    # Simulate conversation history
    conversation_history = [
        "User: I'm feeling really anxious about my presentation tomorrow",
        "Assistant: I can hear how much this presentation is weighing on you. That's a completely normal feeling to have.",
        "User: I know it's normal but I can't seem to calm down",
        "Assistant: It's okay to feel this way. Let's try something simple together - can you take three slow breaths?"
    ]
    
    # Build the chat prompt
    user_message = "I tried breathing but I'm still so nervous"
    chat_prompt = build_chat_prompt(user_message, user_context, conversation_history)
    
    # Format complete prompt
    complete_prompt = format_prompt_for_api(system_prompt, chat_prompt)
    
    print(f"\nUser Message: {user_message}")
    print(f"\nUser Context: {user_context}")
    print(f"\nConversation History: {len(conversation_history)} turns")
    print(f"\nChat Prompt:\n{chat_prompt}")
    print(f"\nComplete Prompt Length: {len(complete_prompt)} characters")
    
    # Validate prompt length
    if validate_prompt_length(complete_prompt):
        print("✅ Prompt length is within acceptable limits")
    else:
        print("⚠️  Prompt may be too long for optimal performance")
    
    return complete_prompt

def demonstrate_crisis_mode():
    """Demonstrate crisis response prompt."""
    print("\n" + "=" * 60)
    print("CRISIS RESPONSE MODE EXAMPLE")
    print("=" * 60)
    
    # Get the crisis response prompt
    crisis_prompt = get_system_prompt('crisis')
    
    print("Crisis Response System Prompt:")
    print("-" * 40)
    print(crisis_prompt)
    print(f"\nPrompt Length: {len(crisis_prompt)} characters")
    
    return crisis_prompt

def demonstrate_wellness_mode():
    """Demonstrate wellness check prompt."""
    print("\n" + "=" * 60)
    print("WELLNESS CHECK MODE EXAMPLE")
    print("=" * 60)
    
    # Get the wellness check prompt
    wellness_prompt = get_system_prompt('wellness')
    
    print("Wellness Check System Prompt:")
    print("-" * 40)
    print(wellness_prompt)
    print(f"\nPrompt Length: {len(wellness_prompt)} characters")
    
    return wellness_prompt

def demonstrate_prompt_utilities():
    """Demonstrate prompt utility functions."""
    print("\n" + "=" * 60)
    print("PROMPT UTILITY FUNCTIONS")
    print("=" * 60)
    
    # Test prompt sanitization
    test_prompt = "```json\nHere's some content with code fences```"
    sanitized = sanitize_prompt(test_prompt)
    print(f"Original prompt: {test_prompt}")
    print(f"Sanitized prompt: {sanitized}")
    
    # Test prompt validation
    long_prompt = "x" * 20000  # Very long prompt
    if validate_prompt_length(long_prompt):
        print("✅ Long prompt is within limits")
    else:
        print("⚠️  Long prompt exceeds recommended limits")
    
    short_prompt = "Short prompt"
    if validate_prompt_length(short_prompt):
        print("✅ Short prompt is within limits")
    else:
        print("⚠️  Short prompt has issues")

def main():
    """Run all demonstration functions."""
    print("SerenityCoach Prompt System Demonstration")
    print("This script shows how to use the comprehensive prompt system")
    
    try:
        # Demonstrate different modes
        motivation_prompt = demonstrate_motivation_mode()
        chat_prompt = demonstrate_chat_mode()
        crisis_prompt = demonstrate_crisis_mode()
        wellness_prompt = demonstrate_wellness_mode()
        
        # Demonstrate utilities
        demonstrate_prompt_utilities()
        
        print("\n" + "=" * 60)
        print("DEMONSTRATION COMPLETE")
        print("=" * 60)
        print("All prompt modes have been demonstrated successfully!")
        print("\nTo use these prompts in your application:")
        print("1. Import the prompts module")
        print("2. Use get_system_prompt() for system instructions")
        print("3. Use build_*_prompt() functions for user prompts")
        print("4. Use format_prompt_for_api() to combine them")
        print("5. Validate and sanitize as needed")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        print("Make sure the prompts.py file is in the same directory")

if __name__ == "__main__":
    main() 