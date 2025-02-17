import firebase_admin
from firebase_admin import credentials, firestore
import os

# Load Firebase credentials from a JSON file (Download from Firebase)
FIREBASE_CRED = "firebase_credentials.json"

if not os.path.exists(FIREBASE_CRED):
    raise Exception("Missing Firebase credentials file!")

# Initialize Firebase
cred = credentials.Certificate(FIREBASE_CRED)
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_chat(user_message, bot_response, user_id="guest"):
    """Save chat messages to Firebase Firestore"""
    doc_ref = db.collection("chats").document(user_id)
    
    # Get existing chat history
    chat_data = doc_ref.get().to_dict() or {"messages": []}
    
    # Append new message
    chat_data["messages"].append({
        "user": user_message,
        "bot": bot_response
    })
    
    # Save back to Firestore
    doc_ref.set(chat_data)

def get_chat_history(user_id="guest"):
    """Retrieve chat history from Firestore"""
    doc_ref = db.collection("chats").document(user_id)
    chat_data = doc_ref.get().to_dict()
    
    if chat_data and "messages" in chat_data:
        return chat_data["messages"]
    return []
