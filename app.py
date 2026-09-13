import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(page_title="Afufa AI", page_icon="🤖", layout="centered")

st.title("🤖 Afufa AI Assistant")
st.caption("Ask me anything, record audio, or upload images!")

# Initialize Gemini Client using Streamlit Secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# 1. Image Upload Section
uploaded_file = st.file_uploader("📸 / 🖼️ Upload image or camera capture", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

# 2. Voice Input Section
audio_value = st.audio_input("🎙️ Tap to speak")

if audio_value:
    st.audio(audio_value)
    st.info("Audio recorded successfully!")

# 3. Chat Interface & Live AI Responses
if prompt := st.chat_input("Ask Afufa anything..."):
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )
        st.write(response.text)
