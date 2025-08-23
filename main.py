#!/usr/bin/env python3
"""
SerenityCoach - Mental Health Companion CLI
Uses one-shot prompting for consistent, empathetic responses.
"""

import os
import json
import argparse
import sys
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Import our one-shot prompting utilities
from prompts import OneShotPrompter, get_motivation_prompt, get_chat_prompt, get_risk_assessment_prompt

# Load environment variables
load_dotenv()

# Risk keywords for safety detection
RISK_KEYWORDS = [
    "suicide", "kill myself", "end it all", "want to die", "better off dead",
    "self-harm", "cut myself", "hurt myself", "no reason to live", "give up"
]


class SerenityCoach:
    """Main SerenityCoach application class."""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
            print("Please set it in your .env file or as an environment variable.")
            sys.exit(1)
        
        self.prompter = OneShotPrompter()
        self.last_output = {}
        
    def simulate_ai_response(self, prompt: str, mode: str = "motivation") -> str:
        """
        Simulate AI response for demonstration purposes.
        In a real implementation, this would call the Google Gemini API.
        """
        if mode == "motivation":
            # Simulate JSON response for motivation mode
            return json.dumps({
                "mood": "tired",
                "quote": "Rest if you must, but don't you quit.",
                "author": "Unknown",
                "suggested_action": "Take a short walk and hydrate.",
                "breathing_exercise": "Inhale for 4, hold for 4, exhale for 4.",
                "resources": "Remember, it's okay to take breaks and ask for help when needed."
            }, indent=2)
        else:
            # Simulate text response for chat mode
            return "I hear you, and it sounds like you're going through a challenging time. Remember that small steps forward are still progress. What's one tiny thing you could do right now to take care of yourself?"
    
    def get_user_input(self, prompt: str, input_type: str = "text") -> Any:
        """Get user input with validation."""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("Please provide a response.")
                    continue
                
                if input_type == "int":
                    value = int(user_input)
                    if 1 <= value <= 10:
                        return value
                    else:
                        print("Please enter a number between 1 and 10.")
                else:
                    return user_input
            except ValueError:
                print("Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\nGoodbye! Take care of yourself.")
                sys.exit(0)
    
    def assess_risk(self, message: str) -> Dict[str, Any]:
        """Assess message for risk indicators."""
        risk_level = "low"
        keywords_detected = []
        
        message_lower = message.lower()
        for keyword in RISK_KEYWORDS:
            if keyword in message_lower:
                keywords_detected.append(keyword)
                risk_level = "high"
                break
        
        if risk_level == "high":
            return {
                "risk_level": "high",
                "keywords_detected": keywords_detected,
                "response_type": "safety_note",
                "safety_message": "I'm concerned about what you're sharing. Please know that you're not alone and there are people who care about you. Consider reaching out to someone you trust or a local helpline for immediate support."
            }
        
        return {
            "risk_level": "low",
            "keywords_detected": [],
            "response_type": "normal",
            "safety_message": ""
        }
    
    def motivation_mode(self, mood: Optional[str] = None):
        """Run motivation mode with one-shot prompting."""
        print("🌟 Welcome to SerenityCoach Motivation Mode!")
        print("=" * 50)
        
        # Get mood if not provided
        if not mood:
            mood = self.get_user_input("How are you feeling today? ")
        
        print(f"\nMood: {mood}")
        
        # Get optional context
        print("\nLet's get some context to personalize your experience:")
        energy = self.get_user_input("Energy level (1-10, where 1=tired, 10=energized): ", "int")
        stress = self.get_user_input("Stress level (1-10, where 1=calm, 10=overwhelmed): ", "int")
        sleep = self.get_user_input("Sleep quality (1-10, where 1=poor, 10=excellent): ", "int")
        hobbies = self.get_user_input("What are your hobbies? (comma-separated, or press Enter to skip): ")
        time_available = self.get_user_input("Time available in minutes: ", "int")
        
        # Create one-shot prompt
        prompt = get_motivation_prompt(
            mood=mood,
            energy=energy,
            stress=stress,
            sleep=sleep,
            hobbies=hobbies,
            time_available=time_available
        )
        
        print("\n🤖 Generating personalized motivation...")
        print("-" * 50)
        
        # Get AI response (simulated for demo)
        response = self.simulate_ai_response(prompt, "motivation")
        
        try:
            response_data = json.loads(response)
            self.display_motivation(response_data)
            
            # Save to last_output.json
            self.last_output = response_data
            with open('last_output.json', 'w') as f:
                json.dump(response_data, f, indent=2)
            
        except json.JSONDecodeError:
            print("❌ Error: Could not parse AI response.")
            print("Raw response:", response)
    
    def display_motivation(self, data: Dict[str, Any]):
        """Display motivation response in a formatted way."""
        print(f"\n💭 Mood: {data.get('mood', 'N/A')}")
        print(f"💬 Quote: \"{data.get('quote', 'N/A')}\"")
        print(f"✍️  Author: {data.get('author', 'N/A')}")
        print(f"🎯 Suggested Action: {data.get('suggested_action', 'N/A')}")
        
        if data.get('breathing_exercise'):
            print(f"🫁 Breathing Exercise: {data.get('breathing_exercise')}")
        
        if data.get('resources'):
            print(f"🆘 Resources: {data.get('resources')}")
        
        if data.get('hobby_suggestion'):
            print(f"🎨 Hobby Suggestion: {data.get('hobby_suggestion')}")
        
        if data.get('challenge'):
            print(f"🏆 Micro-Challenge: {data.get('challenge')}")
    
    def chat_mode(self):
        """Run live chat mode with one-shot prompting."""
        print("💬 Welcome to SerenityCoach Live Chat Mode!")
        print("Type 'exit' to quit.")
        print("=" * 50)
        
        while True:
            try:
                user_message = input("\nYou: ").strip()
                
                if user_message.lower() in ['exit', 'quit', 'bye']:
                    print("👋 Goodbye! Take care of yourself.")
                    break
                
                if not user_message:
                    continue
                
                # Assess risk first
                risk_assessment = self.assess_risk(user_message)
                
                # Create one-shot prompt for chat
                prompt = get_chat_prompt(user_message)
                
                # Get AI response (simulated for demo)
                response = self.simulate_ai_response(prompt, "chat")
                
                print(f"\n🤖 SerenityCoach: {response}")
                
                # Add safety note if needed
                if risk_assessment['risk_level'] == 'high':
                    print(f"\n⚠️  Safety Note: {risk_assessment['safety_message']}")
                
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Take care of yourself.")
                break
    
    def run(self):
        """Main application entry point."""
        parser = argparse.ArgumentParser(description='SerenityCoach - Mental Health Companion')
        parser.add_argument('--chat', action='store_true', help='Start live chat mode')
        parser.add_argument('--mood', type=str, help='Specify mood for motivation mode')
        parser.add_argument('--temperature', type=float, default=0.7, help='AI response creativity (0.0-1.0)')
        parser.add_argument('--top_k', type=int, default=40, help='Top-k sampling parameter')
        parser.add_argument('--top_p', type=float, default=0.95, help='Top-p sampling parameter')
        
        args = parser.parse_args()
        
        try:
            if args.chat:
                self.chat_mode()
            else:
                self.motivation_mode(args.mood)
                
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            sys.exit(1)


def main():
    """Main function."""
    coach = SerenityCoach()
    coach.run()


if __name__ == "__main__":
    main() 