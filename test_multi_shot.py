#!/usr/bin/env python3
"""
Test script for Multi-Shot Prompting Utility

This script tests the basic functionality of the MultiShotPrompter class.
"""

import json
import sys
from multi_shot_prompter import MultiShotPrompter, PromptExample


def test_basic_functionality():
    """Test basic functionality of the MultiShotPrompter."""
    print("🧪 Testing Basic Functionality...")
    
    try:
        # Initialize prompter
        prompter = MultiShotPrompter()
        print("✅ MultiShotPrompter initialized successfully")
        
        # Check example counts
        counts = prompter.get_example_count()
        expected_counts = {"motivation": 5, "chat": 5, "crisis": 3}
        
        for category, expected in expected_counts.items():
            actual = counts[category]
            if actual == expected:
                print(f"✅ {category.title()} examples: {actual}/{expected}")
            else:
                print(f"❌ {category.title()} examples: {actual}/{expected} (expected {expected})")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False


def test_motivation_prompt():
    """Test motivation prompt generation."""
    print("\n🎯 Testing Motivation Prompt Generation...")
    
    try:
        prompter = MultiShotPrompter()
        
        # Generate a motivation prompt
        prompt = prompter.get_motivation_prompt(
            mood="test",
            energy=5,
            stress=5,
            sleep=5,
            hobbies="test",
            time_available=10
        )
        
        # Check if prompt contains expected elements
        required_elements = [
            "SerenityCoach",
            "empathetic",
            "JSON",
            "mood",
            "quote",
            "author",
            "suggested_action"
        ]
        
        for element in required_elements:
            if element in prompt:
                print(f"✅ Prompt contains '{element}'")
            else:
                print(f"❌ Prompt missing '{element}'")
                return False
        
        # Check if prompt contains examples
        if "Example" in prompt and "Examples:" in prompt:
            print("✅ Prompt contains examples section")
        else:
            print("❌ Prompt missing examples section")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Motivation prompt test failed: {e}")
        return False


def test_chat_prompt():
    """Test chat prompt generation."""
    print("\n💬 Testing Chat Prompt Generation...")
    
    try:
        prompter = MultiShotPrompter()
        
        # Generate a chat prompt
        prompt = prompter.get_chat_prompt(
            user_message="test message",
            stress=5,
            energy=5,
            sleep=5,
            time_available=10,
            hobbies="test"
        )
        
        # Check if prompt contains expected elements
        required_elements = [
            "SerenityCoach",
            "empathetic",
            "2-4 short sentences",
            "Examples:"
        ]
        
        for element in required_elements:
            if element in prompt:
                print(f"✅ Prompt contains '{element}'")
            else:
                print(f"❌ Prompt missing '{element}'")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Chat prompt test failed: {e}")
        return False


def test_custom_prompt():
    """Test custom prompt generation."""
    print("\n🎨 Testing Custom Prompt Generation...")
    
    try:
        prompter = MultiShotPrompter()
        
        # Create custom examples
        custom_examples = [
            PromptExample(
                inputs={"test": "value1"},
                output="test output 1",
                description="test example 1"
            ),
            PromptExample(
                inputs={"test": "value2"},
                output="test output 2",
                description="test example 2"
            )
        ]
        
        # Generate custom prompt
        custom_prompt = prompter.get_custom_prompt(
            examples=custom_examples,
            task_description="Test task",
            constraints="Test constraints",
            user_input="test input"
        )
        
        # Check if custom prompt contains expected elements
        required_elements = [
            "Test task",
            "Test constraints",
            "Examples:",
            "test example 1",
            "test example 2",
            "test input"
        ]
        
        for element in required_elements:
            if element in custom_prompt:
                print(f"✅ Custom prompt contains '{element}'")
            else:
                print(f"❌ Custom prompt missing '{element}'")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Custom prompt test failed: {e}")
        return False


def test_adding_examples():
    """Test adding new examples."""
    print("\n➕ Testing Adding Examples...")
    
    try:
        prompter = MultiShotPrompter()
        
        # Get initial count
        initial_count = len(prompter.motivation_examples)
        
        # Create and add new example
        new_example = PromptExample(
            inputs={"mood": "test_mood"},
            output=json.dumps({"test": "data"}),
            description="test description"
        )
        
        prompter.add_example("motivation", new_example)
        
        # Check if count increased
        new_count = len(prompter.motivation_examples)
        if new_count == initial_count + 1:
            print("✅ Example added successfully")
        else:
            print(f"❌ Example count mismatch: {initial_count} -> {new_count}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Adding examples test failed: {e}")
        return False


def test_prompt_example_structure():
    """Test PromptExample dataclass structure."""
    print("\n🏗️ Testing PromptExample Structure...")
    
    try:
        # Create a PromptExample
        example = PromptExample(
            inputs={"key": "value"},
            output="test output",
            description="test description"
        )
        
        # Check attributes
        if example.inputs["key"] == "value":
            print("✅ Inputs attribute working")
        else:
            print("❌ Inputs attribute not working")
            return False
        
        if example.output == "test output":
            print("✅ Output attribute working")
        else:
            print("❌ Output attribute not working")
            return False
        
        if example.description == "test description":
            print("✅ Description attribute working")
        else:
            print("❌ Description attribute not working")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ PromptExample structure test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🚀 Multi-Shot Prompting Utility Test Suite")
    print("=" * 50)
    
    tests = [
        test_basic_functionality,
        test_prompt_example_structure,
        test_motivation_prompt,
        test_chat_prompt,
        test_custom_prompt,
        test_adding_examples
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Multi-shot prompting utility is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 