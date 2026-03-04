"""
LLM utility - calls HuggingFace Inference API.
Fixed with correct working endpoints for 2025.
"""
import os
import json
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

HF_TOKEN = os.getenv("HF_TOKEN", "")
MODEL = os.getenv("HF_MODEL", "google/flan-t5-large")


def hf_generate(prompt: str, max_new_tokens: int = 800) -> str:
    if not HF_TOKEN:
        return '[DEV MODE - set HF_TOKEN in .env]'

    # ── Method 1: HuggingFace Serverless Inference API (most reliable, free) ──
    api_url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": 0.7,
            "top_p": 0.95,
            "return_full_text": False,
            "do_sample": True
        }
    }

    try:
        r = requests.post(api_url, headers=headers, json=payload, timeout=120)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data and "generated_text" in data[0]:
                return data[0]["generated_text"]
            if isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"]
    except Exception:
        pass

    # ── Method 2: HuggingFace Inference Providers (newer API) ──
    try:
        api_url2 = f"https://api-inference.huggingface.co/v1/chat/completions"
        payload2 = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_new_tokens,
            "temperature": 0.7
        }
        r2 = requests.post(api_url2, headers=headers, json=payload2, timeout=120)
        if r2.status_code == 200:
            data2 = r2.json()
            if "choices" in data2:
                return data2["choices"][0]["message"]["content"]
    except Exception:
        pass

    # ── Method 3: Featherless router (correct path) ──
    try:
        api_url3 = "https://router.huggingface.co/featherless-ai/v1/chat/completions"
        payload3 = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_new_tokens,
            "temperature": 0.7
        }
        r3 = requests.post(api_url3, headers=headers, json=payload3, timeout=120)
        if r3.status_code == 200:
            data3 = r3.json()
            if "choices" in data3:
                return data3["choices"][0]["message"]["content"]
    except Exception:
        pass

    r.raise_for_status()
    return str(r.json())


def generate_text(prompt: str, max_new_tokens: int = 1000) -> str:
    return hf_generate(prompt, max_new_tokens)
