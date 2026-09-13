import streamlit as st

st.title("Welcome to Afufa App!")
st.write("Your Streamlit app is up and running successfully.")
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Afufa AI", page_icon="🤖", layout="centered")

st.title("🤖 Afufa AI Assistant")
st.caption("Ask me anything, record audio, or upload images!")

# 1. Image & File Camera Input Section
uploaded_file = st.file_uploader("📷 / 🖼️ Upload image or camera capture", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

# 2. Voice Input Section
audio_value = st.audio_input("🎙️ Tap to speak")

if audio_value:
    st.audio(audio_value)
    st.info("Audio recorded successfully!")

# 3. Text & Chat Interface (Search/Chat Bar)
if prompt := st.chat_input("Ask Afufa anything..."):
    st.chat_message("user").write(prompt)
    # Simple simulated response for testing
    st.chat_message("assistant").write(f"I received your request: '{prompt}'. How else can I help?")
