"""
Configuration file for SerenityCoach Dynamic Prompting System

This file contains configurable parameters for the dynamic prompting system,
allowing easy customization of behavior, thresholds, and features.
"""

import os
from typing import Dict, List, Any

# API Configuration
API_CONFIG = {
    "google_api_key_env": "GOOGLE_API_KEY",
    "model_name": "gemini-pro",
    "temperature": 0.7,
    "max_tokens": 1000,
    "timeout": 30
}

# Dynamic Prompting Configuration
PROMPTING_CONFIG = {
    # Risk Assessment Thresholds
    "risk_thresholds": {
        "stress_high": 8,           # Stress level that triggers medium risk
        "stress_critical": 9,       # Stress level that triggers high risk
        "energy_low": 3,            # Energy level that triggers medium risk
        "energy_critical": 2,       # Energy level that triggers critical risk
        "sleep_poor": 4,            # Sleep quality that triggers medium risk
        "sleep_critical": 3         # Sleep quality that triggers high risk
    },
    
    # Response Style Adaptation
    "response_adaptation": {
        "time_concise": 15,         # Minutes available for concise responses
        "time_detailed": 45,        # Minutes available for detailed responses
        "stress_calming": 7,        # Stress level for calming approach
        "energy_gentle": 3          # Energy level for gentle approach
    },
    
    # Memory and Context Settings
    "memory_settings": {
        "max_conversation_history": 20,    # Maximum messages to keep in memory
        "summary_length": 5,               # Number of recent messages for summary
        "context_window": 10               # Messages to consider for context
    },
    
    # Tool Integration Settings
    "tool_settings": {
        "max_tools_per_prompt": 5,         # Maximum tools to mention in prompt
        "tool_priority_threshold": 0.7,    # Threshold for tool relevance
        "auto_tool_suggestion": True       # Automatically suggest relevant tools
    }
}

# Safety and Risk Detection
SAFETY_CONFIG = {
    # Risk Keywords (case-insensitive)
    "risk_keywords": [
        "suicide", "kill myself", "end it all", "want to die",
        "self-harm", "cut myself", "overdose", "no reason to live",
        "better off dead", "can't take it anymore", "give up",
        "hopeless", "worthless", "burden", "everyone would be better off"
    ],
    
    # Crisis Response Settings
    "crisis_response": {
        "immediate_safety_check": True,
        "crisis_resources_required": True,
        "professional_help_encouragement": True,
        "follow_up_required": True
    },
    
    # Escalation Triggers
    "escalation_triggers": {
        "multiple_risk_mentions": 2,       # Number of risk mentions before escalation
        "consecutive_high_stress": 3,      # Days of high stress before escalation
        "sleep_deprivation": 3             # Days of poor sleep before escalation
    }
}

# User Profile Defaults
USER_PROFILE_DEFAULTS = {
    "expertise_levels": ["beginner", "intermediate", "advanced"],
    "preferred_tones": ["supportive", "encouraging", "calm", "motivational"],
    "mood_categories": [
        "happy", "content", "calm", "focused", "motivated",
        "tired", "anxious", "stressed", "overwhelmed", "sad",
        "angry", "frustrated", "lonely", "confused", "excited"
    ],
    "hobby_categories": [
        "physical_activity", "creative", "intellectual", "social",
        "outdoor", "indoor", "solo", "group", "relaxing", "energizing"
    ]
}

# Tool Definitions
TOOL_DEFINITIONS = {
    "breathing_exercises": {
        "name": "Breathing Exercises",
        "description": "Guided breathing techniques for stress relief and relaxation",
        "categories": ["stress_management", "relaxation", "mindfulness"],
        "time_requirements": [1, 5, 10, 15],
        "energy_requirements": [1, 3, 5, 7],
        "stress_reduction": 0.6,
        "energy_boost": 0.3
    },
    
    "mood_tracker": {
        "name": "Mood Tracker",
        "description": "Track and analyze mood patterns over time",
        "categories": ["self_awareness", "tracking", "analytics"],
        "time_requirements": [2, 5, 10],
        "energy_requirements": [2, 4, 6],
        "stress_reduction": 0.2,
        "energy_boost": 0.1
    },
    
    "micro_actions": {
        "name": "Micro Actions",
        "description": "Quick, actionable wellness activities",
        "categories": ["wellness", "action", "motivation"],
        "time_requirements": [1, 3, 5, 10],
        "energy_requirements": [3, 5, 7, 9],
        "stress_reduction": 0.4,
        "energy_boost": 0.5
    },
    
    "crisis_resources": {
        "name": "Crisis Resources",
        "description": "Emergency mental health resources and helplines",
        "categories": ["crisis", "safety", "emergency"],
        "time_requirements": [1, 2, 5],
        "energy_requirements": [1, 2, 3],
        "stress_reduction": 0.8,
        "energy_boost": 0.1
    },
    
    "hobby_integration": {
        "name": "Hobby Integration",
        "description": "Integrate wellness activities with user hobbies",
        "categories": ["personalization", "motivation", "integration"],
        "time_requirements": [5, 15, 30, 60],
        "energy_requirements": [4, 6, 8, 9],
        "stress_reduction": 0.5,
        "energy_boost": 0.7
    }
}

# Prompt Templates Configuration
PROMPT_TEMPLATES = {
    "motivation": {
        "max_length": 2000,
        "required_fields": ["mood", "quote", "author", "suggested_action"],
        "optional_fields": [
            "hobby_suggestion", "challenge", "affirmation",
            "breathing_exercise", "grounding_exercise", "resources"
        ],
        "style_guide": "warm, encouraging, practical, non-clinical"
    },
    
    "chat": {
        "max_length": 500,
        "response_guidelines": [
            "2-4 sentences maximum",
            "direct answers preferred",
            "practical tips when relevant",
            "warm and validating tone"
        ],
        "style_guide": "concise, supportive, actionable"
    },
    
    "crisis": {
        "max_length": 800,
        "required_elements": [
            "immediate_safety_assessment",
            "crisis_resources",
            "professional_help_encouragement",
            "follow_up_plan"
        ],
        "style_guide": "calm, directive, compassionate, urgent"
    }
}

# Environment-specific Configuration
def get_config_for_environment(env: str = None) -> Dict[str, Any]:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('SERENITY_ENV', 'development')
    
    configs = {
        'development': {
            'debug': True,
            'log_level': 'DEBUG',
            'save_conversations': True,
            'enable_experimental_features': True
        },
        'production': {
            'debug': False,
            'log_level': 'INFO',
            'save_conversations': False,
            'enable_experimental_features': False
        },
        'testing': {
            'debug': True,
            'log_level': 'DEBUG',
            'save_conversations': False,
            'enable_experimental_features': True
        }
    }
    
    return configs.get(env, configs['development'])

# Dynamic Configuration Updates
def update_config(section: str, key: str, value: Any) -> bool:
    """Update configuration dynamically"""
    try:
        if section == "prompting":
            PROMPTING_CONFIG[key] = value
        elif section == "safety":
            SAFETY_CONFIG[key] = value
        elif section == "tools":
            TOOL_DEFINITIONS[key] = value
        else:
            return False
        return True
    except Exception:
        return False

def get_tool_recommendations(user_profile: Dict, context: Dict) -> List[str]:
    """Get tool recommendations based on user profile and context"""
    recommendations = []
    
    # Stress-based recommendations
    if user_profile.get('stress', 0) >= 7:
        recommendations.append('breathing_exercises')
        recommendations.append('crisis_resources')
    
    # Energy-based recommendations
    if user_profile.get('energy', 5) <= 3:
        recommendations.append('micro_actions')
        recommendations.append('hobby_integration')
    
    # Time-based recommendations
    time_available = user_profile.get('time_available', 30)
    if time_available < 10:
        recommendations.append('breathing_exercises')
    elif time_available >= 30:
        recommendations.append('hobby_integration')
    
    # Context-based recommendations
    if context.get('risk_level') == 'high':
        recommendations.append('crisis_resources')
    
    return list(set(recommendations))  # Remove duplicates

# Export all configurations
__all__ = [
    'API_CONFIG',
    'PROMPTING_CONFIG', 
    'SAFETY_CONFIG',
    'USER_PROFILE_DEFAULTS',
    'TOOL_DEFINITIONS',
    'PROMPT_TEMPLATES',
    'get_config_for_environment',
    'update_config',
    'get_tool_recommendations'
] 