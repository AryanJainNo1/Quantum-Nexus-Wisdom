import streamlit as st
import google.generativeai as genai
import time

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Initialize session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Display title + dark mode toggle in one row
col1, col2 = st.columns([6, 1])
with col1:
    st.title("Quantum Nexus Wisdom")
with col2:
    st.session_state.dark_mode = st.toggle("🌙", value=st.session_state.dark_mode, label_visibility="collapsed")

# Choose theme colors
if st.session_state.dark_mode:
    bg_color = "#1e1e1e"
    user_color = "#0e639c"
    assistant_color = "#3c3c3c"
    text_color = "#ffffff"
else:
    bg_color = "#f5f7fa"
    user_color = "#e8f0fe"
    assistant_color = "#f1f3f4"
    text_color = "#000000"

# Inject dynamic CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lobster&family=Great+Vibes&display=swap');

    /* Apply background & text color for whole app */
    html, body, [data-testid="stApp"] {{
        background-color: {bg_color} !important;
        color: {text_color} !important;
    }}

    /* Base chat bubble style */
    .chat-message {{
        border-radius: 0.75rem;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}

    /* User messages with Lobster font */
    .user-message {{
        background-color: {user_color};
        color: {text_color};
        font-family: 'Lobster', cursive !important;
        font-size: 1.1rem;
        font-weight: 400;
    }}

    /* Assistant messages with Great Vibes font */
    .assistant-message {{
        background-color: {assistant_color};
        color: {text_color};
        font-family: 'Great+Vibes', cursive !important;
        font-size: 1rem;
        font-weight: 400;
    }}
    </style>
""", unsafe_allow_html=True)


# Display previous chat messages
for msg in st.session_state.messages:
    role_class = "user-message" if msg["role"] == "user" else "assistant-message"
    avatar = "User.png" if msg["role"] == "user" else "Assistant.png"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(f"<div class='chat-message {role_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# Gemini intro
ASSISTANT_INTRO = (
    "I am a large language model, based on Gemini. I'm a computer program designed "
    "to process and generate human-like text. I can answer questions, translate languages, "
    "write different kinds of creative content, and summarize factual topics. Essentially, "
    "I'm an AI assistant designed to help people with a wide range of tasks involving text."
)

# Get user input
prompt = st.chat_input("Type your message...")
if prompt:
    # Show user message
    with st.chat_message("user", avatar="User.png"):
        st.markdown(f"<div class='chat-message user-message'>{prompt}</div>", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Special intro response
    if any(x in prompt.lower() for x in ["who are you", "about yourself", "tell me about you", "what are you"]):
        full_response = ""
        with st.chat_message("assistant", avatar="Assistant.png"):
            msg_box = st.empty()
            for word in ASSISTANT_INTRO.split():
                full_response += word + " "
                msg_box.markdown(f"<div class='chat-message assistant-message'>{full_response}▌</div>", unsafe_allow_html=True)
                time.sleep(0.02)
            msg_box.markdown(f"<div class='chat-message assistant-message'>{full_response.strip()}</div>", unsafe_allow_html=True)
        st.session_state.messages.append({"role": "assistant", "content": full_response.strip()})
    else:
        # Gemini response with typing animation (letter by letter)
        with st.chat_message("assistant", avatar="Assistant.png"):
            message_placeholder = st.empty()
            full_response = ""
            response = st.session_state.chat.send_message(prompt)

            for char in response.text:
                full_response += char
                message_placeholder.markdown(
                    f"<div class='chat-message assistant-message'>{full_response}▌</div>",
                    unsafe_allow_html=True
                )
                time.sleep(0.01)

            message_placeholder.markdown(
                f"<div class='chat-message assistant-message'>{full_response.strip()}</div>",
                unsafe_allow_html=True
            )
        st.session_state.messages.append({"role": "assistant", "content": full_response.strip()})
