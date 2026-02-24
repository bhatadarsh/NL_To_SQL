"""
gemini_client.py - Handles all communication with the Gemini API.
"""
import json
from groq import Groq 
from app.configuration.config import GROQ_API_KEY, GROQ_MODEL


def call_gemini(prompt: str) -> str:
    
    """Send a prompt to Groq and return the raw text response."""
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return response.choices[0].message.content.strip()



def call_gemini_for_json(prompt: str) -> dict:
    """
    Send a prompt expecting a JSON response.
    Strips any accidental markdown fencing and parses to dict.
    """
    raw = call_gemini(prompt)

    # Strip markdown code fences if present
    if raw.startswith("```"):
        lines = raw.splitlines()
        lines = [l for l in lines if not l.strip().startswith("```")]
        raw = "\n".join(lines)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Groq returned invalid JSON.\nRaw response:\n{raw}\n\nError: {e}")
    