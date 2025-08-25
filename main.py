#!/usr/bin/env python3
"""
SerenityCoach - Mental Health Companion with Dynamic Prompting

A CLI-based AI companion that supports mental wellbeing through empathetic conversation
and personalized micro-actions, utilizing dynamic prompting for adaptive responses.
"""

import os
import json
import argparse
from typing import Dict, List, Optional
from dotenv import load_dotenv
import google.generativeai as genai
from colorama import init, Fore, Style
from dynamic_prompter import DynamicPrompter, UserProfile, DynamicContext, Tool

# Initialize colorama for cross-platform colored output
init(autoreset=True)

class SerenityCoach:
    """
    Main SerenityCoach application with dynamic prompting integration
    """
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Initialize Google Generative AI
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Initialize dynamic prompter
        self.dynamic_prompter = DynamicPrompter()
        
        # Initialize available tools
        self.available_tools = self._initialize_tools()
        
        # User session data
        self.current_user_id = "default_user"
        self.user_profile = None
        self.conversation_context = None
        
        # Risk detection keywords
        self.risk_keywords = [
            "suicide", "kill myself", "end it all", "want to die",
            "self-harm", "cut myself", "overdose", "no reason to live",
            "better off dead", "can't take it anymore"
        ]
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize available tools for the AI assistant"""
        return [
            Tool(
                name="breathing_exercises",
                description="Guided breathing techniques for stress relief",
                input_schema={"technique": "str", "duration": "int"},
                output_schema={"instructions": "str", "benefits": "str"}
            ),
            Tool(
                name="mood_tracker",
                description="Track and analyze mood patterns over time",
                input_schema={"mood": "str", "timestamp": "datetime"},
                output_schema={"pattern": "str", "suggestion": "str"}
            ),
            Tool(
                name="crisis_resources",
                description="Emergency mental health resources and helplines",
                input_schema={"location": "str", "urgency": "str"},
                output_schema={"resources": "list", "immediate_actions": "list"}
            ),
            Tool(
                name="micro_actions",
                description="Quick, actionable wellness activities",
                input_schema={"time_available": "int", "energy_level": "int"},
                output_schema={"actions": "list", "estimated_time": "int"}
            ),
            Tool(
                name="hobby_integration",
                description="Integrate wellness activities with user hobbies",
                input_schema={"hobbies": "list", "wellness_goal": "str"},
                output_schema={"integrated_activities": "list", "motivation_tips": "list"}
            )
        ]
    
    def _get_user_input(self, prompt: str, validation_func=None) -> str:
        """Get user input with optional validation"""
        while True:
            user_input = input(f"{Fore.CYAN}{prompt}{Style.RESET_ALL} ").strip()
            if validation_func and not validation_func(user_input):
                print(f"{Fore.RED}Invalid input. Please try again.{Style.RESET_ALL}")
                continue
            return user_input
    
    def _validate_scale(self, value: str, min_val: int = 1, max_val: int = 10) -> bool:
        """Validate scale input (1-10)"""
        try:
            num = int(value)
            return min_val <= num <= max_val
        except ValueError:
            return False
    
    def _collect_user_profile(self) -> UserProfile:
        """Collect user profile information interactively"""
        print(f"\n{Fore.GREEN}=== Welcome to SerenityCoach ==={Style.RESET_ALL}")
        print("Let me get to know you better to provide personalized support.\n")
        
        # Basic persona and expertise
        persona = self._get_user_input("What best describes you? (e.g., 'busy professional', 'student', 'parent'): ")
        expertise = self._get_user_input("How familiar are you with wellness practices? (beginner/intermediate/advanced): ")
        
        # Current state
        mood = self._get_user_input("How are you feeling today? (e.g., 'tired', 'anxious', 'overwhelmed', 'good'): ")
        
        print(f"\n{Fore.YELLOW}Please rate the following on a scale of 1-10:{Style.RESET_ALL}")
        energy = int(self._get_user_input("Energy level (1=exhausted, 10=very energetic): ", 
                                        lambda x: self._validate_scale(x)))
        stress = int(self._get_user_input("Stress level (1=very relaxed, 10=extremely stressed): ", 
                                        lambda x: self._validate_scale(x)))
        sleep = int(self._get_user_input("Sleep quality last night (1=poor, 10=excellent): ", 
                                       lambda x: self._validate_scale(x)))
        
        # Hobbies and time
        hobbies_input = self._get_user_input("What are your hobbies/interests? (comma-separated, or 'none'): ")
        hobbies = [h.strip() for h in hobbies_input.split(",")] if hobbies_input.lower() != "none" else []
        
        time_available = int(self._get_user_input("How many minutes do you have for wellness activities today? (1-120): ", 
                                                lambda x: self._validate_scale(x, 1, 120)))
        
        # Preferences
        tone = self._get_user_input("What tone do you prefer? (supportive/encouraging/calm): ")
        if tone not in ["supportive", "encouraging", "calm"]:
            tone = "supportive"
        
        return UserProfile(
            persona=persona,
            expertise_level=expertise,
            mood=mood,
            energy=energy,
            stress=stress,
            sleep_quality=sleep,
            hobbies=hobbies,
            time_available=time_available,
            preferred_tone=tone
        )
    
    def _detect_risk_indicators(self, text: str) -> List[str]:
        """Detect risk indicators in user input"""
        detected = []
        text_lower = text.lower()
        
        for keyword in self.risk_keywords:
            if keyword in text_lower:
                detected.append(keyword)
        
        return detected
    
    def _create_dynamic_context(self, user_input: str = None) -> DynamicContext:
        """Create dynamic context for the current interaction"""
        context = DynamicContext()
        
        # Add conversation memory if available
        if self.current_user_id in self.dynamic_prompter.conversation_memory:
            context.memory_summary = self.dynamic_prompter.get_conversation_summary(self.current_user_id)
        
        # Add retrieved knowledge based on user profile
        if self.user_profile:
            knowledge_items = []
            if self.user_profile.stress >= 7:
                knowledge_items.append("Stress management techniques: 4-7-8 breathing, progressive muscle relaxation")
            if self.user_profile.energy <= 3:
                knowledge_items.append("Low energy strategies: gentle movement, hydration, micro-breaks")
            if self.user_profile.sleep_quality <= 4:
                knowledge_items.append("Sleep hygiene: consistent bedtime, screen-free hour, relaxation techniques")
            
            context.retrieved_knowledge = knowledge_items
        
        # Add recent activity based on user profile
        if self.user_profile:
            activities = []
            if self.user_profile.stress >= 8:
                activities.append("High stress detected - monitoring for escalation")
            if self.user_profile.energy <= 2:
                activities.append("Very low energy - gentle approach recommended")
            
            context.recent_activity = activities
        
        # Add conversation history if available
        if user_input:
            context.conversation_history = [{"role": "user", "content": user_input}]
        
        return context
    
    def _generate_response(self, mode: str, user_input: str = None) -> str:
        """Generate AI response using dynamic prompting"""
        try:
            # Create dynamic context
            context = self._create_dynamic_context(user_input)
            
            # Generate dynamic prompt
            dynamic_prompt = self.dynamic_prompter.create_dynamic_prompt(
                mode=mode,
                user_profile=self.user_profile,
                context=context,
                available_tools=self.available_tools
            )
            
            # Add user input if provided
            if user_input:
                full_prompt = f"{dynamic_prompt}\n\nUser input: {user_input}"
            else:
                full_prompt = dynamic_prompt
            
            # Generate response from AI
            response = self.model.generate_content(full_prompt)
            
            # Update conversation memory
            if user_input:
                self.dynamic_prompter.add_conversation_memory(
                    self.current_user_id,
                    {
                        "content": user_input,
                        "role": "user",
                        "mood": self.user_profile.mood if self.user_profile else None,
                        "risk_indicators": self._detect_risk_indicators(user_input)
                    }
                )
                
                self.dynamic_prompter.add_conversation_memory(
                    self.current_user_id,
                    {
                        "content": response.text,
                        "role": "assistant"
                    }
                )
            
            return response.text
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later. Error: {str(e)}"
    
    def motivation_mode(self):
        """Run motivation mode with dynamic prompting"""
        print(f"\n{Fore.GREEN}=== Motivation Mode ==={Style.RESET_ALL}")
        
        # Collect user profile if not already done
        if not self.user_profile:
            self.user_profile = self._collect_user_profile()
            self.dynamic_prompter.update_user_profile(self.current_user_id, self.user_profile)
        
        # Generate motivational response
        print("Generating personalized motivation for you...")
        response = self._generate_response("motivation")
        
        # Try to parse JSON response
        try:
            if response.strip().startswith('{'):
                data = json.loads(response)
                self._display_motivation_response(data)
            else:
                print(f"\n{Fore.YELLOW}AI Response:{Style.RESET_ALL}")
                print(response)
        except json.JSONDecodeError:
            print(f"\n{Fore.YELLOW}AI Response:{Style.RESET_ALL}")
            print(response)
        
        # Save to file
        self._save_last_output(response)
    
    def _display_motivation_response(self, data: Dict):
        """Display formatted motivation response"""
        print(f"\n{Fore.GREEN}=== Your Personalized Motivation ==={Style.RESET_ALL}")
        
        if 'quote' in data:
            print(f"\n{Fore.CYAN}💬 Quote:{Style.RESET_ALL}")
            print(f"\"{data['quote']}\"")
            if 'author' in data and data['author']:
                print(f"— {data['author']}")
        
        if 'suggested_action' in data:
            print(f"\n{Fore.YELLOW}🎯 Suggested Action:{Style.RESET_ALL}")
            print(data['suggested_action'])
        
        if 'hobby_suggestion' in data and data['hobby_suggestion']:
            print(f"\n{Fore.MAGENTA}🎨 Hobby Integration:{Style.RESET_ALL}")
            print(data['hobby_suggestion'])
        
        if 'challenge' in data and data['challenge']:
            print(f"\n{Fore.BLUE}🏆 Micro-Challenge:{Style.RESET_ALL}")
            print(data['challenge'])
        
        if 'affirmation' in data and data['affirmation']:
            print(f"\n{Fore.GREEN}✨ Affirmation:{Style.RESET_ALL}")
            print(data['affirmation'])
        
        if 'breathing_exercise' in data and data['breathing_exercise']:
            print(f"\n{Fore.CYAN}🫁 Breathing Exercise:{Style.RESET_ALL}")
            print(data['breathing_exercise'])
        
        if 'grounding_exercise' in data and data['grounding_exercise']:
            print(f"\n{Fore.YELLOW}🌱 Grounding Technique:{Style.RESET_ALL}")
            print(data['grounding_exercise'])
        
        if 'resources' in data and data['resources']:
            print(f"\n{Fore.RED}📚 Additional Resources:{Style.RESET_ALL}")
            print(data['resources'])
    
    def chat_mode(self):
        """Run live chat mode with dynamic prompting"""
        print(f"\n{Fore.GREEN}=== Live Chat Mode ==={Style.RESET_ALL}")
        print("Type your message and press Enter. Type 'exit' to quit.")
        print("I'm here to listen and support you.\n")
        
        # Collect user profile if not already done
        if not self.user_profile:
            self.user_profile = self._collect_user_profile()
            self.dynamic_prompter.update_user_profile(self.current_user_id, self.user_profile)
        
        while True:
            try:
                user_input = input(f"{Fore.CYAN}You:{Style.RESET_ALL} ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print(f"\n{Fore.GREEN}Thank you for chatting with me. Take care! 💙{Style.RESET_ALL}")
                    break
                
                if not user_input:
                    continue
                
                # Check for risk indicators
                risk_indicators = self._detect_risk_indicators(user_input)
                if risk_indicators:
                    print(f"\n{Fore.RED}⚠️  I notice some concerning language. I'm here to help.{Style.RESET_ALL}")
                
                # Generate response using dynamic prompting
                print(f"{Fore.YELLOW}SerenityCoach:{Style.RESET_ALL} ", end="")
                response = self._generate_response("chat", user_input)
                print(response)
                print()
                
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Chat interrupted. Take care! 💙{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"\n{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
                continue
    
    def _save_last_output(self, output: str):
        """Save the last output to a file"""
        try:
            with open('last_output.json', 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\n{Fore.GREEN}✓ Response saved to last_output.json{Style.RESET_ALL}")
        except Exception as e:
            print(f"\n{Fore.YELLOW}Note: Could not save response to file: {str(e)}{Style.RESET_ALL}")
    
    def run(self, args):
        """Main application entry point"""
        try:
            if args.chat:
                self.chat_mode()
            else:
                self.motivation_mode()
                
        except Exception as e:
            print(f"\n{Fore.RED}An unexpected error occurred: {str(e)}{Style.RESET_ALL}")
            print("Please check your API key and try again.")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SerenityCoach - Mental Health Companion with Dynamic Prompting"
    )
    parser.add_argument(
        '--chat',
        action='store_true',
        help='Start live chat mode'
    )
    parser.add_argument(
        '--mood',
        type=str,
        help='Specify mood for motivation mode (bypasses interactive prompt)'
    )
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.7,
        help='AI model temperature (0.0-1.0)'
    )
    
    args = parser.parse_args()
    
    try:
        coach = SerenityCoach()
        coach.run(args)
    except ValueError as e:
        print(f"{Fore.RED}Configuration Error: {str(e)}{Style.RESET_ALL}")
        print("Please set your GOOGLE_API_KEY environment variable.")
    except Exception as e:
        print(f"{Fore.RED}Unexpected Error: {str(e)}{Style.RESET_ALL}")


if __name__ == "__main__":
    main() 