import React, { useState, useEffect } from "react";
import { View, TextInput, Button, ScrollView, Text, StyleSheet } from "react-native";
import { io } from "socket.io-client";
import { collection, addDoc, getDocs, query, orderBy } from "firebase/firestore";
import { db } from "./firebaseConfig";

const socket = io("https://your-maai-server.com"); 

export default function App() {
    const [messages, setMessages] = useState<{ user: string; bot: string }[]>([]);
    const [userInput, setUserInput] = useState("");

    useEffect(() => {
        socket.on("receive_message", async (data) => {
            setMessages((prevMessages) => [...prevMessages, { user: data.user, bot: data.bot }]);
            await addDoc(collection(db, "chats"), { user: data.user, bot: data.bot, timestamp: new Date() });
        });

        return () => {
            socket.off("receive_message");
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
            <Button title="Send" onPress={sendMessage} />
        </View>
    );
}

const styles = StyleSheet.create({
    container: { flex: 1, padding: 20, backgroundColor: "#f4f4f4" },
    chatBox: { flex: 1, marginBottom: 10 },
    input: { borderWidth: 1, borderColor: "#ccc", padding: 10, marginBottom: 10 },
    userMessage: { fontWeight: "bold", textAlign: "right", marginVertical: 5 },
    botMessage: { fontStyle: "italic", marginVertical: 5 }
});
