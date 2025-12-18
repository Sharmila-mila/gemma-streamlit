import streamlit as st
import requests

URL = "http://localhost:11434/api/chat"
MODEL = "gemma:2b"

st.set_page_config(page_title="Offline Gemma Chatbot")

st.title("🤖 Offline AI Chatbot (Gemma + Ollama)")
st.write("Runs fully offline on your laptop")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Ask your question...")

if user_input:
    # Show user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to Ollama (IMPORTANT FIX HERE)
    payload = {
        "model": MODEL,
        "stream": False,   # ✅ FIX
        "messages": [
            {"role": "system", "content": "You are a helpful AI tutor."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status()

        reply = response.json()["message"]["content"]

    except Exception as e:
        reply = f"❌ Error: {e}"

    # Show AI reply
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    with st.chat_message("assistant"):
        st.markdown(reply) 
