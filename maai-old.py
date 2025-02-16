from flask import Flask, request, render_template, jsonify
from openai import OpenAI

client = OpenAI(api_key="your_api_key")
import json

app = Flask(__name__)

# Replace with your OpenAI API Key

chat_history = []

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
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages."""
    global chat_history
    user_input = request.json.get("message", "")

    if not user_input:
        return jsonify({"error": "Empty input"}), 400

    bot_response = generate_response(user_input)

    # Save chat history (Optional)
    chat_history.append({"user": user_input, "bot": bot_response})
    with open("chat_history.json", "w") as f:
        json.dump(chat_history, f)

    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
