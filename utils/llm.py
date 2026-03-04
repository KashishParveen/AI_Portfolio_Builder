"""
LLM utility - Groq API (free & fast)
"""
import os
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL = "llama3-8b-8192"


def groq_generate(prompt: str, max_new_tokens: int = 1000) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not set. Add it in Space Settings > Secrets.")

    # Truncate prompt if too long
    if len(prompt) > 6000:
        prompt = prompt[:6000]

    # Cap response tokens safely
    safe_tokens = min(max_new_tokens, 1500)

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": safe_tokens,
        "temperature": 0.7
    }

    r = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=60
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]


def generate_text(prompt: str, max_new_tokens: int = 1000) -> str:
    return groq_generate(prompt, max_new_tokens)