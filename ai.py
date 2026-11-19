"""All Gemini (AI) calls live here. Other files just call ask()."""
import os
import re
import json
import time
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# You can change the model name in .env with GEMINI_MODEL=...
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

# If the main model is busy or missing, the app tries these backups.
FALLBACK_MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.6-flash"]
MODELS_TO_TRY = [MODEL] + [m for m in FALLBACK_MODELS if m != MODEL]

TRIES_PER_MODEL = 3   # how many times to try one model when it is busy
WAIT_SECONDS = 2      # first wait; it grows each time (2s, 4s, ...)

SAFETY = (
    "You are a friendly assistant inside an educational college demo app. "
    "Use very simple language. Do NOT diagnose any disease and do NOT prescribe "
    "medicine or doses. You give general information only and you remind the "
    "user to talk to a doctor or dietitian for personal advice. "
)


def _key():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        try:
            key = st.secrets["GEMINI_API_KEY"]  # used when the app is online
        except Exception:
            key = None
    return key


def _is_busy(msg, low):
    """True when Google says the server is busy (a short, temporary problem)."""
    return ("503" in msg or "unavailable" in low
            or "high demand" in low or "overloaded" in low)


def ask(prompt, image=None, mime="image/jpeg", json_mode=False):
    """Return (text, error). Exactly one of them is None."""
    key = _key()
    if not key:
        return None, ("No GEMINI_API_KEY found. Put it in your .env file "
                      "(or in Streamlit Secrets when the app is online).")
    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)
        contents = [prompt]
        if image is not None:
            contents = [types.Part.from_bytes(data=image, mime_type=mime), prompt]
        config = None
        if json_mode:
            config = types.GenerateContentConfig(response_mime_type="application/json")
    except Exception as e:
        return None, f"AI error: {str(e)[:250]}"

    last_error = "AI error: unknown problem. Please try again."

    for model in MODELS_TO_TRY:
        for attempt in range(TRIES_PER_MODEL):
            try:
                resp = client.models.generate_content(
                    model=model, contents=contents, config=config)
                text = (resp.text or "").strip()
                if not text:
                    return None, "The AI sent an empty answer. Please try again."
                return text, None
            except Exception as e:
                msg = str(e)
                low = msg.lower()

                if "429" in msg or "quota" in low or "exhausted" in low:
                    return None, "Free usage limit reached. Wait one minute and try again."
                if "api key" in low or "401" in msg or "403" in msg:
                    return None, "Your Gemini API key was rejected. Check the key in .env."
                if "404" in msg:
                    last_error = (f"Model '{MODEL}' was not found. Set GEMINI_MODEL in .env "
                                  "to a model listed in Google AI Studio.")
                    break  # this model does not exist, go to the next backup
                if _is_busy(msg, low):
                    last_error = ("Google's AI is very busy right now. "
                                  "Please wait a minute and try again.")
                    if attempt < TRIES_PER_MODEL - 1:
                        time.sleep(WAIT_SECONDS * (attempt + 1))
                    continue  # try the same model again
                return None, f"AI error: {msg[:250]}"

    return None, last_error


def parse_json(text):
    """Turn the AI's answer into a Python dict. Returns None if it fails."""
    if not text:
        return None
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    try:
        return json.loads(text)
    except Exception:
        return None
