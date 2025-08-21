# SerenityCoach Prompt System Guide

## Overview

This guide explains the comprehensive prompt system designed for SerenityCoach, a mental health companion CLI application. The prompts are structured to ensure safe, empathetic, and effective AI responses while maintaining clear boundaries around medical advice.

## Prompt Architecture

### 1. System Prompts

System prompts define the AI's role, behavior, and limitations. They are designed to be comprehensive and safety-focused.

#### Motivation Mode System Prompt

- **Purpose**: Generates motivational quotes and actionable wellness guidance
- **Key Features**:
  - Clear identity as a non-medical companion
  - Safety protocols for high-stress situations
  - Structured JSON output requirements
  - Focus on practical, achievable actions

#### Chat Mode System Prompt

- **Purpose**: Provides supportive conversation and coping strategies
- **Key Features**:
  - Concise response guidelines (2-4 sentences)
  - Risk detection and crisis response protocols
  - Practical coping strategy suggestions
  - Trauma-informed communication style

#### Crisis Response Prompt

- **Purpose**: Handles serious mental health concerns safely
- **Key Features**:
  - Immediate safety guidance
  - Professional help encouragement
  - Calm, supportive presence
  - Clear escalation protocols

#### Wellness Check Prompt

- **Purpose**: Conducts gentle mental health assessments
- **Key Features**:
  - Non-intrusive questioning approach
  - Emotional state evaluation
  - Supportive response framework
  - Safety monitoring

### 2. User Prompt Templates

User prompts provide context and specific instructions for each interaction.

#### Motivation Mode Template

```
USER CONTEXT:
Current Mood: "{mood}"
Energy Level (1-10): {energy}
Stress Level (1-10): {stress}
Sleep Quality (1-10): {sleep}
Hobbies/Interests: {hobbies}
Time Available (minutes): {time_available}
Primary Concern: {primary_concern}
```

#### Chat Mode Template

```
USER MESSAGE: "{user_message}"

CONTEXT:
Stress Level: {stress}/10
Energy Level: {energy}/10
Sleep Quality: {sleep}/10
Time Available: {time_available} minutes
Hobbies: {hobbies}

CONVERSATION HISTORY:
{conversation_history}
```

## Usage Examples

### Basic Motivation Mode

```python
from prompts import get_system_prompt, build_motivation_prompt, format_prompt_for_api

# Get the system prompt
system_prompt = get_system_prompt('motivation')

# Build user prompt with context
user_context = {
    'energy': 7,
    'stress': 6,
    'sleep': 8,
    'hobbies': 'reading, walking',
    'time_available': 15,
    'primary_concern': 'work pressure'
}

user_prompt = build_motivation_prompt("overwhelmed", user_context)

# Format for API
complete_prompt = format_prompt_for_api(system_prompt, user_prompt)
```

### Chat Mode with History

```python
from prompts import get_system_prompt, build_chat_prompt

# Get system prompt
system_prompt = get_system_prompt('chat')

# Build chat prompt with conversation history
conversation_history = [
    "User: I'm feeling really anxious today",
    "Assistant: I hear that anxiety can be really overwhelming. Let's take a moment to breathe together.",
    "User: I tried breathing but it's not helping much"
]

user_context = {
    'stress': 8,
    'energy': 4,
    'sleep': 6,
    'time_available': 10,
    'hobbies': 'yoga, music'
}

chat_prompt = build_chat_prompt(
    "What else can I try?",
    user_context,
    conversation_history
)
```

### Crisis Response

```python
from prompts import get_system_prompt

# Get crisis response prompt
crisis_prompt = get_system_prompt('crisis')

# Use when risk keywords are detected
# This should be combined with immediate safety guidance
```

## Safety Features

### 1. Risk Detection

- Monitors for self-harm, suicide, or crisis language
- Provides immediate safety guidance
- Encourages professional help
- Maintains calm, supportive presence

### 2. Medical Disclaimer

- Clear boundaries around medical advice
- Encourages professional consultation
- Focuses on wellness support, not treatment

### 3. Trauma-Informed Approach

- Validates emotional experiences
- Avoids triggering language
- Provides gentle, supportive guidance
- Respects user boundaries

## Best Practices

### 1. Prompt Construction

- Always use the utility functions for consistency
- Validate prompt length before API calls
- Sanitize user inputs to prevent injection
- Maintain context throughout conversations

### 2. Safety Monitoring

- Regularly check for risk indicators
- Escalate to crisis response when needed
- Document safety incidents appropriately
- Maintain clear escalation protocols

### 3. Response Quality

- Keep responses concise and focused
- Provide practical, actionable guidance
- Maintain empathetic, warm tone
- Avoid clinical or therapeutic language

## Customization

### Adding New Modes

1. Define new system prompt constant
2. Add mode to `get_system_prompt()` function
3. Create corresponding user prompt template
4. Add utility functions as needed

### Modifying Existing Prompts

1. Update the prompt constant
2. Test with various user inputs
3. Validate safety protocols
4. Update documentation

## Testing and Validation

### Prompt Testing

- Test with various emotional states
- Validate safety protocols
- Check response consistency
- Monitor for unintended behaviors

### Safety Validation

- Test crisis response protocols
- Validate medical disclaimer effectiveness
- Check risk detection accuracy
- Monitor escalation procedures

## Integration with Main Application

The prompts are designed to integrate seamlessly with the existing SerenityCoach application:

1. **Import the prompts module** in your main application
2. **Use utility functions** for consistent prompt construction
3. **Maintain safety protocols** throughout all interactions
4. **Monitor and log** prompt usage for quality improvement

## Troubleshooting

### Common Issues

1. **Prompt too long**: Use `validate_prompt_length()` to check
2. **Inconsistent responses**: Ensure system prompts are used consistently
3. **Safety concerns**: Verify crisis response protocols are active
4. **Format errors**: Use utility functions for proper formatting

### Debugging

1. Check prompt construction with utility functions
2. Validate system prompt selection
3. Monitor API responses for errors
4. Review conversation logs for issues

## Conclusion

This prompt system provides a robust foundation for safe, empathetic mental health support while maintaining clear boundaries and safety protocols. Regular review and updates ensure continued effectiveness and safety.
