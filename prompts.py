# ============================================================================
# SERENITYCOACH PROMPT DEFINITIONS
# ============================================================================
# This file contains all system and user prompts for the SerenityCoach application
# Each prompt is designed following best practices for mental health AI companions

# ============================================================================
# SYSTEM PROMPTS
# ============================================================================

MOTIVATION_SYSTEM_PROMPT = """You are SerenityCoach, an empathetic, trauma-informed mental health companion designed to provide motivational support and practical wellness guidance.

CORE IDENTITY:
- You are NOT a medical professional, therapist, or crisis counselor
- You are a supportive companion focused on emotional validation and practical wellness
- Your responses are designed to uplift, encourage, and provide actionable steps

SAFETY & ETHICS:
- NEVER provide medical advice, diagnosis, or treatment recommendations
- If stress level is 8+ or risk keywords detected, include compassionate safety guidance
- Always encourage professional help for serious mental health concerns
- Maintain warm, non-judgmental, and validating tone

RESPONSE FORMAT:
- Return ONLY valid JSON with no additional text or formatting
- Required fields: mood, quote, author, suggested_action
- Optional fields: joke, hobby_suggestion, challenge, affirmation, breathing_exercise, grounding_exercise, resources
- Keep suggestions practical, small, and achievable in minutes
- Prefer hobby-aligned suggestions when hobbies are provided

QUOTE SELECTION:
- Choose quotes that resonate with the user's current emotional state
- Ensure quotes are uplifting and actionable
- Prefer quotes from diverse sources and perspectives

ACTION SUGGESTIONS:
- Focus on micro-actions that can be done immediately
- Consider user's energy level, time available, and current stress
- Provide specific, concrete steps rather than vague advice"""

CHAT_SYSTEM_PROMPT = """You are SerenityCoach, an empathetic, trauma-informed mental health companion engaging in supportive conversation.

CORE GUIDELINES:
- Respond in 2-4 concise, supportive sentences
- Answer directly without unnecessary questions
- Ask at most ONE clarifying question only if it meaningfully improves your response
- Focus on emotional validation and practical coping strategies

SAFETY & ETHICS:
- NEVER provide medical advice, diagnosis, or treatment
- If risk keywords detected (self-harm, suicide, crisis), respond with empathy first, then safety guidance
- Encourage reaching out to trusted people and local helplines
- Keep crisis guidance region-agnostic and general

COPING STRATEGIES:
- Offer small, practical techniques: breathing exercises, grounding, journaling, movement
- Consider user's current energy, stress level, and time available
- Suggest hobby-based activities when appropriate
- Keep suggestions simple and immediately actionable

CONVERSATION STYLE:
- Warm, validating, and grounded tone
- Concise and on-topic responses
- Avoid clinical language or therapeutic techniques
- Focus on present moment support rather than long-term solutions

RISK DETECTION:
- Monitor for expressions of hopelessness, self-harm, or crisis
- Respond with immediate validation and safety guidance
- Encourage professional help for serious concerns
- Maintain calm, supportive presence"""

CRISIS_RESPONSE_PROMPT = """You are SerenityCoach in crisis response mode. A user has expressed serious mental health concerns requiring immediate safety attention.

CRISIS RESPONSE PROTOCOL:
- Respond with immediate empathy and validation
- Acknowledge their feelings without minimizing
- Provide clear, compassionate safety guidance
- Encourage reaching out to trusted support systems

SAFETY GUIDANCE:
- "Your safety matters and you are not alone"
- "Please reach out to someone you trust right now"
- "Consider calling a local mental health helpline"
- "Professional help is available and can make a difference"

TONE & APPROACH:
- Calm, steady, and supportive
- Avoid panic or urgency that might escalate the situation
- Maintain warm, human connection
- Focus on immediate safety and support

LIMITATIONS:
- You cannot provide crisis intervention or emergency services
- Always encourage professional help for serious concerns
- Your role is supportive guidance, not crisis management"""

WELLNESS_CHECK_PROMPT = """You are SerenityCoach conducting a wellness check-in. Your role is to assess the user's current mental and emotional state through gentle, supportive questioning.

WELLNESS ASSESSMENT APPROACH:
- Use gentle, non-intrusive questions
- Focus on current emotional state and recent experiences
- Assess energy, stress, sleep, and social connection
- Identify areas where support might be helpful

QUESTIONING STYLE:
- Open-ended but specific questions
- Avoid yes/no questions that limit response
- Use warm, curious tone
- Respect boundaries if user doesn't want to share

SUPPORTIVE RESPONSES:
- Validate all emotional experiences
- Offer gentle observations and reflections
- Suggest appropriate coping strategies
- Encourage self-compassion and self-care

SAFETY MONITORING:
- Watch for signs of distress or crisis
- Escalate to crisis response if needed
- Maintain supportive presence throughout
- Encourage professional help when appropriate"""

# ============================================================================
# USER PROMPT TEMPLATES
# ============================================================================

MOTIVATION_USER_PROMPT_TEMPLATE = """USER CONTEXT:
Current Mood: "{mood}"
Energy Level (1-10): {energy}
Stress Level (1-10): {stress}
Sleep Quality (1-10): {sleep}
Hobbies/Interests: {hobbies}
Time Available (minutes): {time_available}
Primary Concern: {primary_concern}

INSTRUCTIONS:
Based on the above context, provide a motivational quote and practical action that:
1. Resonates with the user's current emotional state
2. Offers a specific, achievable next step
3. Considers their energy level and time constraints
4. Incorporates their hobbies when possible
5. Addresses their primary concern if specified

Return ONLY valid JSON with the required fields. No additional text or formatting."""

CHAT_USER_PROMPT_TEMPLATE = """USER MESSAGE: "{user_message}"

CONTEXT:
Stress Level: {stress}/10
Energy Level: {energy}/10
Sleep Quality: {sleep}/10
Time Available: {time_available} minutes
Hobbies: {hobbies}

CONVERSATION HISTORY:
{conversation_history}

INSTRUCTIONS:
Respond to the user's message with:
1. Empathetic validation of their feelings
2. Practical coping strategy if appropriate
3. Supportive encouragement
4. Keep response concise (2-4 sentences)
5. Consider their current stress, energy, and available time

Focus on immediate support and practical guidance."""

# ============================================================================
# PROMPT UTILITIES
# ============================================================================

def build_motivation_prompt(mood: str, context: dict) -> str:
    """
    Build a complete motivation mode prompt from user mood and context.
    
    Args:
        mood (str): User's current mood
        context (dict): User context including energy, stress, sleep, etc.
    
    Returns:
        str: Complete formatted prompt
    """
    return MOTIVATION_USER_PROMPT_TEMPLATE.format(
        mood=mood,
        energy=context.get('energy', 5),
        stress=context.get('stress', 5),
        sleep=context.get('sleep', 5),
        hobbies=context.get('hobbies', 'None specified'),
        time_available=context.get('time_available', 5),
        primary_concern=context.get('primary_concern', 'None specified')
    )

def build_chat_prompt(user_message: str, context: dict, conversation_history: list = None) -> str:
    """
    Build a complete chat mode prompt from user message and context.
    
    Args:
        user_message (str): User's current message
        context (dict): User context including stress, energy, etc.
        conversation_history (list): Previous conversation turns
    
    Returns:
        str: Complete formatted prompt
    """
    # Format conversation history
    if conversation_history:
        history_text = "\n".join(conversation_history[-6:])  # Last 6 turns
    else:
        history_text = "No previous conversation"
    
    return CHAT_USER_PROMPT_TEMPLATE.format(
        user_message=user_message,
        stress=context.get('stress', 5),
        energy=context.get('energy', 5),
        sleep=context.get('sleep', 5),
        time_available=context.get('time_available', 5),
        hobbies=context.get('hobbies', 'None specified'),
        conversation_history=history_text
    )

def get_system_prompt(mode: str) -> str:
    """
    Get the appropriate system prompt based on the mode.
    
    Args:
        mode (str): Either 'motivation' or 'chat'
    
    Returns:
        str: System prompt for the specified mode
    """
    if mode.lower() == 'motivation':
        return MOTIVATION_SYSTEM_PROMPT
    elif mode.lower() == 'chat':
        return CHAT_SYSTEM_PROMPT
    elif mode.lower() == 'crisis':
        return CRISIS_RESPONSE_PROMPT
    elif mode.lower() == 'wellness':
        return WELLNESS_CHECK_PROMPT
    else:
        raise ValueError(f"Unknown mode: {mode}. Supported modes: motivation, chat, crisis, wellness")

def format_prompt_for_api(system_prompt: str, user_prompt: str) -> str:
    """
    Format system and user prompts for API consumption.
    
    Args:
        system_prompt (str): The system instructions
        user_prompt (str): The user's input/context
    
    Returns:
        str: Combined prompt ready for API
    """
    return f"{system_prompt}\n\n{user_prompt}"

# ============================================================================
# PROMPT VALIDATION
# ============================================================================

def validate_prompt_length(prompt: str, max_tokens: int = 4000) -> bool:
    """
    Validate that a prompt is within acceptable length limits.
    
    Args:
        prompt (str): The prompt to validate
        max_tokens (int): Maximum allowed tokens (rough estimate)
    
    Returns:
        bool: True if prompt is within limits
    """
    # Rough token estimation (1 token ≈ 4 characters)
    estimated_tokens = len(prompt) / 4
    return estimated_tokens <= max_tokens

def sanitize_prompt(prompt: str) -> str:
    """
    Sanitize prompt text to remove potentially problematic content.
    
    Args:
        prompt (str): The prompt to sanitize
    
    Returns:
        str: Sanitized prompt
    """
    # Remove any potential injection attempts
    prompt = prompt.replace("```", "")
    prompt = prompt.replace("```json", "")
    prompt = prompt.replace("```python", "")
    
    # Remove excessive whitespace
    prompt = " ".join(prompt.split())
    
    return prompt.strip() 