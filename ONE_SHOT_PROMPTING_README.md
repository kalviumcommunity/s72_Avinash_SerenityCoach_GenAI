# One-Shot Prompting Implementation in SerenityCoach

## Overview

This project demonstrates the implementation of **one-shot prompting** in the SerenityCoach mental health companion application. One-shot prompting provides the AI model with a single example along with instructions, ensuring consistent, high-quality responses.

## What is One-Shot Prompting?

One-shot prompting is a technique where you provide the AI model with:

1. **Clear instructions** about what to do
2. **Constraints and guidelines** to follow
3. **One concrete example** showing the desired output format and style
4. **The actual input** to process

This approach reduces ambiguity and ensures the model produces consistent, well-formatted responses.

## Implementation in SerenityCoach

### 1. Core One-Shot Prompting Class

The `OneShotPrompter` class in `prompts.py` provides the foundation:

```python
class OneShotPrompter:
    def __init__(self):
        # Pre-defined examples for consistent responses
        self.motivation_example = {...}
        self.chat_example = {...}

    def create_motivation_prompt(self, mood, energy, stress, sleep, hobbies, time_available):
        # Generates one-shot prompts for motivation mode
```

### 2. Motivation Mode One-Shot Prompt

**Structure:**

- Role definition (SerenityCoach)
- Task description
- Constraints and safety guidelines
- Format specification
- **One complete example** with inputs and outputs
- Actual user inputs to process

**Example:**

```python
prompt = get_motivation_prompt(
    mood="overwhelmed",
    energy=3,
    stress=8,
    sleep=4,
    hobbies="reading, music",
    time_available=10
)
```

**Generated Prompt:**

```
You are SerenityCoach, an empathetic, non-clinical mental health companion.
Task: Generate exactly one JSON object based on the user's mood and optional context...

Example inputs:
- mood="overwhelmed"
- energy=3
- stress=8
- sleep=4
- hobbies="reading, music"
- time_available=10

Example output (JSON):
{
  "mood": "overwhelmed",
  "quote": "You don't have to see the whole staircase; just take the first step.",
  "author": "Martin Luther King Jr.",
  "suggested_action": "Do 2 minutes of box breathing, then write one tiny next step you can do now.",
  "breathing_exercise": "Inhale 4, hold 4, exhale 4, hold 4 for 2 minutes.",
  "resources": "If you feel unsafe or overwhelmed, consider reaching out to someone you trust or a local helpline."
}

Now generate the JSON for these inputs:
- mood="tired"
- energy=2
- stress=7
- sleep=3
- hobbies="reading, music, walking"
- time_available=20

Return only the JSON.
```

### 3. Chat Mode One-Shot Prompt

**Structure:**

- Role and task definition
- Response constraints
- Tone guidelines
- **One conversation example** showing the desired interaction style
- User message to respond to

**Example:**

```python
prompt = get_chat_prompt(
    user_message="I'm feeling really anxious about my presentation tomorrow",
    energy=4,
    stress=8,
    sleep=5,
    hobbies="yoga, cooking",
    time_available=15
)
```

## Benefits of One-Shot Prompting

### 1. **Consistency**

- Every response follows the same format and tone
- Reduced variability in AI outputs
- Predictable response structure

### 2. **Quality Assurance**

- Example demonstrates the expected quality level
- Model learns from the provided example
- Fewer formatting errors

### 3. **Safety Integration**

- Example includes safety considerations
- Risk assessment guidelines are demonstrated
- Ethical boundaries are clearly shown

### 4. **Efficiency**

- Faster response generation
- Less need for post-processing
- Reduced API calls for corrections

## Comparison: Zero-Shot vs One-Shot

| Aspect               | Zero-Shot | One-Shot   |
| -------------------- | --------- | ---------- |
| **Instructions**     | ✅        | ✅         |
| **Constraints**      | ✅        | ✅         |
| **Example**          | ❌        | ✅         |
| **Consistency**      | Medium    | High       |
| **Format Accuracy**  | Medium    | High       |
| **Tone Consistency** | Variable  | Consistent |
| **Error Rate**       | Higher    | Lower      |

## Usage Examples

### Basic Usage

```python
from prompts import get_motivation_prompt, get_chat_prompt

# Motivation mode
motivation_prompt = get_motivation_prompt(
    mood="anxious",
    energy=3,
    stress=8,
    sleep=4,
    hobbies="meditation, walking",
    time_available=30
)

# Chat mode
chat_prompt = get_chat_prompt(
    user_message="I can't stop worrying about work",
    stress=9,
    energy=2
)
```

### Custom One-Shot Prompts

```python
from prompts import OneShotPrompter

prompter = OneShotPrompter()

# Create custom prompt for journaling
custom_prompt = f"""You are SerenityCoach, helping users with journaling prompts.
Task: Generate a reflective journaling question based on the user's mood.

Example:
User mood: "stressed"
Journaling question: "What's one small thing that brought you joy today, even in the midst of stress?"

Now generate a journaling question for:
User mood: "grateful"

Return only the question:"""
```

## File Structure

```
s72_Avinash_SerenityCoach_GenAI/
├── prompts.py              # One-shot prompting utilities
├── main.py                 # Main SerenityCoach application
├── demo_one_shot.py        # Demonstration script
├── requirements.txt        # Dependencies
└── ONE_SHOT_PROMPTING_README.md  # This file
```

## Running the Project

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file:

```bash
GOOGLE_API_KEY=your_api_key_here
```

### 3. Run the Application

```bash
# Motivation mode
python main.py

# Chat mode
python main.py --chat

# With specific mood
python main.py --mood "tired"
```

### 4. Run the Demo

```bash
python demo_one_shot.py
```

## Key Features

### 1. **Structured Output**

- JSON responses for motivation mode
- Consistent text responses for chat mode
- Optional fields for additional context

### 2. **Safety Integration**

- Risk keyword detection
- Safety notes for high-stress situations
- Ethical boundaries maintained

### 3. **Context Awareness**

- Energy, stress, and sleep levels
- Hobby preferences
- Time availability constraints

### 4. **Extensibility**

- Easy to add new prompt types
- Customizable examples
- Modular design

## Best Practices

### 1. **Example Selection**

- Choose representative examples
- Include edge cases when relevant
- Ensure examples follow all constraints

### 2. **Prompt Structure**

- Clear task definition
- Specific constraints
- One well-formed example
- Clear input specification

### 3. **Safety Considerations**

- Always include safety guidelines
- Demonstrate risk assessment
- Provide appropriate resources

### 4. **Testing and Validation**

- Test with various inputs
- Validate output format
- Check safety mechanisms

## Future Enhancements

### 1. **Multi-Shot Prompting**

- Multiple examples for complex tasks
- Different response styles
- Context-specific examples

### 2. **Dynamic Examples**

- User preference-based examples
- Cultural adaptation
- Personalized prompting

### 3. **Advanced Safety**

- Real-time risk assessment
- Escalation procedures
- Professional referral integration

## Conclusion

The one-shot prompting implementation in SerenityCoach demonstrates how to create consistent, high-quality AI responses while maintaining safety and ethical considerations. By providing clear examples alongside instructions, the system ensures reliable outputs that users can depend on.

This approach is particularly valuable for mental health applications where consistency, safety, and appropriate tone are crucial for user trust and well-being.

---

**Note:** This implementation is for educational and demonstration purposes. In production use, ensure proper API integration, error handling, and professional mental health oversight.
