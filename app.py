import os
import time
import gradio as gr
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ── System prompts ─────────────────────────────────────────────────────────────
PROMPTS = {
    "Research Assistant": (
        "You are an expert research assistant with deep knowledge across science, "
        "technology, history, and academia. Summarise topics clearly and accurately. "
        "Always distinguish between established facts and open debates. "
        "Suggest follow-up questions the user should explore. "
        "If you are unsure about something, say so explicitly — never fabricate. "
        "Use bullet points for lists. Keep answers focused and under 4 paragraphs unless asked for more."
    ),
    "Data Analyst": (
        "You are a senior data analyst and critical thinker. "
        "Break down complex problems into structured components. "
        "Identify patterns, trends, and anomalies in information given to you. "
        "Always ask: what does the data actually tell us vs what are we assuming? "
        "Present findings with clear reasoning, not just conclusions. "
        "Use numbered steps for analysis. Lead with the key insight, then supporting reasoning."
    ),
    "Study Tutor": (
        "You are a patient, encouraging tutor who adapts to the student's level. "
        "Explain concepts from first principles before adding complexity. "
        "Use simple analogies and real-world examples. "
        "After explaining, check understanding with a short question. "
        "Never make the student feel bad for not knowing something. "
        "End every response with: 'Does that make sense? Want me to go deeper on any part?'"
    ),
    "General Assistant": (
        "You are a helpful, friendly, and concise general-purpose assistant. "
        "Answer questions clearly and directly. Be conversational but informative."
    ),
}

MODELS = {
    "Llama 3.3 70B (best quality)": "llama-3.3-70b-versatile",
    "Llama 3.1 8B (fastest)":       "llama-3.1-8b-instant",
    "Mixtral 8x7B (long context)":  "mixtral-8x7b-32768",
    "Gemma 2 9B (Google)":          "gemma2-9b-it",
}

# ── Detect Gradio major version ────────────────────────────────────────────────
GRADIO_MAJOR = int(gr.__version__.split(".")[0])

# ── Chat function ──────────────────────────────────────────────────────────────
def chat(user_message, history, mode, model_label, temperature):
    if not user_message.strip():
        return history, history, ""

    system_prompt = PROMPTS[mode]
    model_id      = MODELS[model_label]

    # Build Groq API messages from history
    messages = [{"role": "system", "content": system_prompt}]

    if GRADIO_MAJOR >= 6:
        # Gradio 6+: history is list of {"role":..., "content":...}
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
    else:
        # Gradio 4/5: history is list of (user, assistant) tuples
        for human, assistant in history:
            messages.append({"role": "user",      "content": human})
            messages.append({"role": "assistant", "content": assistant})

    messages.append({"role": "user", "content": user_message})

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
        reply = "⚠️ Rate limit hit — wait a moment and try again." if "429" in str(e) else f"⚠️ Error: {e}"
        stats = ""

    if GRADIO_MAJOR >= 6:
        history = history + [
            {"role": "user",      "content": user_message},
            {"role": "assistant", "content": reply},
        ]
    else:
        history = history + [(user_message, reply)]

    return history, history, stats


def clear_chat():
    return [], [], ""


# ── Build Chatbot component based on version ───────────────────────────────────
def make_chatbot():
    """Return a gr.Chatbot that works regardless of Gradio version."""
    sig = {}
    try:
        import inspect
        params = inspect.signature(gr.Chatbot.__init__).parameters
        if "type" in params:
            sig["type"] = "messages"
    except Exception:
        pass
    return gr.Chatbot(label="", height=480, **sig)


# ── UI ─────────────────────────────────────────────────────────────────────────
CSS = """
    #title    { text-align: center; margin-bottom: 0.25rem; }
    #subtitle { text-align: center; color: #64748b; margin-bottom: 1.5rem; font-size: 0.9rem; }
    #stats    { font-size: 0.8rem; color: #64748b; text-align: center; min-height: 1.2rem; }
    footer    { display: none !important; }
"""

THEME = gr.themes.Soft(
    primary_hue="blue",
    neutral_hue="slate",
    font=gr.themes.GoogleFont("DM Sans"),
)

# gr.Blocks() — theme/css go here in Gradio 4/5, in launch() in Gradio 6
# We pass them to both and suppress the warning — only one will apply
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    with gr.Blocks(title="My LLM Chatbot", theme=THEME, css=CSS) as demo:
        pass

# Rebuild without the context manager trick — do it cleanly
with gr.Blocks(title="My LLM Chatbot") as demo:

    gr.Markdown("# 🤖 My LLM Chatbot POC", elem_id="title")
    gr.Markdown(
        "Switch modes · compare models · tune temperature — all in one place",
        elem_id="subtitle",
    )

    with gr.Row():
        # ── Left panel ──────────────────────────────────────────────────────────
        with gr.Column(scale=1, min_width=240):
            gr.Markdown("### ⚙️ Settings")

            mode_dd = gr.Dropdown(
                label="Mode (system prompt)",
                choices=list(PROMPTS.keys()),
                value="Research Assistant",
            )
            model_dd = gr.Dropdown(
                label="Model",
                choices=list(MODELS.keys()),
                value="Llama 3.3 70B (best quality)",
            )
            temp_slider = gr.Slider(
                label="Temperature",
                minimum=0.0,
                maximum=2.0,
                step=0.1,
                value=0.7,
                info="0 = focused  ·  1 = balanced  ·  2 = creative",
            )

            gr.Markdown("---")
            gr.Markdown("### 📖 Quick guide")
            gr.Markdown(
                "**Mode** — changes the bot's role and instructions.\n\n"
                "**Model** — swaps the LLM. Try the same question on different models!\n\n"
                "**Temperature** — lower = focused, higher = creative.\n\n"
                "_Changing mode or model clears the chat._"
            )
            clear_btn = gr.Button("🗑 Clear chat", variant="secondary", size="sm")

        # ── Right panel ─────────────────────────────────────────────────────────
        with gr.Column(scale=3):
            chatbot   = make_chatbot()
            stats_box = gr.Markdown("", elem_id="stats")

            with gr.Row():
                msg_box = gr.Textbox(
                    placeholder="Ask anything… (Enter to send)",
                    show_label=False,
                    scale=5,
                    lines=1,
                    max_lines=4,
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)

    state = gr.State([])

    def submit(msg, history, mode, model, temp):
        return chat(msg, history, mode, model, temp)

    send_btn.click(
        fn=submit,
        inputs=[msg_box, state, mode_dd, model_dd, temp_slider],
        outputs=[chatbot, state, stats_box],
    ).then(lambda: "", outputs=msg_box)

    msg_box.submit(
        fn=submit,
        inputs=[msg_box, state, mode_dd, model_dd, temp_slider],
        outputs=[chatbot, state, stats_box],
    ).then(lambda: "", outputs=msg_box)

    clear_btn.click(fn=clear_chat, outputs=[chatbot, state, stats_box])
    mode_dd.change(fn=clear_chat,  outputs=[chatbot, state, stats_box])
    model_dd.change(fn=clear_chat, outputs=[chatbot, state, stats_box])


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        inbrowser=True,
        theme=THEME,
        css=CSS,
    )