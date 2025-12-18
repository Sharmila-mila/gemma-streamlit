import streamlit as st
import requests

# 🔴 IMPORTANT: Replace with YOUR CURRENT ngrok URL
URL = "https://abcd-1234.ngrok-free.app/api/chat"
MODEL = "gemma:2b"

st.set_page_config(page_title="Offline Gemma Chatbot")

st.title("🤖 Offline AI Chatbot (Gemma + Ollama)")
st.write("Streamlit Cloud UI + Local Ollama via ngrok")

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
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

    # Ollama payload
    payload = {
        "model": MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": "You are a helpful AI tutor."},
            {"role": "user", "content": user_input}
        ]
    }

    # 🔑 REQUIRED HEADER FOR NGROK FREE VERSION
    headers = {
        "ngrok-skip-browser-warning": "true"
    }

    try:
        response = requests.post(
            URL,
            json=payload,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()

        reply = response.json()["message"]["content"]

    except Exception as e:
        reply = f"❌ Error connecting to Ollama: {e}"

    # Show AI response
    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
    with st.chat_message("assistant"):
        st.markdown(reply)

