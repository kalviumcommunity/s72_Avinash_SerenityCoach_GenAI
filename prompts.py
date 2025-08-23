"""
One-shot prompting utilities for SerenityCoach mental health companion.
Implements structured prompts with examples to guide AI responses.
"""

from typing import Dict, Any, Optional
import json


class OneShotPrompter:
    """Utility class for creating one-shot prompts with examples."""
    
    def __init__(self):
        self.motivation_example = {
            "mood": "overwhelmed",
            "quote": "You don't have to see the whole staircase; just take the first step.",
            "author": "Martin Luther King Jr.",
            "suggested_action": "Do 2 minutes of box breathing, then write one tiny next step you can do now.",
            "breathing_exercise": "Inhale 4, hold 4, exhale 4, hold 4 for 2 minutes.",
            "resources": "If you feel unsafe or overwhelmed, consider reaching out to someone you trust or a local helpline."
        }
        
        self.chat_example = {
            "user_message": "I've been anxious all day and can't concentrate.",
            "assistant_response": "Thanks for sharing that—it's tough when your mind won't settle. Try a 3-minute grounding: name 5 things you see, 4 you feel, 3 you hear. A short walk or some water can also help reset. If you'd like, what's the smallest task you could start for 5 minutes?"
        }
    
    def create_motivation_prompt(self, mood: str, energy: int = 5, stress: int = 5, 
                                sleep: int = 5, hobbies: str = "", time_available: int = 15) -> str:
        """
        Create a one-shot prompt for motivation mode.
        
        Args:
            mood: User's current mood
            energy: Energy level (1-10)
            stress: Stress level (1-10)
            sleep: Sleep quality (1-10)
            hobbies: Comma-separated hobbies
            time_available: Time available in minutes
            
        Returns:
            Formatted one-shot prompt string
        """
        prompt = f"""You are SerenityCoach, an empathetic, non-clinical mental health companion.
Task: Generate exactly one JSON object based on the user's mood and optional context. Return only JSON—no extra text.

Constraints:
- No diagnosis or medical advice.
- If stress >= 8 or risk keywords appear (e.g., self-harm, suicide, "end it"), include a brief, compassionate safety note under "resources" encouraging reaching out to trusted people and local helplines (region-agnostic).
- Keep suggestions small, practical, and doable in minutes. Prefer hobby-aligned ideas if hobbies are provided.

Format: Required keys {{mood, quote, author, suggested_action}}. Optional {{joke, hobby_suggestion, challenge, affirmation, breathing_exercise, grounding_exercise, resources}}.

Example inputs:
- mood="overwhelmed"
- energy=3
- stress=8
- sleep=4
- hobbies="reading, music"
- time_available=10

Example output (JSON):
{json.dumps(self.motivation_example, indent=2)}

Now generate the JSON for these inputs:
- mood="{mood}"
- energy={energy}
- stress={stress}
- sleep={sleep}
- hobbies="{hobbies}"
- time_available={time_available}

Return only the JSON."""
        
        return prompt
    
    def create_chat_prompt(self, user_message: str, energy: int = 5, stress: int = 5,
                          sleep: int = 5, hobbies: str = "", time_available: int = 15) -> str:
        """
        Create a one-shot prompt for live chat mode.
        
        Args:
            user_message: User's message
            energy: Energy level (1-10)
            stress: Stress level (1-10)
            sleep: Sleep quality (1-10)
            hobbies: Comma-separated hobbies
            time_available: Time available in minutes
            
        Returns:
            Formatted one-shot prompt string
        """
        prompt = f"""You are SerenityCoach, an empathetic, non-clinical mental health companion.
Task: Reply directly to the user in 2–4 short sentences. Ask at most one clarifying question only if it clearly improves usefulness.

Constraints:
- Offer small, practical coping strategies when appropriate (breathing, grounding, journaling, water, brief walk).
- No diagnosis or medical advice.
- If risk keywords appear, validate feelings and add a gentle, region-agnostic safety nudge to contact trusted people or local helplines.

Tone: warm, validating, concise, and on-topic.

Example:
User: "{self.chat_example['user_message']}"
Assistant: "{self.chat_example['assistant_response']}"

Now respond to the new message using the same tone and constraints:
- user_message="{user_message}"
Optional context: stress={stress}, energy={energy}, sleep={sleep}, time_available={time_available}, hobbies="{hobbies}"

Respond in 2-4 sentences:"""
        
        return prompt
    
    def create_risk_assessment_prompt(self, message: str) -> str:
        """
        Create a one-shot prompt for risk assessment.
        
        Args:
            message: User message to assess
            
        Returns:
            Formatted risk assessment prompt
        """
        risk_example = {
            "risk_level": "medium",
            "keywords_detected": ["overwhelmed", "can't take it"],
            "response_type": "safety_note",
            "safety_message": "It sounds like you're really struggling right now. Please know that you don't have to face this alone. Consider reaching out to someone you trust or a local helpline for support."
        }
        
        prompt = f"""You are a mental health safety assessor. Analyze the user message for risk indicators and return a JSON response.

Task: Assess the message for risk level and provide appropriate response guidance.

Example input: "I'm so overwhelmed, I can't take it anymore"
Example output:
{json.dumps(risk_example, indent=2)}

Now assess this message: "{message}"

Return only the JSON with keys: risk_level (low/medium/high), keywords_detected (list), response_type (normal/safety_note), safety_message (if needed)."""
        
        return prompt


def format_mood_context(mood: str, **kwargs) -> Dict[str, Any]:
    """
    Format mood context for prompt generation.
    
    Args:
        mood: User's mood
        **kwargs: Additional context parameters
        
    Returns:
        Dictionary with formatted context
    """
    context = {
        "mood": mood,
        "energy": kwargs.get("energy", 5),
        "stress": kwargs.get("stress", 5),
        "sleep": kwargs.get("sleep", 5),
        "hobbies": kwargs.get("hobbies", ""),
        "time_available": kwargs.get("time_available", 15)
    }
    return context


def validate_prompt_output(output: str, expected_type: str = "json") -> bool:
    """
    Validate prompt output format.
    
    Args:
        output: AI model output
        expected_type: Expected output type ("json" or "text")
        
    Returns:
        True if valid, False otherwise
    """
    if expected_type == "json":
        try:
            json.loads(output.strip())
            return True
        except (json.JSONDecodeError, ValueError):
            return False
    return True


# Convenience functions for quick prompt generation
def get_motivation_prompt(mood: str, **context) -> str:
    """Quick function to get motivation prompt."""
    prompter = OneShotPrompter()
    return prompter.create_motivation_prompt(mood, **context)


def get_chat_prompt(user_message: str, **context) -> str:
    """Quick function to get chat prompt."""
    prompter = OneShotPrompter()
    return prompter.create_chat_prompt(user_message, **context)


def get_risk_assessment_prompt(message: str) -> str:
    """Quick function to get risk assessment prompt."""
    prompter = OneShotPrompter()
    return prompter.create_risk_assessment_prompt(message) 