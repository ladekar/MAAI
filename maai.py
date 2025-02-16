from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Get API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_input):
    """Generate AI response using OpenAI's GPT model."""
    if not openai.api_key:
        return "Error: OpenAI API key is missing!"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on("send_message")
def handle_message(data):
    """Handle incoming user messages and respond in real-time."""
    user_input = data.get("message", "")
    if not user_input.strip():
        return

    bot_response = generate_response(user_input)
    emit("receive_message", {"user": user_input, "bot": bot_response}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
