"""
Dynamic Prompting Module for SerenityCoach

This module implements dynamic prompting that adapts the AI assistant's behavior
based on user context, mood, available tools, and conversation history.
"""

import json
import yaml
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import os


@dataclass
class UserProfile:
    """User profile information for dynamic prompting"""
    persona: str
    expertise_level: str
    mood: str
    energy: int
    stress: int
    sleep_quality: int
    hobbies: List[str]
    time_available: int
    preferred_tone: str = "supportive"
    preferred_format: str = "concise"


@dataclass
class DynamicContext:
    """Dynamic context for adaptive prompting"""
    memory_summary: Optional[str] = None
    retrieved_knowledge: List[str] = None
    recent_activity: List[str] = None
    conversation_history: List[Dict] = None
    risk_level: str = "low"
    
    def __post_init__(self):
        if self.retrieved_knowledge is None:
            self.retrieved_knowledge = []
        if self.recent_activity is None:
            self.recent_activity = []
        if self.conversation_history is None:
            self.conversation_history = []


@dataclass
class Tool:
    """Available tool for the AI assistant"""
    name: str
    description: str
    input_schema: Dict
    output_schema: Dict
    is_available: bool = True


class DynamicPrompter:
    """
    Dynamic prompting system that adapts prompts based on context
    
    Features:
    - Context-aware prompt generation
    - User profile adaptation
    - Tool availability integration
    - Risk assessment and safety measures
    - Memory and conversation history integration
    """
    
    def __init__(self):
        self.base_templates = self._load_base_templates()
        self.user_profiles = {}
        self.conversation_memory = {}
        self.risk_keywords = [
            "suicide", "kill myself", "end it all", "want to die",
            "self-harm", "cut myself", "overdose", "no reason to live"
        ]
        
    def _load_base_templates(self) -> Dict:
        """Load base prompt templates"""
        return {
            "motivation": {
                "role": "empathetic mental health companion",
                "mission": "provide personalized motivation and actionable wellness suggestions",
                "success_criteria": [
                    "generate relevant motivational quote",
                    "suggest practical, doable actions",
                    "maintain supportive, non-clinical tone"
                ],
                "constraints": [
                    "no medical diagnosis or advice",
                    "keep suggestions practical and time-appropriate",
                    "prioritize safety for high-risk situations"
                ]
            },
            "chat": {
                "role": "supportive conversation partner",
                "mission": "engage in empathetic, helpful dialogue",
                "success_criteria": [
                    "respond directly to user concerns",
                    "offer practical coping strategies",
                    "maintain warm, validating tone"
                ],
                "constraints": [
                    "keep responses concise (2-4 sentences)",
                    "avoid unnecessary questions",
                    "detect and respond to risk signals"
                ]
            },
            "crisis": {
                "role": "crisis intervention specialist",
                "mission": "provide immediate safety guidance and support",
                "success_criteria": [
                    "assess immediate safety needs",
                    "provide clear crisis resources",
                    "encourage professional help-seeking"
                ],
                "constraints": [
                    "prioritize safety over all other concerns",
                    "provide specific, actionable crisis guidance",
                    "maintain calm, directive tone"
                ]
            }
        }
    
    def create_dynamic_prompt(
        self,
        mode: str,
        user_profile: UserProfile,
        context: DynamicContext,
        available_tools: List[Tool],
        custom_instructions: Optional[str] = None
    ) -> str:
        """
        Create a dynamic prompt based on current context and user profile
        
        Args:
            mode: Prompt mode (motivation, chat, crisis)
            user_profile: User profile information
            context: Dynamic context information
            available_tools: List of available tools
            custom_instructions: Additional custom instructions
            
        Returns:
            Formatted dynamic prompt string
        """
        
        # Get base template
        base = self.base_templates.get(mode, self.base_templates["chat"])
        
        # Assess risk level
        risk_level = self._assess_risk_level(user_profile, context)
        if risk_level == "high":
            mode = "crisis"
            base = self.base_templates["crisis"]
        
        # Build dynamic prompt
        prompt_parts = []
        
        # System role and mission
        prompt_parts.append(f"You are SerenityCoach, a {base['role']}.")
        prompt_parts.append(f"Your mission: {base['mission']}")
        
        # Success criteria
        prompt_parts.append("\nSuccess criteria:")
        for criterion in base['success_criteria']:
            prompt_parts.append(f"- {criterion}")
        
        # User profile adaptation
        prompt_parts.append(f"\nUser Profile:")
        prompt_parts.append(f"- Persona: {user_profile.persona}")
        prompt_parts.append(f"- Current mood: {user_profile.mood}")
        prompt_parts.append(f"- Energy level: {user_profile.energy}/10")
        prompt_parts.append(f"- Stress level: {user_profile.stress}/10")
        prompt_parts.append(f"- Sleep quality: {user_profile.sleep_quality}/10")
        prompt_parts.append(f"- Hobbies: {', '.join(user_profile.hobbies) if user_profile.hobbies else 'None specified'}")
        prompt_parts.append(f"- Time available: {user_profile.time_available} minutes")
        prompt_parts.append(f"- Preferred tone: {user_profile.preferred_tone}")
        
        # Dynamic context
        if context.memory_summary:
            prompt_parts.append(f"\nPrevious context: {context.memory_summary}")
        
        if context.retrieved_knowledge:
            prompt_parts.append("\nRelevant knowledge:")
            for i, knowledge in enumerate(context.retrieved_knowledge, 1):
                prompt_parts.append(f"[K{i}] {knowledge}")
        
        if context.recent_activity:
            prompt_parts.append("\nRecent activity:")
            for activity in context.recent_activity[-3:]:  # Last 3 activities
                prompt_parts.append(f"- {activity}")
        
        # Risk assessment and safety measures
        if risk_level != "low":
            prompt_parts.append(f"\n⚠️ RISK LEVEL: {risk_level.upper()}")
            if risk_level == "high":
                prompt_parts.append("CRITICAL: User shows signs of crisis. Prioritize safety guidance.")
            elif risk_level == "medium":
                prompt_parts.append("CAUTION: Monitor for escalation. Offer additional support resources.")
        
        # Available tools
        if available_tools:
            prompt_parts.append("\nAvailable tools:")
            for tool in available_tools:
                if tool.is_available:
                    prompt_parts.append(f"- {tool.name}: {tool.description}")
        
        # Constraints
        prompt_parts.append("\nConstraints:")
        for constraint in base['constraints']:
            prompt_parts.append(f"- {constraint}")
        
        # Mode-specific instructions
        if mode == "motivation":
            prompt_parts.append("\nOutput Format: Return ONLY a JSON object with the following structure:")
            prompt_parts.append("""
{
  "mood": "user's current mood",
  "quote": "motivational quote",
  "author": "quote author",
  "suggested_action": "practical action suggestion",
  "hobby_suggestion": "hobby-aligned wellness tip",
  "challenge": "micro-challenge for today",
  "affirmation": "positive affirmation",
  "breathing_exercise": "simple breathing technique",
  "grounding_exercise": "grounding technique",
  "resources": "additional support resources if needed"
}""")
        
        elif mode == "chat":
            prompt_parts.append("\nChat Guidelines:")
            prompt_parts.append("- Keep responses to 2-4 sentences")
            prompt_parts.append("- Answer directly without unnecessary questions")
            prompt_parts.append("- Offer practical coping strategies when relevant")
            prompt_parts.append("- Maintain warm, validating tone")
        
        elif mode == "crisis":
            prompt_parts.append("\nCrisis Response Protocol:")
            prompt_parts.append("- Acknowledge the user's feelings with empathy")
            prompt_parts.append("- Provide immediate safety guidance")
            prompt_parts.append("- Offer crisis resources and helplines")
            prompt_parts.append("- Encourage reaching out to trusted support")
        
        # Custom instructions
        if custom_instructions:
            prompt_parts.append(f"\nAdditional Instructions: {custom_instructions}")
        
        # Final guidance
        prompt_parts.append("\nRemember: You are a supportive companion, not a medical professional.")
        prompt_parts.append("Always prioritize user safety and well-being.")
        
        return "\n".join(prompt_parts)
    
    def _assess_risk_level(self, user_profile: UserProfile, context: DynamicContext) -> str:
        """Assess risk level based on user profile and context"""
        
        # Check for risk keywords in recent conversation
        if context.conversation_history:
            recent_text = " ".join([msg.get("content", "") for msg in context.conversation_history[-5:]])
            if any(keyword in recent_text.lower() for keyword in self.risk_keywords):
                return "high"
        
        # Check stress and sleep indicators
        if user_profile.stress >= 8 or user_profile.sleep_quality <= 3:
            return "medium"
        
        # Check for concerning patterns
        if user_profile.energy <= 2 and user_profile.stress >= 7:
            return "medium"
        
        return "low"
    
    def update_user_profile(self, user_id: str, profile: UserProfile):
        """Update user profile for future prompts"""
        self.user_profiles[user_id] = profile
    
    def add_conversation_memory(self, user_id: str, message: Dict):
        """Add conversation to memory for context"""
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        self.conversation_memory[user_id].append({
            "timestamp": datetime.now().isoformat(),
            "content": message.get("content", ""),
            "role": message.get("role", "user"),
            "mood": message.get("mood"),
            "risk_indicators": message.get("risk_indicators", [])
        })
        
        # Keep only last 20 messages
        if len(self.conversation_memory[user_id]) > 20:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-20:]
    
    def get_conversation_summary(self, user_id: str) -> str:
        """Get a summary of recent conversation for context"""
        if user_id not in self.conversation_memory:
            return "No previous conversation history."
        
        messages = self.conversation_memory[user_id][-5:]  # Last 5 messages
        summary_parts = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            summary_parts.append(f"{role}: {content}")
        
        return " | ".join(summary_parts)
    
    def create_adaptive_response_plan(
        self,
        user_profile: UserProfile,
        context: DynamicContext,
        available_tools: List[Tool]
    ) -> Dict[str, Any]:
        """Create an adaptive response plan based on current context"""
        
        plan = {
            "primary_approach": "supportive",
            "suggested_tools": [],
            "response_style": "standard",
            "safety_measures": [],
            "follow_up_actions": []
        }
        
        # Adapt based on stress level
        if user_profile.stress >= 7:
            plan["primary_approach"] = "calming"
            plan["suggested_tools"].append("breathing_exercises")
            plan["safety_measures"].append("stress_monitoring")
        
        # Adapt based on energy level
        if user_profile.energy <= 3:
            plan["primary_approach"] = "gentle"
            plan["suggested_tools"].append("micro_actions")
            plan["response_style"] = "encouraging"
        
        # Adapt based on time available
        if user_profile.time_available < 15:
            plan["response_style"] = "concise"
            plan["suggested_tools"].append("quick_exercises")
        
        # Adapt based on hobbies
        if user_profile.hobbies:
            plan["suggested_tools"].append("hobby_integration")
        
        # Add safety measures for medium/high risk
        risk_level = self._assess_risk_level(user_profile, context)
        if risk_level != "low":
            plan["safety_measures"].append("crisis_resources")
            plan["follow_up_actions"].append("safety_check")
        
        return plan
    
    def export_prompt_template(self, mode: str, output_format: str = "yaml") -> str:
        """Export a prompt template for external use"""
        template = {
            "mode": mode,
            "base_template": self.base_templates.get(mode, {}),
            "dynamic_elements": {
                "user_profile_fields": [
                    "persona", "mood", "energy", "stress", "sleep_quality",
                    "hobbies", "time_available", "preferred_tone"
                ],
                "context_fields": [
                    "memory_summary", "retrieved_knowledge", "recent_activity",
                    "conversation_history", "risk_level"
                ],
                "adaptation_rules": {
                    "high_stress": "switch_to_calming_approach",
                    "low_energy": "use_gentle_encouragement",
                    "limited_time": "prioritize_concise_responses",
                    "hobby_available": "integrate_hobby_based_suggestions"
                }
            }
        }
        
        if output_format == "yaml":
            return yaml.dump(template, default_flow_style=False, sort_keys=False)
        else:
            return json.dumps(template, indent=2)


# Example usage and testing
if __name__ == "__main__":
    # Create dynamic prompter instance
    prompter = DynamicPrompter()
    
    # Example user profile
    user = UserProfile(
        persona="busy professional",
        expertise_level="beginner",
        mood="overwhelmed",
        energy=3,
        stress=8,
        sleep_quality=4,
        hobbies=["reading", "walking"],
        time_available=20
    )
    
    # Example context
    context = DynamicContext(
        memory_summary="User has been experiencing high stress for the past week",
        retrieved_knowledge=["4-7-8 breathing technique", "Progressive muscle relaxation"],
        recent_activity=["Completed breathing exercise yesterday", "Missed morning walk today"]
    )
    
    # Example tools
    tools = [
        Tool("breathing_exercises", "Guided breathing techniques", {}, {}),
        Tool("mood_tracker", "Track daily mood and patterns", {}, {}),
        Tool("crisis_resources", "Emergency mental health resources", {}, {})
    ]
    
    # Generate dynamic prompt
    prompt = prompter.create_dynamic_prompt("chat", user, context, tools)
    print("=== DYNAMIC PROMPT EXAMPLE ===")
    print(prompt)
    
    # Create adaptive response plan
    plan = prompter.create_adaptive_response_plan(user, context, tools)
    print("\n=== ADAPTIVE RESPONSE PLAN ===")
    print(json.dumps(plan, indent=2))
    
    # Export template
    template = prompter.export_prompt_template("chat", "yaml")
    print("\n=== EXPORTED TEMPLATE ===")
    print(template) 