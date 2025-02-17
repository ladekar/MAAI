from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import openai
import os
from dotenv import load_dotenv
from database import save_chat, get_chat_history

# Load environment variables
load_dotenv()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(user_input):
    """Generate AI response using OpenAI's GPT model."""
    if not openai.api_key:
        return "Error: OpenAI API key is missing!"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def home():
    """Render chat UI with chat history."""
    user_id = request.args.get("user", "guest")
    history = get_chat_history(user_id)
    return render_template("index-firebase.html", history=history, user_id=user_id)

@socketio.on("send_message")
def handle_message(data):
    """Handle chat messages and sync with Firebase."""
    user_input = data.get("message", "")
    user_id = data.get("user_id", "guest")

    if not user_input.strip():
        return

    bot_response = generate_response(user_input)

    # Save chat to Firebase
    save_chat(user_input, bot_response, user_id)

    emit("receive_message", {"user": user_input, "bot": bot_response, "user_id": user_id}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
