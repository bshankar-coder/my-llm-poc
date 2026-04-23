# My LLM POC Chatbot

A simple chatbot application that uses the Groq API to provide conversational AI responses.

## Prerequisites

- Python 3.7 or higher
- A Groq API key (get one from [Groq Console](https://console.groq.com/))

## Setup

1. **Clone or download the project** to your local machine.

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install groq python-dotenv
   ```

5. **Set up your API key**:
   - Create a `.env` file in the project root (if it doesn't exist)
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_api_key_here
     ```
   - Replace `your_api_key_here` with your actual API key from Groq.

## Running the Chatbot

1. Ensure your virtual environment is activated (if using one).

2. Run the chatbot:
   ```bash
   python chatbot.py
   ```

3. Start chatting! Type your messages and press Enter. The bot will respond with helpful answers.

4. To exit, type `quit` and press Enter.

## Features

- Conversational AI using Groq's Llama model
- Maintains conversation history
- Simple command-line interface
- Configurable system prompt

## Troubleshooting

- **API Key Issues**: Make sure your `.env` file is in the project root and contains the correct API key.
- **Import Errors**: Ensure all dependencies are installed with `pip install groq python-dotenv`.
- **Python Version**: Make sure you're using Python 3.7+.