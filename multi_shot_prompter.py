"""
Multi-shot Prompting Utility for SerenityCoach

This module provides structured multi-shot prompts with multiple examples
to improve AI model performance and consistency across different scenarios.
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class PromptExample:
    """Represents a single example for multi-shot prompting."""
    inputs: Dict[str, Any]
    output: str
    description: str = ""


class MultiShotPrompter:
    """Utility class for creating and managing multi-shot prompts."""
    
    def __init__(self):
        self.motivation_examples = self._create_motivation_examples()
        self.chat_examples = self._create_chat_examples()
        self.crisis_examples = self._create_crisis_examples()
    
    def _create_motivation_examples(self) -> List[PromptExample]:
        """Create examples for motivation mode prompts."""
        return [
            PromptExample(
                inputs={
                    "mood": "anxious",
                    "energy": 4,
                    "stress": 7,
                    "sleep": 5,
                    "hobbies": "art, running",
                    "time_available": 5
                },
                output=json.dumps({
                    "mood": "anxious",
                    "quote": "Feelings are waves; you can ride them without being swept away.",
                    "author": "Unknown",
                    "suggested_action": "Try a 5-4-3-2-1 grounding for 2 minutes, then sketch anything you notice.",
                    "grounding_exercise": "Name 5 things you see, 4 feel, 3 hear, 2 smell, 1 taste.",
                    "hobby_suggestion": "Spend 5 minutes doodling simple shapes to settle your mind."
                }, indent=2),
                description="Anxious mood with art hobby"
            ),
            PromptExample(
                inputs={
                    "mood": "tired",
                    "energy": 2,
                    "stress": 5,
                    "sleep": 3,
                    "hobbies": "gaming",
                    "time_available": 10
                },
                output=json.dumps({
                    "mood": "tired",
                    "quote": "Rest is productive when it helps you return with clarity.",
                    "author": "Unknown",
                    "suggested_action": "Drink water and take a 7-minute walk; then plan one tiny step for your next task.",
                    "challenge": "Set a 7-minute timer and walk indoors or outside.",
                    "joke": "Why did the computer nap? It had too many tabs open."
                }, indent=2),
                description="Tired mood with gaming hobby"
            ),
            PromptExample(
                inputs={
                    "mood": "overwhelmed",
                    "energy": 3,
                    "stress": 9,
                    "sleep": 4,
                    "hobbies": "reading",
                    "time_available": 8
                },
                output=json.dumps({
                    "mood": "overwhelmed",
                    "quote": "You don't have to do it all today; just the next right thing.",
                    "author": "Unknown",
                    "suggested_action": "Do box breathing for 2 minutes, then list one small step you can take now.",
                    "breathing_exercise": "Inhale 4, hold 4, exhale 4, hold 4 for 2-3 minutes.",
                    "resources": "If you feel unsafe or flooded, consider reaching out to someone you trust or a local helpline."
                }, indent=2),
                description="High stress overwhelmed mood"
            ),
            PromptExample(
                inputs={
                    "mood": "excited",
                    "energy": 8,
                    "stress": 2,
                    "sleep": 7,
                    "hobbies": "cooking, music",
                    "time_available": 15
                },
                output=json.dumps({
                    "mood": "excited",
                    "quote": "Enthusiasm is the electricity of life. How do you apply it?",
                    "author": "Gordon Parks",
                    "suggested_action": "Channel your energy into a quick cooking project or dance to your favorite song for 5 minutes.",
                    "hobby_suggestion": "Try a new recipe that takes 15 minutes or less.",
                    "challenge": "Learn to cook one new dish this week.",
                    "affirmation": "Your excitement is contagious and inspiring!"
                }, indent=2),
                description="Positive excited mood"
            ),
            PromptExample(
                inputs={
                    "mood": "lonely",
                    "energy": 5,
                    "stress": 6,
                    "sleep": 6,
                    "hobbies": "writing, photography",
                    "time_available": 20
                },
                output=json.dumps({
                    "mood": "lonely",
                    "quote": "Sometimes the most beautiful connections happen when we're alone with ourselves.",
                    "author": "Unknown",
                    "suggested_action": "Write a letter to your future self or take photos of things that bring you joy.",
                    "hobby_suggestion": "Start a photo journal of daily moments that make you smile.",
                    "challenge": "Reach out to one person you haven't talked to in a while.",
                    "affirmation": "You are worthy of connection and love."
                }, indent=2),
                description="Lonely mood with creative hobbies"
            )
        ]
    
    def _create_chat_examples(self) -> List[PromptExample]:
        """Create examples for live chat mode prompts."""
        return [
            PromptExample(
                inputs={"user_message": "I'm nervous about a presentation tomorrow."},
                output="It's normal to feel that way—your nerves mean you care. Try a 2-minute box breathing and rehearse your opening sentence out loud. Lay out your notes and water tonight so you feel prepared. What's one key point you want to land?",
                description="Presentation anxiety"
            ),
            PromptExample(
                inputs={"user_message": "I keep procrastinating and feel guilty."},
                output="That's a tough cycle—thanks for being honest about it. Try a 5-minute start: set a timer and do only the first tiny step. After that, stretch and grab water. If it helps, what's the smallest step you could do right now?",
                description="Procrastination guilt"
            ),
            PromptExample(
                inputs={"user_message": "I feel like giving up."},
                output="I'm really sorry it's this heavy. You're not alone, and you deserve support. If you're feeling unsafe, consider reaching out to someone you trust or a local helpline. For now, could we try 2 minutes of slow breathing together—inhale 4, exhale 6?",
                description="Crisis response"
            ),
            PromptExample(
                inputs={"user_message": "I had a great day today!"},
                output="That's wonderful to hear! Celebrating good moments is so important. What made it special? Maybe you could write down one highlight or share it with someone you care about.",
                description="Positive mood support"
            ),
            PromptExample(
                inputs={"user_message": "I can't stop worrying about everything."},
                output="Worry can feel like a broken record that won't stop playing. Try this: set a 5-minute timer and let yourself worry freely. When it goes off, take 3 deep breaths and do something completely different for 10 minutes. What activity could distract you?",
                description="Chronic worry"
            )
        ]
    
    def _create_crisis_examples(self) -> List[PromptExample]:
        """Create examples for crisis intervention prompts."""
        return [
            PromptExample(
                inputs={"user_message": "I don't want to be here anymore."},
                output="I'm really concerned about what you're going through. You matter, and you deserve help. Please reach out to someone you trust right now, or call a crisis helpline. You don't have to face this alone. Can you tell me one person you could call?",
                description="Suicidal ideation"
            ),
            PromptExample(
                inputs={"user_message": "I want to hurt myself."},
                output="I'm so sorry you're in this much pain. You deserve safety and support. Please reach out to someone you trust immediately, or call a crisis helpline. You're not alone in this. What's one thing that could help you feel safer right now?",
                description="Self-harm thoughts"
            ),
            PromptExample(
                inputs={"user_message": "Everything feels hopeless."},
                output="I hear how overwhelming this feels. When things seem hopeless, it's a sign you need extra support. Please consider reaching out to someone you trust or a mental health professional. You don't have to figure this out alone. What's one small thing that usually helps you feel a bit better?",
                description="Hopelessness"
            )
        ]
    
    def get_motivation_prompt(self, mood: str, energy: int = 5, stress: int = 5, 
                             sleep: int = 5, hobbies: str = "", time_available: int = 10) -> str:
        """Generate a multi-shot prompt for motivation mode."""
        prompt = """You are SerenityCoach, an empathetic, non-clinical mental health companion.
Task: Generate exactly one JSON object based on the user's mood and optional context. Return only JSON—no extra text.

Constraints:
- No diagnosis or medical advice.
- If stress >= 8 or risk keywords appear (e.g., self-harm, suicide, "end it"), include a brief, compassionate safety note under "resources" encouraging reaching out to trusted people and local helplines (region-agnostic).
- Keep suggestions small, practical, and doable in minutes. Prefer hobby-aligned ideas if hobbies are provided.

Format: Required keys {mood, quote, author, suggested_action}. Optional {joke, hobby_suggestion, challenge, affirmation, breathing_exercise, grounding_exercise, resources}.

Examples:
"""
        
        # Add examples
        for i, example in enumerate(self.motivation_examples, 1):
            prompt += f"\n[Example {i} - {example.description}]\n"
            prompt += "Inputs:\n"
            for key, value in example.inputs.items():
                prompt += f"- {key}=\"{value}\"\n"
            prompt += f"Output (JSON):\n{example.output}\n"
        
        prompt += f"""

Now generate the JSON for these inputs:
- mood="{mood}"
- energy={energy}
- stress={stress}
- sleep={sleep}
- hobbies="{hobbies}"
- time_available={time_available}

Return only the JSON."""
        
        return prompt
    
    def get_chat_prompt(self, user_message: str, stress: int = 5, energy: int = 5, 
                        sleep: int = 5, time_available: int = 10, hobbies: str = "") -> str:
        """Generate a multi-shot prompt for live chat mode."""
        prompt = """You are SerenityCoach, an empathetic, non-clinical mental health companion.
Task: Reply directly to the user in 2-4 short sentences. Ask at most one clarifying question only if it clearly improves usefulness.

Constraints:
- Offer small, practical coping strategies when appropriate (breathing, grounding, journaling, water, brief walk).
- No diagnosis or medical advice.
- If risk keywords appear, validate feelings and add a gentle, region-agnostic safety nudge to contact trusted people or local helplines.
Tone: warm, validating, concise, and on-topic.

Examples:
"""
        
        # Add regular chat examples
        for i, example in enumerate(self.chat_examples, 1):
            prompt += f"\n[Example {i} - {example.description}]\n"
            prompt += f"User: \"{example.inputs['user_message']}\"\n"
            prompt += f"Assistant: \"{example.output}\"\n"
        
        # Add crisis examples
        prompt += "\n[Crisis Response Examples]\n"
        for i, example in enumerate(self.crisis_examples, 1):
            prompt += f"\n[Example {i} - {example.description}]\n"
            prompt += f"User: \"{example.inputs['user_message']}\"\n"
            prompt += f"Assistant: \"{example.output}\"\n"
        
        prompt += f"""

Now respond to the new message using the same tone and constraints:
- user_message="{user_message}"
Optional context: stress={stress}, energy={energy}, sleep={sleep}, time_available={time_available}, hobbies="{hobbies}"

Remember: If you detect crisis language, prioritize safety and encourage reaching out to trusted support."""
        
        return prompt
    
    def get_custom_prompt(self, examples: List[PromptExample], task_description: str, 
                         constraints: str, user_input: str) -> str:
        """Generate a custom multi-shot prompt with user-defined examples."""
        prompt = f"""Task: {task_description}

Constraints:
{constraints}

Examples:
"""
        
        for i, example in enumerate(examples, 1):
            prompt += f"\n[Example {i} - {example.description}]\n"
            prompt += "Inputs:\n"
            for key, value in example.inputs.items():
                prompt += f"- {key}=\"{value}\"\n"
            prompt += f"Output:\n{example.output}\n"
        
        prompt += f"""

Now respond to this input using the same format and style:
{user_input}"""
        
        return prompt
    
    def add_example(self, examples_list: str, example: PromptExample):
        """Add a new example to the specified examples list."""
        if examples_list == "motivation":
            self.motivation_examples.append(example)
        elif examples_list == "chat":
            self.chat_examples.append(example)
        elif examples_list == "crisis":
            self.crisis_examples.append(example)
        else:
            raise ValueError("examples_list must be 'motivation', 'chat', or 'crisis'")
    
    def get_example_count(self) -> Dict[str, int]:
        """Get the count of examples in each category."""
        return {
            "motivation": len(self.motivation_examples),
            "chat": len(self.chat_examples),
            "crisis": len(self.crisis_examples)
        }


# Example usage and testing
if __name__ == "__main__":
    prompter = MultiShotPrompter()
    
    # Test motivation prompt
    motivation_prompt = prompter.get_motivation_prompt(
        mood="stressed", 
        energy=3, 
        stress=8, 
        sleep=4, 
        hobbies="reading, yoga", 
        time_available=15
    )
    print("=== MOTIVATION PROMPT ===")
    print(motivation_prompt)
    print("\n" + "="*50 + "\n")
    
    # Test chat prompt
    chat_prompt = prompter.get_chat_prompt(
        user_message="I'm feeling really overwhelmed with work",
        stress=8,
        energy=2,
        sleep=3,
        time_available=10,
        hobbies="music, walking"
    )
    print("=== CHAT PROMPT ===")
    print(chat_prompt)
    
    # Show example counts
    print(f"\nExample counts: {prompter.get_example_count()}") 