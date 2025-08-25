# Dynamic Prompting System for SerenityCoach

## Overview

The Dynamic Prompting System is the core innovation of SerenityCoach, enabling the AI assistant to automatically adapt its behavior, tone, and response strategy based on real-time context. This system goes beyond static prompts by incorporating user profiles, emotional states, available tools, and conversation history to create truly personalized interactions.

## 🚀 Key Features

### 1. **Context-Aware Prompt Generation**

- Automatically adapts prompts based on user's current emotional state
- Incorporates real-time mood, energy, and stress levels
- Considers available time and user preferences

### 2. **Risk Assessment & Safety**

- Real-time risk level assessment using multiple indicators
- Automatic escalation to crisis mode when needed
- Built-in safety measures and crisis resources

### 3. **Tool Integration**

- Dynamically includes relevant tools based on context
- Adapts tool suggestions to user's current needs
- Prioritizes tools based on effectiveness and time requirements

### 4. **Memory & Learning**

- Maintains conversation history for context
- Learns from user interactions and preferences
- Provides continuity across sessions

### 5. **Adaptive Response Planning**

- Creates personalized response strategies
- Adjusts tone and approach based on user state
- Optimizes for user's current capacity and needs

## 🏗️ Architecture

```
User Input → Profile Analysis → Context Creation → Risk Assessment → Dynamic Prompt Generation → AI Response → Memory Update
     ↓              ↓              ↓              ↓                    ↓                    ↓            ↓
Mood/Energy    Persona/Expertise  History/Activity  Safety Check    Context + Tools    Personalized   Learning
```

## 📋 Core Components

### DynamicPrompter Class

The main orchestrator that manages all dynamic prompting functionality.

```python
from dynamic_prompter import DynamicPrompter

prompter = DynamicPrompter()
```

### UserProfile Dataclass

Stores comprehensive user information for personalization.

```python
from dynamic_prompter import UserProfile

profile = UserProfile(
    persona="busy professional",
    expertise_level="beginner",
    mood="overwhelmed",
    energy=3,
    stress=8,
    sleep_quality=4,
    hobbies=["reading", "walking"],
    time_available=20
)
```

### DynamicContext Dataclass

Manages real-time context information.

```python
from dynamic_prompter import DynamicContext

context = DynamicContext(
    memory_summary="User has been stressed for the past week",
    retrieved_knowledge=["Breathing techniques", "Stress management"],
    recent_activity=["Completed breathing exercise", "Missed morning walk"]
)
```

### Tool Class

Represents available tools and their capabilities.

```python
from dynamic_prompter import Tool

tool = Tool(
    name="breathing_exercises",
    description="Guided breathing techniques for stress relief",
    input_schema={"technique": "str", "duration": "int"},
    output_schema={"instructions": "str", "benefits": "str"}
)
```

## 🔧 Usage Examples

### Basic Dynamic Prompt Generation

```python
# Create a dynamic prompt for motivation mode
prompt = prompter.create_dynamic_prompt(
    mode="motivation",
    user_profile=profile,
    context=context,
    available_tools=tools
)

# Generate AI response
response = ai_model.generate_content(prompt)
```

### Risk Assessment

```python
# Assess risk level automatically
risk_level = prompter._assess_risk_level(profile, context)

# Risk levels: "low", "medium", "high"
if risk_level == "high":
    # Automatically switch to crisis mode
    prompt = prompter.create_dynamic_prompt("crisis", profile, context, tools)
```

### Adaptive Response Planning

```python
# Create personalized response strategy
plan = prompter.create_adaptive_response_plan(profile, context, tools)

print(f"Primary Approach: {plan['primary_approach']}")
print(f"Response Style: {plan['response_style']}")
print(f"Suggested Tools: {plan['suggested_tools']}")
print(f"Safety Measures: {plan['safety_measures']}")
```

### Memory Management

```python
# Add conversation to memory
prompter.add_conversation_memory(
    user_id="user123",
    message={
        "content": "I'm feeling really stressed",
        "role": "user",
        "mood": "stressed",
        "risk_indicators": []
    }
)

# Get conversation summary for context
summary = prompter.get_conversation_summary("user123")
```

## 🎯 Prompt Modes

### 1. **Motivation Mode**

- Generates structured JSON responses
- Includes motivational quotes, actions, and wellness tips
- Adapts to user's current state and preferences

### 2. **Chat Mode**

- Provides conversational support
- Maintains context across turns
- Offers practical coping strategies

### 3. **Crisis Mode**

- Automatically activated for high-risk situations
- Provides immediate safety guidance
- Includes crisis resources and professional help encouragement

## ⚙️ Configuration

The system is highly configurable through the `config.py` file:

```python
from config import PROMPTING_CONFIG, SAFETY_CONFIG

# Risk thresholds
stress_threshold = PROMPTING_CONFIG["risk_thresholds"]["stress_high"]

# Safety settings
crisis_response = SAFETY_CONFIG["crisis_response"]["immediate_safety_check"]
```

### Key Configuration Areas:

- **Risk Assessment Thresholds**: Customize when risk levels change
- **Response Adaptation**: Configure how responses adapt to user state
- **Memory Settings**: Control conversation history and context window
- **Tool Integration**: Manage tool availability and relevance
- **Safety Configuration**: Customize crisis response and escalation

## 🔒 Safety Features

### Risk Detection

- Monitors for concerning language patterns
- Tracks stress, energy, and sleep indicators
- Identifies escalation patterns over time

### Crisis Response

- Automatic crisis mode activation
- Immediate safety assessment
- Crisis resource provision
- Professional help encouragement

### Escalation Triggers

- Multiple risk mentions
- Consecutive high-stress days
- Sleep deprivation patterns

## 📊 Adaptive Behavior Examples

### High Stress Scenario

```
User Profile: stress=9, energy=2, time=15min
→ Primary Approach: calming
→ Suggested Tools: breathing_exercises, crisis_resources
→ Response Style: gentle, supportive
→ Safety Measures: stress_monitoring, crisis_resources
```

### Low Energy Scenario

```
User Profile: energy=1, stress=6, time=45min
→ Primary Approach: gentle
→ Suggested Tools: micro_actions, hobby_integration
→ Response Style: encouraging
→ Safety Measures: energy_monitoring
```

### Limited Time Scenario

```
User Profile: time=10min, energy=5, stress=4
→ Primary Approach: supportive
→ Suggested Tools: quick_exercises
→ Response Style: concise
→ Safety Measures: standard
```

## 🧪 Testing and Demonstration

Run the demonstration script to see the system in action:

```bash
python demo_dynamic_prompting.py
```

This will showcase:

- Different user profile adaptations
- Context-aware prompt generation
- Risk assessment scenarios
- Tool integration examples
- Memory and learning capabilities

## 🔄 Integration with Main Application

The dynamic prompting system is seamlessly integrated into SerenityCoach:

```python
# In main.py
class SerenityCoach:
    def __init__(self):
        self.dynamic_prompter = DynamicPrompter()
        self.available_tools = self._initialize_tools()

    def _generate_response(self, mode: str, user_input: str = None):
        # Create dynamic context
        context = self._create_dynamic_context(user_input)

        # Generate dynamic prompt
        dynamic_prompt = self.dynamic_prompter.create_dynamic_prompt(
            mode=mode,
            user_profile=self.user_profile,
            context=context,
            available_tools=self.available_tools
        )

        # Generate AI response
        response = self.model.generate_content(dynamic_prompt)
        return response.text
```

## 🚀 Advanced Features

### Template Export

Export prompt templates for external use:

```python
# Export as YAML
yaml_template = prompter.export_prompt_template("motivation", "yaml")

# Export as JSON
json_template = prompter.export_prompt_template("chat", "json")
```

### Custom Instructions

Add custom instructions to any prompt:

```python
prompt = prompter.create_dynamic_prompt(
    mode="chat",
    user_profile=profile,
    context=context,
    available_tools=tools,
    custom_instructions="Focus on work-life balance tips"
)
```

### Tool Recommendations

Get intelligent tool suggestions:

```python
from config import get_tool_recommendations

recommendations = get_tool_recommendations(
    user_profile={"stress": 8, "energy": 2, "time_available": 20},
    context={"risk_level": "medium"}
)
# Returns: ['breathing_exercises', 'crisis_resources', 'micro_actions']
```

## 📈 Performance and Scalability

### Memory Management

- Efficient conversation history storage
- Configurable memory limits
- Automatic cleanup of old messages

### Context Optimization

- Smart context window sizing
- Relevant knowledge prioritization
- Efficient context summarization

### Tool Integration

- Lazy tool loading
- Relevance scoring
- Automatic tool filtering

## 🔮 Future Enhancements

### Planned Features:

- **Multi-modal Context**: Image, audio, and sensor data integration
- **Advanced Learning**: Machine learning-based adaptation
- **Real-time Monitoring**: Continuous risk assessment
- **Integration APIs**: External tool and service connections
- **Personalization Engine**: Advanced user preference learning

### Extensibility:

- **Plugin System**: Custom tool and context providers
- **Template Engine**: Customizable prompt templates
- **Rule Engine**: Configurable adaptation rules
- **Analytics**: Usage and effectiveness tracking

## 🛠️ Troubleshooting

### Common Issues:

1. **Import Errors**: Ensure all dependencies are installed
2. **Configuration Issues**: Check `config.py` for proper settings
3. **Memory Issues**: Adjust memory settings in configuration
4. **Tool Integration**: Verify tool definitions and availability

### Debug Mode:

Enable debug mode for detailed logging:

```python
import os
os.environ['SERENITY_ENV'] = 'development'
```

## 📚 Best Practices

### 1. **User Profile Management**

- Collect comprehensive initial profiles
- Update profiles based on interactions
- Respect user privacy and preferences

### 2. **Context Creation**

- Include relevant conversation history
- Add retrieved knowledge when available
- Monitor for context changes

### 3. **Safety Implementation**

- Always prioritize user safety
- Implement proper escalation procedures
- Maintain crisis resource lists

### 4. **Tool Integration**

- Define clear tool schemas
- Implement proper error handling
- Monitor tool effectiveness

## 🤝 Contributing

To contribute to the dynamic prompting system:

1. **Fork the repository**
2. **Create a feature branch**
3. **Implement your changes**
4. **Add tests and documentation**
5. **Submit a pull request**

### Development Guidelines:

- Follow the existing code structure
- Add comprehensive documentation
- Include test coverage
- Maintain backward compatibility

## 📄 License

This project is part of the SerenityCoach mental health companion system, developed as part of learning GenAI agent design.

---

## 🎯 Quick Start Checklist

- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set up environment variables: `GOOGLE_API_KEY`
- [ ] Run demonstration: `python demo_dynamic_prompting.py`
- [ ] Test main application: `python main.py --chat`
- [ ] Explore configuration: `config.py`
- [ ] Customize settings for your use case

The Dynamic Prompting System transforms static AI interactions into adaptive, context-aware conversations that truly understand and respond to the user's current needs and situation.
