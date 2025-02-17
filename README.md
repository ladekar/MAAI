# MAAI
The non-profit & exploratory project to evolve AI and teach the AI to RRP Robotics team. It's for helping students, and learners around the world to learn & adopt AI. 
© 2025 MAAI@RRP Robotics Team. All rights reserved.
This software is licensed under the MIT License.
For more details, see LICENSE file or visit https://opensource.org/licenses/MIT.
Features of Maai:
Runs a Flask web server
Accepts user input via a simple web form
Generates AI responses using OpenAI's GPT API (or a placeholder if you don’t have an API key)
Code for maai.py (Flask App)
Save this as maai.py and run it using python maai.py.

python
Copy
Edit
from flask import Flask, request, render_template
import openai  # Install with: pip install openai

app = Flask(__name__)

# Replace with your OpenAI API Key
openai.api_key = "your_openai_api_key"

def generate_response(user_input):
    """Generate AI response using OpenAI's GPT model."""
    try:
        response = openai.ChatCompletion.create(
#           model="gpt-4o",
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form["user_input"]
        bot_response = generate_response(user_input)
        return render_template("index.html", user_input=user_input, bot_response=bot_response)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
HTML Frontend (templates/index.html)
Create a folder named templates and inside it, save this as index.html:

html
Copy
Edit
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Maai - AI Assistant</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            margin: 50px;
        }
        input, button {
            padding: 10px;
            font-size: 16px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>Welcome to Maai - Your AI Assistant</h1>
    <form method="post">
        <input type="text" name="user_input" placeholder="Ask me anything..." required>
        <button type="submit">Ask</button>
    </form>
    {% if user_input %}
        <p><strong>You:</strong> {{ user_input }}</p>
        <p><strong>Maai:</strong> {{ bot_response }}</p>
    {% endif %}
</body>
</html>
How to Run the Maai App
Install dependencies:
sh
Copy
Edit
pip install flask openai
Run the app:
sh
Copy
Edit
python maai.py
#Open http://127.0.0.1:5000/ in your browser and start chatting with Maai! 🚀
Open https://maai.io in your browser and start chatting with Maai! 🚀

