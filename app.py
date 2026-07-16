import streamlit as st
from streamlit_mic_recorder import mic_recorder

from database.schema import create_tables

from utils.speech_to_text import transcribe_audio

from auth.auth_manager import (
    register_user,
    login_user
)

from llm.gateway import generate_response

from nlp.preprocess import clean_text
from nlp.sentiment import analyze_sentiment

from memory.memory_manager import (
    save_chat,
    get_recent_history
)

from utils.helpers import build_prompt

create_tables()

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown("""
<div style="
background: linear-gradient(90deg,#4F46E5,#7C3AED);
padding:15px;
border-radius:12px;
margin-bottom:20px;
">

<h2 style="color:white;">
🤖 AI Assistant
</h2>

<p style="color:white;">
Powered by Groq Llama 3.3 • Memory Enabled
</p>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# Prevent duplicate voice processing
if "last_voice_text" not in st.session_state:
    st.session_state.last_voice_text = ""

# --------------------------------------------------
# LOGIN / SIGNUP
# --------------------------------------------------
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Choose Option",
        ["Login", "Signup"]
    )

    if menu == "Signup":

        st.subheader("Create Account")

        new_username = st.text_input("Username")
        new_email = st.text_input("Email")

        new_password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Signup"):

            success = register_user(
                new_username,
                new_email,
                new_password
            )

            if success:
                st.success(
                    "Account Created Successfully"
                )
            else:
                st.error(
                    "Username or Email already exists"
                )

    else:

        st.subheader("Login")

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user_id = login_user(
                username,
                password
            )

            if user_id:

                st.session_state.logged_in = True
                st.session_state.user_id = user_id
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )

    st.stop()

# --------------------------------------------------
# LOAD HISTORY ONLY ONCE
# --------------------------------------------------
if len(st.session_state.messages) == 0:

    history = get_recent_history(
        st.session_state.user_id,
        limit=20
    )

    for user_msg, bot_msg in reversed(history):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_msg
            }
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_msg
            }
        )

# --------------------------------------------------
# VOICE INPUT
# --------------------------------------------------
st.subheader("🎤 Voice Input")

audio = mic_recorder(
    start_prompt="🎤 Start Recording",
    stop_prompt="⏹ Stop Recording",
    use_container_width=True,
    key="voice_recorder"
)

voice_text = ""

if audio:

    try:

        voice_text = transcribe_audio(
            audio["bytes"]
        )

        st.success(
            f"Voice Detected: {voice_text}"
        )

    except Exception as e:

        st.error(
            f"Transcription Error: {e}"
        )

# --------------------------------------------------
# TEXT INPUT
# --------------------------------------------------
typed_input = st.chat_input(
    "Ask me anything..."
)

# --------------------------------------------------
# INPUT SOURCE SELECTION
# --------------------------------------------------
user_input = None

# Text has priority
if typed_input:
    user_input = typed_input

# Voice next
elif (
    voice_text
    and voice_text != st.session_state.last_voice_text
):
    user_input = voice_text
    st.session_state.last_voice_text = voice_text

# --------------------------------------------------
# PROCESS USER QUERY
# --------------------------------------------------
if user_input:

    try:

        cleaned = clean_text(
            user_input
        )

        sentiment = analyze_sentiment(
            cleaned
        )

        history = get_recent_history(
            st.session_state.user_id,
            limit=5
        )

        prompt = build_prompt(
            cleaned,
            history
        )

        response = generate_response(
            prompt
        )

        if not response:
            response = (
                "Sorry, I could not generate a response."
            )

        save_chat(
            st.session_state.user_id,
            user_input,
            response,
            sentiment
        )

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.rerun()

    except Exception as e:

        st.error(
            f"Error: {str(e)}"
        )

# --------------------------------------------------
# CHAT DISPLAY
# --------------------------------------------------
st.divider()

for message in reversed(
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):
        st.write(
            message["content"]
        )

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.success(
    f"Welcome {st.session_state.username}"
)

if st.sidebar.button(
    "Logout"
):

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.messages = []
    st.session_state.last_voice_text = ""

    st.rerun()

# --------------------------------------------------
# DOWNLOAD CHAT
# --------------------------------------------------
chat_export = ""

for msg in st.session_state.messages:

    chat_export += (
        f"{msg['role']}: "
        f"{msg['content']}\n\n"
    )

st.sidebar.download_button(
    "📄 Download Chat",
    chat_export,
    file_name="chat_history.txt"
)

# --------------------------------------------------
# RECENT CHATS
# --------------------------------------------------
with st.sidebar:

    st.header("Recent Chats")

    history = get_recent_history(
    st.session_state.user_id,
    limit=5
)

    for user_msg, bot_msg in history:

        st.markdown(
            f"**👤 User:** {user_msg}"
        )

        st.markdown(
            f"**🤖 Bot:** {bot_msg[:100]}..."
        )

        st.divider()