import sqlite3

DB_NAME = "chat_history.db"

def init_db():
    """Create the chat history table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_chat(user_message, bot_response):
    """Save chat message to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat (user_message, bot_response) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()
    conn.close()

def get_chat_history():
    """Retrieve the last 10 messages."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_response, timestamp FROM chat ORDER BY timestamp DESC LIMIT 10")
    history = cursor.fetchall()
    conn.close()
    return history

# Initialize the database
init_db()
