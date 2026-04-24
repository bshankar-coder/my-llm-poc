# My LLM POC Chatbot

A simple chatbot application that uses the Groq API to provide conversational AI responses. Features both a command-line interface and a modern web UI built with Gradio.

## Prerequisites

- Python 3.7 or higher
- A Groq API key (get one from [Groq Console](https://console.groq.com/))

## Project Structure

- `app.py`: Main entry point for the web UI application
- `ui.py`: Gradio-based user interface components and event handling
- `llm.py`: Handles communication with the Groq API
- `config.py`: Configuration settings, model definitions, and system prompts
- `chatbot.py`: Command-line interface version of the chatbot

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
   pip install groq python-dotenv gradio
   ```

5. **Set up your API key**:
   - Create a `.env` file in the project root (if it doesn't exist)
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_api_key_here
     ```
   - Replace `your_api_key_here` with your actual API key from Groq.

## Running the Chatbot

### Web UI (Recommended)

1. Ensure your virtual environment is activated (if using one).

2. Run the web application:
   ```bash
   python app.py
   ```

3. Open your browser and navigate to `http://localhost:7860`

### Command-Line Interface

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