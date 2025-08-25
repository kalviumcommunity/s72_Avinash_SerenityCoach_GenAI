#!/usr/bin/env python3
"""
Dynamic Prompting Demonstration Script

This script demonstrates the various capabilities of the dynamic prompting system
by showing how prompts adapt based on different user profiles and contexts.
"""

import json
from dynamic_prompter import DynamicPrompter, UserProfile, DynamicContext, Tool


def demo_basic_dynamic_prompting():
    """Demonstrate basic dynamic prompting with different user profiles"""
    print("=" * 60)
    print("DEMO 1: Basic Dynamic Prompting")
    print("=" * 60)
    
    prompter = DynamicPrompter()
    
    # Create different user profiles
    profiles = {
        "high_stress_professional": UserProfile(
            persona="busy executive",
            expertise_level="beginner",
            mood="overwhelmed",
            energy=2,
            stress=9,
            sleep_quality=3,
            hobbies=["golf", "reading"],
            time_available=15
        ),
        "low_energy_student": UserProfile(
            persona="college student",
            expertise_level="intermediate",
            mood="tired",
            energy=1,
            stress=6,
            sleep_quality=2,
            hobbies=["gaming", "music"],
            time_available=45
        ),
        "balanced_parent": UserProfile(
            persona="working parent",
            expertise_level="advanced",
            mood="content",
            energy=7,
            stress=4,
            sleep_quality=7,
            hobbies=["yoga", "cooking"],
            time_available=30
        )
    }
    
    # Available tools
    tools = [
        Tool("breathing_exercises", "Stress relief techniques", {}, {}),
        Tool("mood_tracker", "Mood pattern analysis", {}, {}),
        Tool("micro_actions", "Quick wellness activities", {}, {})
    ]
    
    # Generate prompts for each profile
    for profile_name, profile in profiles.items():
        print(f"\n📋 User Profile: {profile_name}")
        print(f"   Mood: {profile.mood}, Stress: {profile.stress}/10, Energy: {profile.energy}/10")
        
        context = DynamicContext(
            memory_summary=f"User has been {profile.mood} for the past few days",
            retrieved_knowledge=["Basic wellness practices", "Stress management techniques"],
            recent_activity=["Completed daily check-in", "Used breathing exercise"]
        )
        
        # Generate motivation mode prompt
        prompt = prompter.create_dynamic_prompt("motivation", profile, context, tools)
        
        print(f"\n🎯 Generated Prompt Preview (first 200 chars):")
        print(f"   {prompt[:200]}...")
        
        # Show adaptive response plan
        plan = prompter.create_adaptive_response_plan(profile, context, tools)
        print(f"\n📊 Adaptive Response Plan:")
        print(f"   Primary Approach: {plan['primary_approach']}")
        print(f"   Response Style: {plan['response_style']}")
        print(f"   Suggested Tools: {', '.join(plan['suggested_tools'])}")
        print(f"   Safety Measures: {', '.join(plan['safety_measures'])}")


def demo_context_adaptation():
    """Demonstrate how context affects prompt generation"""
    print("\n" + "=" * 60)
    print("DEMO 2: Context Adaptation")
    print("=" * 60)
    
    prompter = DynamicPrompter()
    
    # Base user profile
    user = UserProfile(
        persona="remote worker",
        expertise_level="intermediate",
        mood="anxious",
        energy=5,
        stress=7,
        sleep_quality=6,
        hobbies=["photography", "hiking"],
        time_available=25
    )
    
    # Different contexts
    contexts = {
        "normal_day": DynamicContext(
            memory_summary="User had a productive morning",
            retrieved_knowledge=["Mindfulness techniques", "Work-life balance tips"],
            recent_activity=["Completed morning routine", "Had healthy breakfast"]
        ),
        "stressful_week": DynamicContext(
            memory_summary="User has been under high pressure for 5 days",
            retrieved_knowledge=["Burnout prevention", "Stress management"],
            recent_activity=["Missed exercise sessions", "Irregular sleep pattern"],
            conversation_history=[
                {"role": "user", "content": "I feel like I'm drowning in work"},
                {"role": "assistant", "content": "That sounds really overwhelming. Let's break this down."}
            ]
        ),
        "crisis_situation": DynamicContext(
            memory_summary="User expressed concerning thoughts",
            retrieved_knowledge=["Crisis intervention", "Emergency resources"],
            recent_activity=["User mentioned feeling hopeless", "Risk assessment triggered"],
            conversation_history=[
                {"role": "user", "content": "I don't see the point anymore"},
                {"role": "assistant", "content": "I'm here with you. Let's talk about this."}
            ]
        )
    }
    
    tools = [Tool("crisis_resources", "Emergency support", {}, {})]
    
    for context_name, context in contexts.items():
        print(f"\n🔄 Context: {context_name}")
        
        # Assess risk level
        risk_level = prompter._assess_risk_level(user, context)
        print(f"   Risk Level: {risk_level.upper()}")
        
        # Generate prompt
        prompt = prompter.create_dynamic_prompt("chat", user, context, tools)
        
        print(f"   Prompt Mode: {'crisis' if risk_level == 'high' else 'chat'}")
        print(f"   Safety Measures: {'⚠️ CRITICAL' if risk_level == 'high' else 'Standard'}")


def demo_tool_integration():
    """Demonstrate how available tools affect prompt generation"""
    print("\n" + "=" * 60)
    print("DEMO 3: Tool Integration")
    print("=" * 60)
    
    prompter = DynamicPrompter()
    
    user = UserProfile(
        persona="fitness enthusiast",
        expertise_level="advanced",
        mood="motivated",
        energy=8,
        stress=3,
        sleep_quality=8,
        hobbies=["running", "weightlifting"],
        time_available=60
    )
    
    context = DynamicContext(
        memory_summary="User completed a challenging workout",
        retrieved_knowledge=["Recovery techniques", "Performance optimization"],
        recent_activity=["Ran 10km", "Lifted weights", "Stretching routine"]
    )
    
    # Different tool configurations
    tool_configs = {
        "basic_tools": [
            Tool("breathing_exercises", "Basic breathing", {}, {}),
            Tool("mood_tracker", "Simple tracking", {}, {})
        ],
        "advanced_tools": [
            Tool("breathing_exercises", "Advanced breathing", {}, {}),
            Tool("mood_tracker", "Comprehensive tracking", {}, {}),
            Tool("performance_analyzer", "Workout analysis", {}, {}),
            Tool("recovery_planner", "Recovery optimization", {}, {}),
            Tool("nutrition_advisor", "Nutrition guidance", {}, {})
        ],
        "specialized_tools": [
            Tool("athlete_coach", "Sports psychology", {}, {}),
            Tool("injury_prevention", "Prevention protocols", {}, {}),
            Tool("competition_prep", "Competition readiness", {}, {})
        ]
    }
    
    for config_name, tools in tool_configs.items():
        print(f"\n🛠️  Tool Configuration: {config_name}")
        print(f"   Available Tools: {len(tools)}")
        
        # Generate prompt
        prompt = prompter.create_dynamic_prompt("motivation", user, context, tools)
        
        # Count tool mentions in prompt
        tool_mentions = sum(1 for tool in tools if tool.name in prompt)
        print(f"   Tools Referenced: {tool_mentions}")
        
        # Show adaptive plan
        plan = prompter.create_adaptive_response_plan(user, context, tools)
        print(f"   Suggested Tools: {', '.join(plan['suggested_tools'])}")


def demo_memory_and_learning():
    """Demonstrate conversation memory and learning capabilities"""
    print("\n" + "=" * 60)
    print("DEMO 4: Memory and Learning")
    print("=" * 60)
    
    prompter = DynamicPrompter()
    user_id = "demo_user"
    
    # Simulate conversation history
    conversation_messages = [
        {"role": "user", "content": "I'm feeling really stressed about my presentation tomorrow"},
        {"role": "assistant", "content": "Presentations can be nerve-wracking. Let's work on some calming techniques."},
        {"role": "user", "content": "I tried the breathing exercise you suggested, it helped a bit"},
        {"role": "assistant", "content": "Great! Breathing exercises are excellent for managing presentation anxiety."},
        {"role": "user", "content": "But I'm still worried I'll forget what to say"},
        {"role": "assistant", "content": "That's a common fear. Let me suggest some memory techniques."},
        {"role": "user", "content": "I'm feeling a bit better now, thanks"},
        {"role": "assistant", "content": "You're welcome! Remember, preparation and practice build confidence."}
    ]
    
    # Add messages to memory
    for msg in conversation_messages:
        prompter.add_conversation_memory(user_id, msg)
    
    # Get conversation summary
    summary = prompter.get_conversation_summary(user_id)
    print(f"📝 Conversation Summary:")
    print(f"   {summary}")
    
    # Show how memory affects context
    user = UserProfile(
        persona="anxious presenter",
        expertise_level="beginner",
        mood="nervous",
        energy=6,
        stress=8,
        sleep_quality=5,
        hobbies=["reading", "puzzles"],
        time_available=20
    )
    
    context = DynamicContext(
        memory_summary=summary,
        retrieved_knowledge=["Presentation anxiety techniques", "Memory improvement strategies"],
        recent_activity=["Used breathing exercises", "Practiced presentation"]
    )
    
    tools = [Tool("anxiety_tools", "Anxiety management", {}, {})]
    
    # Generate prompt with memory context
    prompt = prompter.create_dynamic_prompt("chat", user, context, tools)
    
    print(f"\n🧠 Memory-Enhanced Prompt Preview:")
    print(f"   {prompt[:300]}...")


def demo_export_and_templates():
    """Demonstrate template export functionality"""
    print("\n" + "=" * 60)
    print("DEMO 5: Template Export")
    print("=" * 60)
    
    prompter = DynamicPrompter()
    
    # Export different template formats
    modes = ["motivation", "chat", "crisis"]
    
    for mode in modes:
        print(f"\n📋 Template for {mode.upper()} mode:")
        
        # Export as YAML
        yaml_template = prompter.export_prompt_template(mode, "yaml")
        print(f"   YAML format (first 200 chars):")
        print(f"   {yaml_template[:200]}...")
        
        # Export as JSON
        json_template = prompter.export_prompt_template(mode, "json")
        print(f"   JSON format (first 200 chars):")
        print(f"   {json_template[:200]}...")


def main():
    """Run all demonstrations"""
    print("🚀 SERENITYCOACH DYNAMIC PROMPTING DEMONSTRATION")
    print("This script showcases the adaptive capabilities of our dynamic prompting system.\n")
    
    try:
        demo_basic_dynamic_prompting()
        demo_context_adaptation()
        demo_tool_integration()
        demo_memory_and_learning()
        demo_export_and_templates()
        
        print("\n" + "=" * 60)
        print("✅ DEMONSTRATION COMPLETE!")
        print("=" * 60)
        print("\nKey Features Demonstrated:")
        print("• Context-aware prompt generation")
        print("• User profile adaptation")
        print("• Risk assessment and safety measures")
        print("• Tool availability integration")
        print("• Conversation memory and learning")
        print("• Template export capabilities")
        print("\nThe dynamic prompting system automatically adapts to:")
        print("• User's current emotional state")
        print("• Available time and energy")
        print("• Risk indicators and safety needs")
        print("• Available tools and resources")
        print("• Conversation history and context")
        
    except Exception as e:
        print(f"\n❌ Error during demonstration: {str(e)}")
        print("Please ensure all dependencies are installed and the dynamic_prompter module is available.")


if __name__ == "__main__":
    main() 