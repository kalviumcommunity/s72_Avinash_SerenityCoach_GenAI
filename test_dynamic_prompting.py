#!/usr/bin/env python3
"""
Test script for the Dynamic Prompting System

This script tests the core functionality of the dynamic prompting system
without requiring external API calls.
"""

import unittest
from unittest.mock import Mock, patch
import json
import sys
import os

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dynamic_prompter import DynamicPrompter, UserProfile, DynamicContext, Tool


class TestDynamicPrompting(unittest.TestCase):
    """Test cases for the Dynamic Prompting System"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.prompter = DynamicPrompter()
        
        # Create test user profile
        self.test_profile = UserProfile(
            persona="test user",
            expertise_level="intermediate",
            mood="anxious",
            energy=4,
            stress=7,
            sleep_quality=5,
            hobbies=["reading", "music"],
            time_available=30
        )
        
        # Create test context
        self.test_context = DynamicContext(
            memory_summary="User has been anxious for the past few days",
            retrieved_knowledge=["Breathing techniques", "Stress management"],
            recent_activity=["Completed breathing exercise", "Missed morning walk"]
        )
        
        # Create test tools
        self.test_tools = [
            Tool("breathing_exercises", "Stress relief", {}, {}),
            Tool("mood_tracker", "Mood tracking", {}, {}),
            Tool("crisis_resources", "Crisis support", {}, {})
        ]
    
    def test_user_profile_creation(self):
        """Test UserProfile dataclass creation"""
        profile = UserProfile(
            persona="student",
            expertise_level="beginner",
            mood="stressed",
            energy=3,
            stress=8,
            sleep_quality=4,
            hobbies=["gaming"],
            time_available=20
        )
        
        self.assertEqual(profile.persona, "student")
        self.assertEqual(profile.stress, 8)
        self.assertEqual(profile.hobbies, ["gaming"])
        self.assertEqual(profile.preferred_tone, "supportive")  # Default value
    
    def test_dynamic_context_creation(self):
        """Test DynamicContext dataclass creation"""
        context = DynamicContext(
            memory_summary="Test memory",
            retrieved_knowledge=["Knowledge 1", "Knowledge 2"],
            recent_activity=["Activity 1"]
        )
        
        self.assertEqual(context.memory_summary, "Test memory")
        self.assertEqual(len(context.retrieved_knowledge), 2)
        self.assertEqual(len(context.recent_activity), 1)
        self.assertEqual(context.risk_level, "low")  # Default value
    
    def test_tool_creation(self):
        """Test Tool dataclass creation"""
        tool = Tool(
            name="test_tool",
            description="Test description",
            input_schema={"param": "str"},
            output_schema={"result": "str"},
            is_available=True
        )
        
        self.assertEqual(tool.name, "test_tool")
        self.assertEqual(tool.description, "Test description")
        self.assertTrue(tool.is_available)
    
    def test_dynamic_prompt_generation(self):
        """Test dynamic prompt generation"""
        prompt = self.prompter.create_dynamic_prompt(
            mode="motivation",
            user_profile=self.test_profile,
            context=self.test_context,
            available_tools=self.test_tools
        )
        
        # Check that the prompt contains expected elements
        self.assertIn("SerenityCoach", prompt)
        self.assertIn("motivation", prompt)
        self.assertIn("test user", prompt)
        self.assertIn("anxious", prompt)
        self.assertIn("breathing_exercises", prompt)
        self.assertIn("JSON", prompt)
    
    def test_chat_mode_prompt(self):
        """Test chat mode prompt generation"""
        prompt = self.prompter.create_dynamic_prompt(
            mode="chat",
            user_profile=self.test_profile,
            context=self.test_context,
            available_tools=self.test_tools
        )
        
        # Check chat mode specific elements
        self.assertIn("conversation partner", prompt)
        self.assertIn("2–4 sentences", prompt)
        self.assertIn("practical coping strategies", prompt)
    
    def test_crisis_mode_prompt(self):
        """Test crisis mode prompt generation"""
        # Create high-risk context
        crisis_context = DynamicContext(
            memory_summary="User expressed concerning thoughts",
            retrieved_knowledge=["Crisis intervention"],
            recent_activity=["Risk assessment triggered"],
            conversation_history=[
                {"role": "user", "content": "I don't see the point anymore"}
            ]
        )
        
        prompt = self.prompter.create_dynamic_prompt(
            mode="chat",  # Will be automatically changed to crisis
            user_profile=self.test_profile,
            context=crisis_context,
            available_tools=self.test_tools
        )
        
        # Check crisis mode elements
        self.assertIn("crisis intervention specialist", prompt)
        self.assertIn("CRITICAL", prompt)
        self.assertIn("safety guidance", prompt)
    
    def test_risk_assessment(self):
        """Test risk level assessment"""
        # Low risk scenario
        low_risk_context = DynamicContext(
            memory_summary="Normal day",
            retrieved_knowledge=["Wellness tips"],
            recent_activity=["Completed routine"]
        )
        
        risk_level = self.prompter._assess_risk_level(
            self.test_profile, low_risk_context
        )
        self.assertEqual(risk_level, "medium")  # Due to stress=7
        
        # High risk scenario
        high_risk_context = DynamicContext(
            memory_summary="User expressed concerning thoughts",
            conversation_history=[
                {"role": "user", "content": "I want to end it all"}
            ]
        )
        
        risk_level = self.prompter._assess_risk_level(
            self.test_profile, high_risk_context
        )
        self.assertEqual(risk_level, "high")
    
    def test_adaptive_response_plan(self):
        """Test adaptive response plan creation"""
        plan = self.prompter.create_adaptive_response_plan(
            self.test_profile, self.test_context, self.test_tools
        )
        
        # Check plan structure
        self.assertIn("primary_approach", plan)
        self.assertIn("suggested_tools", plan)
        self.assertIn("response_style", plan)
        self.assertIn("safety_measures", plan)
        
        # Check that plan adapts to user state
        self.assertIn("breathing_exercises", plan["suggested_tools"])
        self.assertIn("stress_monitoring", plan["safety_measures"])
    
    def test_conversation_memory(self):
        """Test conversation memory functionality"""
        user_id = "test_user_123"
        
        # Add messages to memory
        self.prompter.add_conversation_memory(
            user_id,
            {"content": "Hello", "role": "user", "mood": "happy"}
        )
        
        self.prompter.add_conversation_memory(
            user_id,
            {"content": "How are you?", "role": "assistant"}
        )
        
        # Get conversation summary
        summary = self.prompter.get_conversation_summary(user_id)
        self.assertIn("Hello", summary)
        self.assertIn("How are you?", summary)
        
        # Check memory limits
        for i in range(25):  # Add more than 20 messages
            self.prompter.add_conversation_memory(
                user_id,
                {"content": f"Message {i}", "role": "user"}
            )
        
        # Should only keep last 20 messages
        summary = self.prompter.get_conversation_summary(user_id)
        self.assertNotIn("Message 0", summary)  # Old message should be removed
    
    def test_user_profile_management(self):
        """Test user profile management"""
        user_id = "profile_test_user"
        
        # Update user profile
        self.prompter.update_user_profile(user_id, self.test_profile)
        
        # Check that profile is stored
        self.assertIn(user_id, self.prompter.user_profiles)
        self.assertEqual(
            self.prompter.user_profiles[user_id].persona,
            "test user"
        )
    
    def test_template_export(self):
        """Test template export functionality"""
        # Export as YAML
        yaml_template = self.prompter.export_prompt_template("motivation", "yaml")
        self.assertIn("mode", yaml_template)
        self.assertIn("motivation", yaml_template)
        
        # Export as JSON
        json_template = self.prompter.export_prompt_template("chat", "json")
        self.assertIn("mode", json_template)
        self.assertIn("chat", json_template)
    
    def test_custom_instructions(self):
        """Test custom instructions in prompts"""
        prompt = self.prompter.create_dynamic_prompt(
            mode="chat",
            user_profile=self.test_profile,
            context=self.test_context,
            available_tools=self.test_tools,
            custom_instructions="Focus on breathing exercises"
        )
        
        self.assertIn("Focus on breathing exercises", prompt)
    
    def test_tool_filtering(self):
        """Test that only available tools are included"""
        # Create some unavailable tools
        unavailable_tools = [
            Tool("broken_tool", "Broken tool", {}, {}, is_available=False),
            Tool("working_tool", "Working tool", {}, {}, is_available=True)
        ]
        
        prompt = self.prompter.create_dynamic_prompt(
            mode="motivation",
            user_profile=self.test_profile,
            context=self.test_context,
            available_tools=unavailable_tools
        )
        
        # Should only include available tools
        self.assertIn("working_tool", prompt)
        self.assertNotIn("broken_tool", prompt)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_end_to_end_workflow(self):
        """Test complete workflow from profile to response plan"""
        prompter = DynamicPrompter()
        
        # Create user profile
        profile = UserProfile(
            persona="busy professional",
            expertise_level="beginner",
            mood="overwhelmed",
            energy=2,
            stress=9,
            sleep_quality=3,
            hobbies=["reading"],
            time_available=15
        )
        
        # Create context
        context = DynamicContext(
            memory_summary="User has been overwhelmed for days",
            retrieved_knowledge=["Stress management", "Time management"],
            recent_activity=["Missed appointments", "Irregular sleep"]
        )
        
        # Create tools
        tools = [
            Tool("breathing_exercises", "Stress relief", {}, {}),
            Tool("crisis_resources", "Crisis support", {}, {})
        ]
        
        # Generate prompt
        prompt = prompter.create_dynamic_prompt("motivation", profile, context, tools)
        
        # Create response plan
        plan = prompter.create_adaptive_response_plan(profile, context, tools)
        
        # Verify integration
        self.assertIn("overwhelmed", prompt)
        self.assertIn("breathing_exercises", prompt)
        self.assertEqual(plan["primary_approach"], "calming")
        self.assertIn("crisis_resources", plan["suggested_tools"])


def run_tests():
    """Run all tests"""
    print("🧪 Running Dynamic Prompting System Tests...")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestDynamicPrompting)
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
        print(f"   Tests run: {result.testsRun}")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
    else:
        print("❌ Some tests failed!")
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"   {test}: {traceback}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"   {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 