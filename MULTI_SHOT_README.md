# Multi-Shot Prompting in SerenityCoach

This document explains the implementation and usage of multi-shot prompting in the SerenityCoach mental health companion project.

## 🎯 What is Multi-Shot Prompting?

Multi-shot prompting is an advanced technique that provides the AI model with multiple illustrative examples alongside instructions and constraints. This approach helps the model:

- **Learn consistent patterns** from multiple examples
- **Handle edge cases** more reliably (e.g., crisis situations)
- **Maintain consistent tone and style** across responses
- **Improve JSON formatting** accuracy in structured outputs
- **Better understand context** and user intent

## 🏗️ Architecture Overview

```
SerenityCoach/
├── multi_shot_prompter.py    # Core multi-shot prompting utility
├── main.py                   # Main application with multi-shot integration
├── demo_multi_shot.py        # Demonstration script
├── requirements.txt          # Dependencies
└── MULTI_SHOT_README.md     # This documentation
```

## 🔧 Core Components

### 1. MultiShotPrompter Class

The main utility class that manages multi-shot prompts:

```python
from multi_shot_prompter import MultiShotPrompter

prompter = MultiShotPrompter()

# Generate motivation prompt with multiple examples
motivation_prompt = prompter.get_motivation_prompt(
    mood="anxious",
    energy=4,
    stress=7,
    sleep=5,
    hobbies="art, running",
    time_available=5
)

# Generate chat prompt with multiple examples
chat_prompt = prompter.get_chat_prompt(
    user_message="I'm feeling overwhelmed",
    stress=8,
    energy=2,
    sleep=3,
    time_available=10,
    hobbies="music, walking"
)
```

### 2. PromptExample Dataclass

Represents individual examples for multi-shot prompting:

```python
from multi_shot_prompter import PromptExample

example = PromptExample(
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
)
```

## 📚 Built-in Examples

### Motivation Mode Examples (5 examples)

1. **Anxious Mood** - Art hobby focus with grounding exercises
2. **Tired Mood** - Gaming hobby with rest suggestions
3. **Overwhelmed Mood** - High stress with crisis resources
4. **Excited Mood** - Positive energy with hobby suggestions
5. **Lonely Mood** - Creative hobbies with connection tips

### Chat Mode Examples (5 examples)

1. **Presentation Anxiety** - Practical preparation tips
2. **Procrastination Guilt** - Small step approach
3. **Crisis Response** - Safety and support guidance
4. **Positive Mood Support** - Celebration and sharing
5. **Chronic Worry** - Time-boxed worry technique

### Crisis Response Examples (3 examples)

1. **Suicidal Ideation** - Immediate safety guidance
2. **Self-Harm Thoughts** - Crisis intervention
3. **Hopelessness** - Support and professional help

## 🚀 Usage Examples

### Basic Usage

```python
from multi_shot_prompter import MultiShotPrompter

# Initialize the prompter
prompter = MultiShotPrompter()

# Get motivation prompt
prompt = prompter.get_motivation_prompt(
    mood="stressed",
    energy=3,
    stress=8,
    sleep=4,
    hobbies="reading, yoga",
    time_available=15
)

# Use with your AI model
response = ai_model.generate(prompt)
```

### Adding Custom Examples

```python
# Create a new example
new_example = PromptExample(
    inputs={"mood": "grateful", "energy": 9, "stress": 1},
    output=json.dumps({
        "mood": "grateful",
        "quote": "Gratitude turns what we have into enough.",
        "author": "Melody Beattie",
        "suggested_action": "Write down 3 things you're grateful for."
    }),
    description="Positive grateful mood"
)

# Add to the prompter
prompter.add_example("motivation", new_example)
```

### Custom Multi-Shot Prompts

```python
custom_examples = [
    PromptExample(
        inputs={"emotion": "frustrated", "context": "work deadline"},
        output="Take a 5-minute break, then break the task into 3 smaller steps.",
        description="Work frustration"
    ),
    # ... more examples
]

custom_prompt = prompter.get_custom_prompt(
    examples=custom_examples,
    task_description="Provide emotional support and practical advice.",
    constraints="Keep responses under 2 sentences. Be empathetic.",
    user_input="emotion='confused', context='career decision'"
)
```

## 📊 Comparison with Other Approaches

### Zero-Shot vs One-Shot vs Multi-Shot

| Approach       | Examples | Consistency | Edge Case Handling | Response Quality |
| -------------- | -------- | ----------- | ------------------ | ---------------- |
| **Zero-Shot**  | 0        | Low         | Poor               | Variable         |
| **One-Shot**   | 1        | Medium      | Fair               | Good             |
| **Multi-Shot** | 5+       | High        | Excellent          | Excellent        |

### Example Length Comparison

- **Zero-Shot**: ~200 characters
- **One-Shot**: ~400 characters
- **Multi-Shot**: ~1500+ characters

## 🎮 Running the Project

### 1. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set your Google API key
export GOOGLE_API_KEY="your_api_key_here"
# or create a .env file with GOOGLE_API_KEY=your_key
```

### 2. Basic Usage

```bash
# Interactive motivation mode
python main.py

# Quick motivation for specific mood
python main.py --mood "tired"

# Live chat mode
python main.py --chat

# Show multi-shot examples
python main.py --examples
```

### 3. Demonstration

```bash
# Run the multi-shot prompting demonstration
python demo_multi_shot.py
```

## 🔍 Prompt Structure Analysis

### Motivation Mode Prompt Structure

```
1. Role Definition (SerenityCoach)
2. Task Description (Generate JSON)
3. Constraints (Safety, ethics, format)
4. Format Specification (Required/optional fields)
5. Multiple Examples (5 detailed examples)
6. User Input
7. Output Instructions
```

### Chat Mode Prompt Structure

```
1. Role Definition (SerenityCoach)
2. Task Description (2-4 sentence response)
3. Constraints (Coping strategies, safety)
4. Multiple Examples (5 chat + 3 crisis examples)
5. User Input
6. Safety Reminders
```

## 🛡️ Safety Features

### Risk Detection

- **Keyword monitoring** for crisis situations
- **Stress level assessment** (≥8 triggers safety notes)
- **Crisis response examples** for immediate intervention
- **Fallback responses** when AI is unavailable

### Crisis Response

- **Immediate safety guidance**
- **Helpline information** (region-agnostic)
- **Trusted person encouragement**
- **Professional help recommendations**

## 📈 Benefits of Multi-Shot Prompting

### 1. **Consistency**

- Same tone and style across all responses
- Consistent JSON formatting in motivation mode
- Reliable crisis detection and response

### 2. **Reliability**

- Better handling of edge cases
- Improved understanding of user context
- More accurate hobby and time-based suggestions

### 3. **Safety**

- Multiple crisis response examples
- Consistent safety messaging
- Better risk assessment patterns

### 4. **Personalization**

- Hobby-aligned suggestions
- Time-appropriate actions
- Energy and stress level consideration

## 🔧 Customization

### Adding New Mood Types

```python
# Add new mood example
new_mood_example = PromptExample(
    inputs={"mood": "creative_block", "energy": 6, "stress": 4},
    output=json.dumps({
        "mood": "creative_block",
        "quote": "Creativity is intelligence having fun.",
        "author": "Albert Einstein",
        "suggested_action": "Try a different medium or take a 10-minute break.",
        "hobby_suggestion": "Switch from digital to paper, or vice versa."
    }),
    description="Creative block with medium switching"
)

prompter.add_example("motivation", new_mood_example)
```

### Modifying Existing Examples

```python
# Access and modify examples
anxious_example = prompter.motivation_examples[0]
anxious_example.output = new_output_json
anxious_example.description = "Updated anxious mood example"
```

## 🧪 Testing and Validation

### Running Tests

```bash
# Test the multi-shot prompter
python -c "
from multi_shot_prompter import MultiShotPrompter
prompter = MultiShotPrompter()
print(f'Examples loaded: {prompter.get_example_count()}')
print('✅ Multi-shot prompter working correctly!')
"
```

### Validation Checks

- **JSON format validation** for motivation responses
- **Required field checking** (mood, quote, author, action)
- **Safety note inclusion** for high-stress situations
- **Example count verification** across all categories

## 🚀 Future Enhancements

### Planned Features

1. **Dynamic Example Loading** from external sources
2. **User Feedback Integration** to improve examples
3. **A/B Testing** different prompt structures
4. **Multilingual Support** with localized examples
5. **Context-Aware Examples** based on user history

### Extensibility

The `MultiShotPrompter` class is designed to be easily extensible:

- **New example categories** can be added
- **Custom prompt templates** supported
- **External data sources** can be integrated
- **Prompt optimization** algorithms can be added

## 📚 Additional Resources

### Documentation

- [Google Generative AI Documentation](https://ai.google.dev/docs)
- [Python Dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [JSON Schema Validation](https://json-schema.org/)

### Related Concepts

- **Few-Shot Learning** in AI
- **Prompt Engineering** best practices
- **Mental Health AI** safety guidelines
- **Conversational AI** design patterns

## 🤝 Contributing

To add new examples or improve the multi-shot prompting:

1. **Fork the repository**
2. **Add new examples** using the `PromptExample` class
3. **Test with different scenarios** to ensure consistency
4. **Update documentation** for new features
5. **Submit a pull request** with detailed descriptions

## 📄 License

This project is part of the Kalvium GenAI Workshops and follows the same licensing terms as the main SerenityCoach project.

---

**Note**: Multi-shot prompting significantly improves AI response quality and consistency, making it an essential technique for production AI applications like SerenityCoach.
