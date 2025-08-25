import os
from typing import Optional, Dict, Any


def _print_token_usage(usage: Dict[str, Any]) -> None:
    prompt = usage.get("prompt_tokens") or usage.get("prompt_token_count")
    completion = usage.get("completion_tokens") or usage.get("candidates_token_count")
    total = usage.get("total_tokens") or usage.get("total_token_count")
    print(f"[LLM] Tokens — prompt: {prompt}, completion: {completion}, total: {total}")


def _try_openai_chat(system_prompt: str, user_prompt: str, model: Optional[str]) -> Optional[str]:
    try:
        from openai import OpenAI  # type: ignore
    except Exception:
        return None

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    client = OpenAI(api_key=api_key)
    model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
    )

    # Log token usage if available
    usage = getattr(response, "usage", None)
    if usage:
        usage_dict = {
            "prompt_tokens": getattr(usage, "prompt_tokens", None),
            "completion_tokens": getattr(usage, "completion_tokens", None),
            "total_tokens": getattr(usage, "total_tokens", None),
        }
        _print_token_usage(usage_dict)

    content = response.choices[0].message.content if response.choices else ""
    return content


def _try_gemini_chat(system_prompt: str, user_prompt: str, model: Optional[str]) -> Optional[str]:
    try:
        import google.generativeai as genai  # type: ignore
    except Exception:
        return None

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_GENERATIVE_AI_API_KEY")
    if not api_key:
        return None

    genai.configure(api_key=api_key)
    model_name = model or os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")

    # Gemini doesn't have roles in the same way; prepend system to user content
    prompt = f"System:\n{system_prompt}\n\nUser:\n{user_prompt}"

    gm = genai.GenerativeModel(model_name)
    response = gm.generate_content(prompt)

    # Log token usage if available
    usage_meta = getattr(response, "usage_metadata", None)
    if usage_meta:
        usage_dict = {
            "prompt_token_count": getattr(usage_meta, "prompt_token_count", None),
            "candidates_token_count": getattr(usage_meta, "candidates_token_count", None),
            "total_token_count": getattr(usage_meta, "total_token_count", None),
        }
        _print_token_usage(usage_dict)

    try:
        return response.text  # SDK provides aggregated text
    except Exception:
        return None


def chat_completion(system_prompt: str, user_prompt: str, *, provider: Optional[str] = None, model: Optional[str] = None) -> str:
    """
    Perform a chat completion with the configured provider and print token usage.

    Provider resolution order:
    - Explicit `provider` argument: "openai" or "gemini"
    - Env var `LLM_PROVIDER`
    - Auto: try OpenAI then Gemini
    """
    prov = (provider or os.getenv("LLM_PROVIDER") or "").lower()

    if prov == "openai":
        result = _try_openai_chat(system_prompt, user_prompt, model)
        if result is not None:
            return result
    elif prov == "gemini":
        result = _try_gemini_chat(system_prompt, user_prompt, model)
        if result is not None:
            return result

    # Auto-detect fallback
    result = _try_openai_chat(system_prompt, user_prompt, model)
    if result is not None:
        return result

    result = _try_gemini_chat(system_prompt, user_prompt, model)
    if result is not None:
        return result

    raise RuntimeError(
        "No supported LLM provider available. Install and configure OpenAI or Google Gemini SDK with API key."
    ) 