from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from openai import OpenAI

client = OpenAI(api_key="your_api_key")

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSocket support

# Replace with your OpenAI API Key

def generate_response(user_input):
    """Generate AI response using OpenAI's GPT model."""
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}])
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index-old.html")

@socketio.on("send_message")
def handle_message(data):
    """Handle incoming user messages and respond in real-time."""
    user_input = data.get("message", "")
    if not user_input.strip():
        return

    bot_response = generate_response(user_input)

    # Emit messages back to the frontend
    emit("receive_message", {"user": user_input, "bot": bot_response}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)
