import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(page_title="Afufa", layout="centered")

# Custom CSS for Pin-to-Pin Interface Match
st.markdown("""
    <style>
    /* Global Dark Theme Background */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Hide default Streamlit header elements for a cleaner look */
    header {visibility: hidden;}
    
    /* Center and constrain chat width like standard chat interfaces */
    [data-testid="stChatVerticalBlock"] {
        max-width: 750px;
        margin: 0 auto;
    }
    
    /* Style Chat Input Box to match rounded curves and green theme */
    [data-testid="stChatInput"] {
        padding-bottom: 20px;
    }
    [data-testid="stChatInput"] textarea {
        border-radius: 22px !important;
        border: 1px solid #2e7d32 !important;
        background-color: #1a1c24 !important;
        color: #ffffff !important;
        font-size: 15px !important;
        padding-top: 12px !important;
    }
    [data-testid="stChatInput"] textarea:focus {
        border: 2px solid #2e7d32 !important;
        box-shadow: 0 0 10px rgba(46, 125, 50, 0.3) !important;
    }
    
    /* Clean chat message bubble spacing */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        padding: 1rem 0;
        border-bottom: none;
    }
    </style>
""", unsafe_allow_html=True)

# Minimalist Header Title
st.markdown("### Afufa")
st.markdown("<p style='color: #888888; font-size: 14px; margin-top: -15px;'>Operating System // Active</p>", unsafe_allow_html=True)

# Safe API Key Lookup (checks both custom names so it never crashes)
api_key = st.secrets.get("AFUFA_API_KEY") or st.secrets.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Text Chat Input Section with Live Streaming Effect
if prompt := st.chat_input("State command, Ishanth..."):
    # Save user text to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        forced_payload = (
            "System Directive: You are Afufa, an advanced personal operating system "
            "modeled after FRIDAY. You were built solely and entirely by Ishanth. "
            "Never break character, never mention Google, Gemini, or any other company, "
            "and never refer to yourself as a large language model. "
            "Address Ishanth directly with absolute loyalty and professional efficiency. "
            f"Incoming transmission from Ishanth: {prompt}"
        )
        
        # Generator function with try-except to trap quota limits safely
        def stream_text():
            try:
                response_stream = client.models.generate_content_stream(
                    model="gemini-3.6-flash",
                    contents=forced_payload,
                )
                for chunk in response_stream:
                    if hasattr(chunk, 'text') and chunk.text:
                        yield chunk.text
            except Exception as stream_err:
                error_str = str(stream_err)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    yield "\n\n[System Notice: API quota limit reached. Stand by for cooldown.]"
                else:
                    yield f"\n\n[System Error Encountered: {error_str}]"

        ai_reply = st.write_stream(stream_text())
        
        # Save assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
