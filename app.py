# app.py
# ─────────────────────────────────────────────────────────────────────────────
# Entry point — run this file to start the chatbot.
#
#   python app.py
#
# Then open http://localhost:7860 in your browser.
# ─────────────────────────────────────────────────────────────────────────────

from ui import build_demo, THEME, CSS
from config import SERVER_HOST, SERVER_PORT

if __name__ == "__main__":
    demo = build_demo()
    demo.launch(
        server_name=SERVER_HOST,
        server_port=SERVER_PORT,
        share=False,
        inbrowser=True,
        theme=THEME,
        css=CSS,
    )