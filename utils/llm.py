import os
import requests

PROVIDER = os.getenv("PROVIDER", "none").lower()

def _openai_chat(messages, model=None, temperature=0.3):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {"model": model, "messages": messages, "temperature": temperature}
    r = requests.post(url, headers=headers, json=body, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def maybe_generate_cover_letter(prompt: str) -> str:
    """If PROVIDER=openai and key present, use LLM. Otherwise return empty string."""
    if PROVIDER == "openai" and os.getenv("OPENAI_API_KEY"):
        system = {"role": "system", "content": "You are an expert career coach and persuasive copywriter."}
        user = {"role": "user", "content": prompt}
        return _openai_chat([system, user], temperature=0.5)
    return ""
