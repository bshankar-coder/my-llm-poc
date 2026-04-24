import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

conversation_history = []

prompts = {
    "research": "You are a research assistant...",
    "analyst":  "You are a data analyst...",
    "tutor":    "You are a patient tutor..."
}

print("Choose a mode: research / analyst / tutor")
mode = input("Mode: ").strip().lower()

system_prompt = prompts.get(mode, prompts["research"])

print("Chatbot ready! Type 'quit' to exit.")
print("-" * 40)

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt}
        ] + conversation_history
    )

    reply = response.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    print(f"Bot: {reply}")
    print("-" * 40)