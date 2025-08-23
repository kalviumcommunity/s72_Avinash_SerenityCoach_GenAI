#!/usr/bin/env python3
"""
SerenityCoach - Mental Health Companion CLI
Main application integrating multi-shot prompting for improved AI responses.
"""

import os
import json
import argparse
import sys
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from multi_shot_prompter import MultiShotPrompter

# Load environment variables
load_dotenv()

class SerenityCoach:
    """Main SerenityCoach application with multi-shot prompting."""
    
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            print("❌ Error: GOOGLE_API_KEY not found in environment variables.")
            print("Please set it in your .env file or environment variables.")
            sys.exit(1)
        
        self.prompter = MultiShotPrompter()
        self.risk_keywords = [
            "kill myself", "end it all", "don't want to live", "suicide",
            "self-harm", "hurt myself", "want to die", "better off dead"
        ]
        
        # Initialize Google AI (placeholder - you'll need to implement this)
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.ai_available = True
        except ImportError:
            print("⚠️  Warning: google-generativeai not available. Using fallback responses.")
            self.ai_available = False
        except Exception as e:
            print(f"⚠️  Warning: AI initialization failed: {e}")
            self.ai_available = False
    
    def detect_risk(self, text: str) -> bool:
        """Detect potential risk phrases in user input."""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in self.risk_keywords)
    
    def get_motivation_response(self, mood: str, energy: int = 5, stress: int = 5,
                               sleep: int = 5, hobbies: str = "", time_available: int = 10) -> Dict[str, Any]:
        """Get motivational response using multi-shot prompting."""
        if not self.ai_available:
            return self._get_fallback_motivation(mood, stress)
        
        try:
            # Generate multi-shot prompt
            prompt = self.prompter.get_motivation_prompt(
                mood=mood, energy=energy, stress=stress, 
                sleep=sleep, hobbies=hobbies, time_available=time_available
            )
            
            # Get AI response
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Parse JSON response
            try:
                result = json.loads(response_text)
                # Validate required fields
                required_fields = ['mood', 'quote', 'author', 'suggested_action']
                if all(field in result for field in required_fields):
                    return result
                else:
                    print("⚠️  AI response missing required fields, using fallback")
                    return self._get_fallback_motivation(mood, stress)
            except json.JSONDecodeError:
                print("⚠️  AI response not valid JSON, using fallback")
                return self._get_fallback_motivation(mood, stress)
                
        except Exception as e:
            print(f"⚠️  AI request failed: {e}")
            return self._get_fallback_motivation(mood, stress)
    
    def get_chat_response(self, user_message: str, stress: int = 5, energy: int = 5,
                          sleep: int = 5, time_available: int = 10, hobbies: str = "") -> str:
        """Get chat response using multi-shot prompting."""
        # Check for risk first
        if self.detect_risk(user_message):
            return self._get_crisis_response(user_message)
        
        if not self.ai_available:
            return self._get_fallback_chat(user_message, stress)
        
        try:
            # Generate multi-shot prompt
            prompt = self.prompter.get_chat_prompt(
                user_message=user_message, stress=stress, energy=energy,
                sleep=sleep, time_available=time_available, hobbies=hobbies
            )
            
            # Get AI response
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"⚠️  AI request failed: {e}")
            return self._get_fallback_chat(user_message, stress)
    
    def _get_fallback_motivation(self, mood: str, stress: int) -> Dict[str, Any]:
        """Fallback motivation response when AI is unavailable."""
        fallback_quotes = {
            "tired": {
                "quote": "Rest is productive when it helps you return with clarity.",
                "author": "Unknown",
                "suggested_action": "Take a short walk and hydrate."
            },
            "anxious": {
                "quote": "Feelings are waves; you can ride them without being swept away.",
                "author": "Unknown",
                "suggested_action": "Try deep breathing for 2 minutes."
            },
            "overwhelmed": {
                "quote": "You don't have to do it all today; just the next right thing.",
                "author": "Unknown",
                "suggested_action": "List one small step you can take now."
            }
        }
        
        quote_data = fallback_quotes.get(mood.lower(), fallback_quotes["tired"])
        
        result = {
            "mood": mood,
            "quote": quote_data["quote"],
            "author": quote_data["author"],
            "suggested_action": quote_data["suggested_action"]
        }
        
        if stress >= 8:
            result["resources"] = "If you feel unsafe, consider reaching out to someone you trust or a local helpline."
        
        return result
    
    def _get_fallback_chat(self, user_message: str, stress: int) -> str:
        """Fallback chat response when AI is unavailable."""
        if "tired" in user_message.lower() or "exhausted" in user_message.lower():
            return "It sounds like you're really worn out. Try taking a short break, maybe 5 minutes of deep breathing or a quick walk. What's one small thing that usually helps you recharge?"
        elif "anxious" in user_message.lower() or "worried" in user_message.lower():
            return "Anxiety can feel really overwhelming. Try the 5-4-3-2-1 grounding technique: name 5 things you see, 4 you feel, 3 you hear, 2 you smell, 1 you taste. What's one thing you can see right now?"
        elif "sad" in user_message.lower() or "down" in user_message.lower():
            return "I'm sorry you're feeling down. It's okay to not be okay. Maybe try writing down one thing you're grateful for, or reach out to someone you trust. What usually helps lift your spirits a little?"
        else:
            return "Thanks for sharing that with me. It sounds like you're going through a challenging time. What's one small thing you could do right now to take care of yourself?"
    
    def _get_crisis_response(self, user_message: str) -> str:
        """Response for crisis situations."""
        return """I'm really concerned about what you're going through. You matter, and you deserve help.

Please reach out to someone you trust right now, or call a crisis helpline. You don't have to face this alone.

If you're in the US, you can call 988 (Suicide & Crisis Lifeline) or text HOME to 741741 (Crisis Text Line).

You're not alone in this, and there are people who want to help you."""

    def save_output(self, output: Dict[str, Any], filename: str = "last_output.json"):
        """Save the last output to a JSON file."""
        try:
            with open(filename, 'w') as f:
                json.dump(output, f, indent=2)
            print(f"💾 Output saved to {filename}")
        except Exception as e:
            print(f"⚠️  Could not save output: {e}")

    def run_motivation_mode(self, mood: Optional[str] = None):
        """Run the motivation mode with multi-shot prompting."""
        print("🌟 Welcome to SerenityCoach Motivation Mode!")
        print("I'll help you find motivation and actionable steps based on how you're feeling.\n")
        
        if not mood:
            mood = input("How are you feeling today? ").strip()
            if not mood:
                print("❌ Please provide a mood to continue.")
                return
        
        print(f"\n📊 Let me get to know you better to provide personalized support...")
        
        # Get additional context
        try:
            energy = int(input("Energy level (1-10, where 1=exhausted, 10=energized): ") or "5")
            stress = int(input("Stress level (1-10, where 1=calm, 10=overwhelmed): ") or "5")
            sleep = int(input("Sleep quality last night (1-10, where 1=poor, 10=excellent): ") or "5")
            hobbies = input("What are your hobbies/interests? (optional): ").strip() or ""
            time_available = int(input("How many minutes do you have available? (optional, default 10): ") or "10")
        except ValueError:
            print("⚠️  Using default values for invalid inputs.")
            energy, stress, sleep, time_available = 5, 5, 5, 10
            hobbies = ""
        
        print(f"\n🔄 Generating personalized motivation for '{mood}'...")
        
        # Get response using multi-shot prompting
        response = self.get_motivation_response(
            mood=mood, energy=energy, stress=stress, 
            sleep=sleep, hobbies=hobbies, time_available=time_available
        )
        
        # Display response
        print(f"\n✨ Here's your personalized motivation:")
        print(f"📝 Quote: \"{response['quote']}\"")
        print(f"👤 Author: {response['author']}")
        print(f"🎯 Suggested Action: {response['suggested_action']}")
        
        # Display optional fields
        if 'hobby_suggestion' in response:
            print(f"🎨 Hobby Tip: {response['hobby_suggestion']}")
        if 'challenge' in response:
            print(f"🏆 Micro-Challenge: {response['challenge']}")
        if 'breathing_exercise' in response:
            print(f"🫁 Breathing Exercise: {response['breathing_exercise']}")
        if 'grounding_exercise' in response:
            print(f"🌍 Grounding Exercise: {response['grounding_exercise']}")
        if 'joke' in response:
            print(f"😄 Joke: {response['joke']}")
        if 'affirmation' in response:
            print(f"💝 Affirmation: {response['affirmation']}")
        if 'resources' in response:
            print(f"🆘 Safety Note: {response['resources']}")
        
        # Save output
        self.save_output(response)
        
        print(f"\n💡 Multi-shot prompting used {self.prompter.get_example_count()['motivation']} examples to generate this response.")

    def run_chat_mode(self):
        """Run the live chat mode with multi-shot prompting."""
        print("💬 Welcome to SerenityCoach Live Chat Mode!")
        print("I'm here to listen and provide supportive conversation.")
        print("Type 'exit' to quit.\n")
        
        print("💡 Multi-shot prompting active with examples for various scenarios.")
        print(f"📚 Available examples: {self.prompter.get_example_count()['chat']} chat, {self.prompter.get_example_count()['crisis']} crisis\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("👋 Take care! Remember, you're not alone.")
                    break
                
                if not user_input:
                    continue
                
                # Get context for better responses
                stress = 5  # Default values
                energy = 5
                sleep = 5
                time_available = 10
                hobbies = ""
                
                print("🤖 SerenityCoach: ", end="")
                response = self.get_chat_response(
                    user_input, stress, energy, sleep, time_available, hobbies
                )
                print(response)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Take care! Remember, you're not alone.")
                break
            except Exception as e:
                print(f"⚠️  Error: {e}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SerenityCoach - Mental Health Companion with Multi-shot Prompting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive motivation mode
  python main.py --mood "tired"     # Quick motivation for tired mood
  python main.py --chat             # Live chat mode
  python main.py --examples         # Show multi-shot prompting examples
        """
    )
    
    parser.add_argument('--mood', help='Specify mood for motivation mode')
    parser.add_argument('--chat', action='store_true', help='Start live chat mode')
    parser.add_argument('--examples', action='store_true', help='Show multi-shot prompting examples')
    parser.add_argument('--temperature', type=float, default=0.7, help='AI response creativity (0.0-1.0)')
    parser.add_argument('--top-k', type=int, default=40, help='AI response diversity')
    parser.add_argument('--top-p', type=float, default=0.95, help='AI response focus')
    
    args = parser.parse_args()
    
    try:
        coach = SerenityCoach()
        
        if args.examples:
            print("📚 Multi-shot Prompting Examples in SerenityCoach:")
            print(f"🎯 Motivation examples: {coach.prompter.get_example_count()['motivation']}")
            print(f"💬 Chat examples: {coach.prompter.get_example_count()['chat']}")
            print(f"🆘 Crisis examples: {coach.prompter.get_example_count()['crisis']}")
            
            print("\n🔍 Example motivation prompt structure:")
            example_prompt = coach.prompter.get_motivation_prompt("anxious", 4, 7, 5, "art", 5)
            print(example_prompt[:500] + "..." if len(example_prompt) > 500 else example_prompt)
            return
        
        if args.chat:
            coach.run_chat_mode()
        else:
            coach.run_motivation_mode(args.mood)
            
    except KeyboardInterrupt:
        print("\n👋 Take care!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 