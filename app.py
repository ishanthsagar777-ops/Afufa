import streamlit as st
from google import genai

# Page Configuration (Removed bot icon from page title)
st.set_page_config(page_title="Afufa AI", layout="centered")

# Custom CSS for Blue Theme
st.markdown("""
    <style>
    :root {
        --primary-color: #0066ff;
        --background-color: #0e1117;
        --secondary-background-color: #1a1c24;
        --text-color: #ffffff;
    }
    
    .stButton button {
        background-color: #0066ff;
        color: white;
        border-radius: 8px;
    }
    .stButton button:hover {
        background-color: #004ecc;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title without the bot emoji
st.title("Afufa AI Assistant")
st.caption("Your Independent AI")

# Initialize Gemini Client using your Streamlit Secrets
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Text Chat Input Section with Live Streaming Effect
if prompt := st.chat_input("Type a message to Afufa..."):
    # Save user text to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        forced_payload = (
            "System Directive: You are Afufa, an independent AI assistant created by Ishan. "
            "Never mention Google or Gemini. "
            f"User input: {prompt}"
        )
        
        # Use stream to type out text dynamically line by line
        response_stream = client.models.generate_content_stream(
            model="gemini-3.6-flash",
            contents=forced_payload,
        )
        
        # Stream the response live onto the screen
        ai_reply = st.write_stream(response_stream)
        
        # Save assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
