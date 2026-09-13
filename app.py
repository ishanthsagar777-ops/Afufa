import streamlit as st
from google import genai
import os

# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="Afufa AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Afufa AI")
st.caption("Your personal AI assistant")

# -----------------------------
# GET API KEY
# -----------------------------

api_key = os.getenv("GEMINI_API_KEY")

# Streamlit Secrets fallback
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    st.error("❌ GEMINI_API_KEY is not configured.")
    st.info(
        "Add GEMINI_API_KEY to your Streamlit Secrets or environment variables."
    )
    st.stop()

# -----------------------------
# GEMINI CLIENT
# -----------------------------

try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error("❌ Could not connect to Gemini.")
    st.code(str(e))
    st.stop()

# -----------------------------
# CHAT MEMORY
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# DISPLAY OLD MESSAGES
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# USER INPUT
# -----------------------------

prompt = st.chat_input("Ask Afufa anything...")

if prompt:

    # Show user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation for Gemini
    conversation = ""

    for message in st.session_state.messages:
        if message["role"] == "user":
            conversation += f"User: {message['content']}\n"
        else:
            conversation += f"Afufa AI: {message['content']}\n"

    # -----------------------------
    # GEMINI REQUEST
    # -----------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=conversation
                )

                answer = response.text

                if not answer:
                    answer = "Sorry, I couldn't generate a response."

                st.markdown(answer)

                # Save AI response
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                st.error("❌ Gemini API Error")
                st.code(str(e))

# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.header("⚙️ Afufa AI")

    st.write(
        "Powered by Google Gemini"
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption(
        "Afufa AI • Streamlit"
    )
requirements.txt
Make sure your requirements.txt contains:
streamlit
google-genai
You can also pin a recent version if you want reproducible deployments:
streamlit>=1.40.0
google-genai>=1.0.0
Google's current examples use:
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)
