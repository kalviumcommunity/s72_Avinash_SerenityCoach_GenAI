# SerenityCoach Prompt System - Quick Reference

## 🎯 Overview

Comprehensive prompt system for a mental health AI companion that provides motivational support and empathetic conversation while maintaining strict safety boundaries.

## 🚀 Key Features

### **Safety First**

- ❌ No medical advice or diagnosis
- ✅ Crisis detection and response protocols
- ✅ Professional help encouragement
- ✅ Trauma-informed communication

### **Multiple Modes**

1. **Motivation Mode** - Quotes + actionable guidance
2. **Chat Mode** - Supportive conversation + coping strategies
3. **Crisis Response** - Safety guidance for serious concerns
4. **Wellness Check** - Gentle mental health assessment

## 📝 Prompt Structure

### System Prompts

- Define AI role and behavior
- Set safety boundaries
- Establish response guidelines
- Include ethical considerations

### User Prompts

- Provide user context
- Include conversation history
- Specify response requirements
- Maintain conversation flow

## 🔧 Usage Examples

```python
from prompts import get_system_prompt, build_motivation_prompt

# Get system prompt
system_prompt = get_system_prompt('motivation')

# Build user prompt
user_prompt = build_motivation_prompt("anxious", user_context)

# Combine for API
complete_prompt = f"{system_prompt}\n\n{user_prompt}"
```

## 🛡️ Safety Protocols

### Risk Detection

- Self-harm language
- Suicide ideation
- Crisis expressions
- High stress levels (8+)

### Response Guidelines

- Immediate empathy
- Safety guidance
- Professional help encouragement
- Calm, supportive presence

## 📊 Response Formats

### Motivation Mode

```json
{
  "mood": "anxious",
  "quote": "Quote text",
  "author": "Author name",
  "suggested_action": "Practical step",
  "breathing_exercise": "Optional",
  "resources": "Safety info if needed"
}
```

### Chat Mode

- 2-4 concise sentences
- Empathetic validation
- Practical coping strategies
- Supportive encouragement

## 🎨 Customization

### Adding New Modes

1. Define system prompt constant
2. Add to `get_system_prompt()` function
3. Create user prompt template
4. Add utility functions

### Modifying Prompts

1. Update prompt constants
2. Test with various inputs
3. Validate safety protocols
4. Update documentation

## 🧪 Testing

### Prompt Validation

- Length checking
- Content sanitization
- Safety protocol verification
- Response consistency testing

### Safety Testing

- Crisis response protocols
- Risk detection accuracy
- Medical disclaimer effectiveness
- Escalation procedures

## 📁 Files

- `prompts.py` - Core prompt definitions and utilities
- `PROMPT_GUIDE.md` - Comprehensive usage guide
- `prompt_example.py` - Working examples
- `PROMPT_SUMMARY.md` - This quick reference

## 🚨 Important Notes

1. **Always use utility functions** for consistency
2. **Validate prompts** before API calls
3. **Monitor safety protocols** continuously
4. **Test thoroughly** with various scenarios
5. **Maintain ethical boundaries** at all times

## 🔗 Integration

The prompt system integrates seamlessly with the existing SerenityCoach application:

- Import prompts module
- Use utility functions
- Maintain safety protocols
- Monitor and log usage

---

_This prompt system ensures safe, empathetic, and effective mental health support while maintaining clear boundaries and professional standards._
