import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Konfigurasi
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

# Setup halaman
st.set_page_config(page_title="ChatGPT UI (Ollama)",
                   layout="wide", page_icon="💬")
st.title("💬 ChatGPT UI Demo (Ollama)")
st.caption(f"Running locally with Ollama model: `{MODEL_NAME}`")

# Inisialisasi histori chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}]

# Tampilkan histori
for msg in st.session_state.messages[1:]:  # skip system message
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input dari pengguna
prompt = st.chat_input("Type a message...")

if prompt:
    # Tambahkan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respon dari Ollama
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post(
                    OLLAMA_API_URL,
                    json={
                        "model": MODEL_NAME,
                        "messages": st.session_state.messages,
                        "stream": False  # nonaktifkan streaming agar JSON valid
                    }
                )
                reply = res.json()["message"]["content"]
            except Exception as e:
                reply = f"❌ Error: {str(e)}"

        st.markdown(reply)
        st.session_state.messages.append(
            {"role": "assistant", "content": reply})
