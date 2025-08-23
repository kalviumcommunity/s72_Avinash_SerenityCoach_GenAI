#!/usr/bin/env python3
"""
Test script for one-shot prompting functionality.
"""

import json
from prompts import OneShotPrompter, get_motivation_prompt, get_chat_prompt


def test_motivation_prompt():
    """Test motivation mode one-shot prompting."""
    print("🧪 Testing Motivation Mode One-Shot Prompting...")
    
    # Test basic functionality
    prompt = get_motivation_prompt(
        mood="anxious",
        energy=4,
        stress=8,
        sleep=5,
        hobbies="yoga, reading",
        time_available=20
    )
    
    # Check that prompt contains key elements
    assert "You are SerenityCoach" in prompt, "Role definition missing"
    assert "Example output (JSON):" in prompt, "Example section missing"
    assert "mood=\"anxious\"" in prompt, "User mood not included"
    assert "Return only the JSON" in prompt, "Output instruction missing"
    
    print("✅ Motivation prompt test passed!")
    return prompt


def test_chat_prompt():
    """Test chat mode one-shot prompting."""
    print("🧪 Testing Chat Mode One-Shot Prompting...")
    
    # Test basic functionality
    prompt = get_chat_prompt(
        user_message="I'm feeling overwhelmed with work",
        energy=3,
        stress=9,
        sleep=4,
        hobbies="music, walking",
        time_available=15
    )
    
    # Check that prompt contains key elements
    assert "You are SerenityCoach" in prompt, "Role definition missing"
    assert "Example:" in prompt, "Example section missing"
    assert "I'm feeling overwhelmed with work" in prompt, "User message not included"
    assert "Respond in 2-4 sentences" in prompt, "Response instruction missing"
    
    print("✅ Chat prompt test passed!")
    return prompt


def test_prompter_class():
    """Test the OneShotPrompter class."""
    print("🧪 Testing OneShotPrompter Class...")
    
    prompter = OneShotPrompter()
    
    # Check that examples are properly defined
    assert "mood" in prompter.motivation_example, "Motivation example missing mood"
    assert "quote" in prompter.motivation_example, "Motivation example missing quote"
    assert "user_message" in prompter.chat_example, "Chat example missing user message"
    assert "assistant_response" in prompter.chat_example, "Chat example missing assistant response"
    
    print("✅ OneShotPrompter class test passed!")


def test_prompt_structure():
    """Test that prompts have proper structure."""
    print("🧪 Testing Prompt Structure...")
    
    # Test motivation prompt structure
    motivation_prompt = get_motivation_prompt(
        mood="tired",
        energy=2,
        stress=6,
        sleep=3,
        hobbies="",
        time_available=10
    )
    
    # Check structure components
    sections = [
        "You are SerenityCoach",
        "Task:",
        "Constraints:",
        "Format:",
        "Example inputs:",
        "Example output (JSON):",
        "Now generate the JSON for these inputs:",
        "Return only the JSON"
    ]
    
    for section in sections:
        assert section in motivation_prompt, f"Missing section: {section}"
    
    print("✅ Prompt structure test passed!")


def test_safety_integration():
    """Test that safety considerations are included in prompts."""
    print("🧪 Testing Safety Integration...")
    
    # Test motivation prompt with high stress
    prompt = get_motivation_prompt(
        mood="overwhelmed",
        energy=2,
        stress=9,  # High stress
        sleep=2,
        hobbies="",
        time_available=5
    )
    
    # Check safety elements
    assert "risk keywords" in prompt.lower(), "Risk detection missing"
    assert "safety note" in prompt.lower(), "Safety note missing"
    assert "helplines" in prompt.lower(), "Helpline reference missing"
    
    print("✅ Safety integration test passed!")


def test_custom_prompts():
    """Test custom prompt creation."""
    print("🧪 Testing Custom Prompt Creation...")
    
    prompter = OneShotPrompter()
    
    # Create a custom journaling prompt
    custom_prompt = f"""You are SerenityCoach, helping users with journaling prompts.
Task: Generate a reflective journaling question based on the user's mood.

Example:
User mood: "stressed"
Journaling question: "What's one small thing that brought you joy today, even in the midst of stress?"

Now generate a journaling question for:
User mood: "grateful"

Return only the question:"""
    
    # Check custom prompt structure
    assert "Example:" in custom_prompt, "Custom prompt missing example"
    assert "User mood: \"grateful\"" in custom_prompt, "Custom prompt missing user input"
    assert "Return only the question" in custom_prompt, "Custom prompt missing output instruction"
    
    print("✅ Custom prompt test passed!")


def run_all_tests():
    """Run all tests."""
    print("🚀 Running One-Shot Prompting Tests...")
    print("=" * 50)
    
    try:
        test_prompter_class()
        test_motivation_prompt()
        test_chat_prompt()
        test_prompt_structure()
        test_safety_integration()
        test_custom_prompts()
        
        print("\n🎉 All tests passed successfully!")
        print("=" * 50)
        print("The one-shot prompting implementation is working correctly.")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False
    
    return True


if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print("\n✨ Ready to use! Run 'python main.py' to start SerenityCoach.")
    else:
        print("\n🔧 Please fix the issues before proceeding.")
        exit(1) 