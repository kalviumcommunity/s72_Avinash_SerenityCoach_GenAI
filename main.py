import sys
import os
from prompts import zero_shot_prompt

# Gemini LLM integration
import google.generativeai as genai

def get_gemini_response(prompt: str) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "[ERROR] GOOGLE_API_KEY not set in environment."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text.strip() if hasattr(response, 'text') else str(response)

def main():
    if len(sys.argv) > 1:
        user_message = " ".join(sys.argv[1:])
    else:
        user_message = input("How are you feeling today? ")
    prompt = zero_shot_prompt(user_message)
    print("\n--- Zero-Shot Prompt Sent to LLM ---\n")
    print(prompt)
    print("\n--- LLM Response ---\n")
    response = get_gemini_response(prompt)
    print(response)

if __name__ == "__main__":
    main() 