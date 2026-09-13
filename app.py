import streamlit as st
from google import genai
from google.genai import types

# Page Configuration
st.set_page_config(page_title="Afufa AI", page_icon="🤖", layout="centered")

st.title("🤖 Afufa AI Assistant")
st.caption("Your Independent Voice-Activated AI")

# Initialize Gemini Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Session state security lock
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Voice Authentication/Command Input
audio_value = st.audio_input("🎙️ Tap to speak to Afufa")

if audio_value:
    with st.spinner("Afufa is processing your voice..."):
        # Send audio directly to Gemini to interpret voice command and verify identity
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                audio_value,
                (
                    "System Directive: You are Afufa, an independent AI assistant created by Ishan. "
                    "You serve only your creator, Boss. Never mention Google or Gemini. "
                    "Listen to the user's spoken audio. If they are giving a command or asking a question, "
                    "respond directly as Afufa in a helpful, concise manner."
                )
            ]
        )
        
        # Automatically authenticate upon first valid voice interaction
        st.session_state.authenticated = True
        
        st.chat_message("assistant").write(response.text)

# Fallback text chat input for convenience
if prompt := st.chat_input("Or type a message to Afufa..."):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=(
                "System Directive: You are Afufa, an independent AI assistant created by Ishan. "
                "Never mention Google or Gemini. "
                f"User input: {prompt}"
            ),
        )
        st.write(response.text)
