# llm.py
# ─────────────────────────────────────────────────────────────────────────────
# Handles all communication with the Groq API.
# No UI code lives here — this file only knows about Python and the API.
# ─────────────────────────────────────────────────────────────────────────────

import os
import time
from groq import Groq
from dotenv import load_dotenv
from config import PROMPTS, MODELS

load_dotenv()

# Initialise the Groq client once when the module is imported
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def build_messages(system_prompt: str, history: list, user_message: str) -> list:
    """
    Build the messages list to send to the Groq API.

    history format (Gradio 6+): list of {"role": "user"/"assistant", "content": "..."}

    Returns a list ready to pass to client.chat.completions.create()
    """
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})
    return messages


def get_response(
    user_message: str,
    history: list,
    mode: str,
    model_label: str,
    temperature: float,
) -> tuple[list, str]:
    """
    Send a message to the Groq API and return the updated history and stats string.

    Returns:
        history (list): Updated conversation history in Gradio 6 dict format.
        stats   (str):  Human-readable string showing tokens, speed, model used.
    """
    system_prompt = PROMPTS[mode]
    model_id      = MODELS[model_label]
    messages      = build_messages(system_prompt, history, user_message)

    start = time.time()
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=messages,
            temperature=temperature,
        )
        reply         = response.choices[0].message.content
        elapsed       = time.time() - start
        input_tokens  = response.usage.prompt_tokens
        output_tokens = response.usage.completion_tokens

        stats = (
            f"⏱ {elapsed:.2f}s  ·  "
            f"📥 {input_tokens} tokens in  ·  "
            f"📤 {output_tokens} tokens out  ·  "
            f"🌡 temp {temperature:.1f}  ·  "
            f"🤖 {model_label.split('(')[0].strip()}"
        )

    except Exception as e:
        if "429" in str(e):
            reply = "⚠️ Rate limit hit — wait a moment and try again."
        else:
            reply = f"⚠️ Error: {e}"
        stats = ""

    # Append both sides of the exchange to history
    history = history + [
        {"role": "user",      "content": user_message},
        {"role": "assistant", "content": reply},
    ]
    return history, stats