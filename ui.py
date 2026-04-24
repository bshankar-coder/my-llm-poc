# ui.py
# ─────────────────────────────────────────────────────────────────────────────
# Builds the Gradio UI and wires up all events.
# No API calls or business logic live here — it only calls functions from llm.py.
# ─────────────────────────────────────────────────────────────────────────────

import inspect
import gradio as gr
from config import (
    PROMPTS, MODELS,
    DEFAULT_MODE, DEFAULT_MODEL,
    TEMPERATURE_DEFAULT, TEMPERATURE_MIN, TEMPERATURE_MAX, TEMPERATURE_STEP,
)
from llm import get_response

# ── Theme & styles ─────────────────────────────────────────────────────────────
THEME = gr.themes.Soft(
    primary_hue="blue",
    neutral_hue="slate",
    font=gr.themes.GoogleFont("DM Sans"),
)

CSS = """
    #title    { text-align: center; margin-bottom: 0.25rem; }
    #subtitle { text-align: center; color: #64748b; margin-bottom: 1.5rem; font-size: 0.9rem; }
    #stats    { font-size: 0.8rem; color: #64748b; text-align: center; min-height: 1.2rem; }
    footer    { display: none !important; }
"""


# ── Helpers ────────────────────────────────────────────────────────────────────
def make_chatbot() -> gr.Chatbot:
    """
    Create a gr.Chatbot that works across Gradio versions.
    Gradio 6+ requires type='messages'; older versions don't accept it.
    We inspect the signature at runtime to decide.
    """
    kwargs = {"label": "", "height": 480}
    params = inspect.signature(gr.Chatbot.__init__).parameters
    if "type" in params:
        kwargs["type"] = "messages"
    return gr.Chatbot(**kwargs)


def submit(user_message, history, mode, model_label, temperature):
    """Called when the user sends a message."""
    if not user_message.strip():
        return history, history, ""
    history, stats = get_response(user_message, history, mode, model_label, temperature)
    return history, history, stats


def clear_chat():
    """Reset all chat state."""
    return [], [], ""


# ── Layout ─────────────────────────────────────────────────────────────────────
def build_demo() -> gr.Blocks:
    """
    Construct and return the full Gradio Blocks demo.
    Called once from app.py.
    """
    with gr.Blocks(title="My LLM Chatbot") as demo:

        # Header
        gr.Markdown("# 🤖 My LLM Chatbot POC", elem_id="title")
        gr.Markdown(
            "Switch modes · compare models · tune temperature — all in one place",
            elem_id="subtitle",
        )

        with gr.Row():

            # ── Left column: settings ──────────────────────────────────────────
            with gr.Column(scale=1, min_width=240):
                gr.Markdown("### ⚙️ Settings")

                mode_dd = gr.Dropdown(
                    label="Mode (system prompt)",
                    choices=list(PROMPTS.keys()),
                    value=DEFAULT_MODE,
                )
                model_dd = gr.Dropdown(
                    label="Model",
                    choices=list(MODELS.keys()),
                    value=DEFAULT_MODEL,
                )
                temp_slider = gr.Slider(
                    label="Temperature",
                    minimum=TEMPERATURE_MIN,
                    maximum=TEMPERATURE_MAX,
                    step=TEMPERATURE_STEP,
                    value=TEMPERATURE_DEFAULT,
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

            # ── Right column: chat ─────────────────────────────────────────────
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

        # Shared state — stores conversation history between messages
        state = gr.State([])

        # ── Event wiring ───────────────────────────────────────────────────────
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

        # Auto-clear chat when mode or model changes so context stays clean
        mode_dd.change(fn=clear_chat,  outputs=[chatbot, state, stats_box])
        model_dd.change(fn=clear_chat, outputs=[chatbot, state, stats_box])

    return demo