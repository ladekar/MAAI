import React, { useState, useEffect } from "react";
import { View, TextInput, Button, ScrollView, Text, StyleSheet, TouchableOpacity } from "react-native";
import { io } from "socket.io-client";
import Voice from "@react-native-voice/voice";
import { collection, addDoc, getDocs, query, orderBy } from "firebase/firestore";
import { db } from "./firebaseConfig";

// Connect to WebSocket server (Replace with your deployed URL)
const socket = io("https://your-maai-server.com");

export default function App() {
    const [messages, setMessages] = useState([]);
    const [userInput, setUserInput] = useState("");
    const [isListening, setIsListening] = useState(false);

    useEffect(() => {
        // Speech recognition listener
        Voice.onSpeechResults = (event) => {
            setUserInput(event.value ? event.value[0] : "");
        };

        // WebSocket listener for incoming messages
        socket.on("receive_message", async (data) => {
            setMessages((prevMessages) => [...prevMessages, { user: data.user, bot: data.bot }]);
            await addDoc(collection(db, "chats"), { user: data.user, bot: data.bot, timestamp: new Date() });
        });

        return () => {
            socket.off("receive_message");
            Voice.destroy().then(Voice.removeAllListeners);
        };
    }, []);

    useEffect(() => {
        const fetchMessages = async () => {
            const q = query(collection(db, "chats"), orderBy("timestamp", "asc"));
            const querySnapshot = await getDocs(q);
            const chatHistory = querySnapshot.docs.map(doc => doc.data());
            setMessages(chatHistory);
        };

        fetchMessages();
    }, []);

    const sendMessage = () => {
        if (userInput.trim()) {
            socket.emit("send_message", { message: userInput });
            setMessages((prevMessages) => [...prevMessages, { user: userInput, bot: "..." }]);
            setUserInput("");
        }
    };

    const startListening = async () => {
        setIsListening(true);
        try {
            await Voice.start("en-US");
        } catch (error) {
            console.error(error);
        }
    };

    const stopListening = async () => {
        setIsListening(false);
        try {
            await Voice.stop();
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <View style={styles.container}>
            <ScrollView style={styles.chatBox}>
                {messages.map((msg, index) => (
                    <View key={index}>
                        <Text style={styles.userMessage}>You: {msg.user}</Text>
                        <Text style={styles.botMessage}>Maai: {msg.bot}</Text>
                    </View>
                ))}
            </ScrollView>

            <TextInput
                style={styles.input}
                placeholder="Ask Maai something..."
                value={userInput}
                onChangeText={setUserInput}
            />
            <View style={styles.buttonContainer}>
                <Button title="Send" onPress={sendMessage} />
                <TouchableOpacity style={styles.micButton} onPress={isListening ? stopListening : startListening}>
                    <Text style={styles.micText}>{isListening ? "🛑 Stop" : "🎤 Speak"}</Text>
                </TouchableOpacity>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20, backgroundColor: "#f4f4f4" },
    chatBox: { flex: 1, marginBottom: 10 },
    input: { borderWidth: 1, borderColor: "#ccc", padding: 10, marginBottom: 10 },
    buttonContainer: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
    micButton: { padding: 10, backgroundColor: "blue", borderRadius: 5 },
    micText: { color: "white", fontWeight: "bold" },
    userMessage: { fontWeight: "bold", textAlign: "right", marginVertical: 5 },
    botMessage: { fontStyle: "italic", marginVertical: 5 }
});
