import streamlit as st
from google import genai

# Page Configuration (Clean title, no emoji)
st.set_page_config(page_title="Afufa AI", layout="centered")

# Custom CSS for Green Theme and Rounded Search Bar
st.markdown("""
    <style>
    :root {
        --primary-color: #2e7d32;
        --background-color: #0e1117;
        --secondary-background-color: #1a1c24;
        --text-color: #ffffff;
    }
    
    /* Remove default red focus glow and add smooth green curves to the chat input */
    [data-testid="stChatInput"] textarea {
        border-radius: 24px !important;
        border: 1px solid #2e7d32 !important;
        background-color: #1a1c24 !important;
        color: #ffffff !important;
    }
    
    /* Ensure no red border/glow appears when clicked or focused */
    [data-testid="stChatInput"] textarea:focus {
        border: 2px solid #2e7d32 !important;
        box-shadow: 0 0 8px rgba(46, 125, 50, 0.4) !important;
    }
    
    /* Style buttons with a nice green accent */
    .stButton button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
    }
    .stButton button:hover {
        background-color: #1b5e20;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

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
        
        # Stream the actual response chunks cleanly onto the screen
        response_stream = client.models.generate_content_stream(
            model="gemini-3.6-flash",
            contents=forced_payload,
        )
        
        ai_reply = st.write_stream(response_stream)
        
        # Save assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
