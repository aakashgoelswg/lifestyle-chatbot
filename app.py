import streamlit as st
from duckduckgo_search import DDGS
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set app layout and design
st.set_page_config(page_title="All About Lifestyle", layout="centered")
st.markdown("""
    <style>
        body { background-color: #f3f5f4; }
        .block-container { border: 2px solid #708238; border-radius: 15px; padding: 20px; }
        .stTextInput > div > div > input { background-color: #f3f5f4; border: 1px solid #708238; }
        .stButton>button { background-color: #708238; color: white; }
    </style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #708238;'>All About Lifestyle 🌿</h1>", unsafe_allow_html=True)

if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Get user name
if not st.session_state.user_name:
    name = st.text_input("👋 Hey Dear User! What’s your name?", "")
    if name:
        if len(name.split()) > 2 or any(char.isdigit() for char in name):
            st.error("Please enter a valid name (no numbers or long sentences).")
        else:
            st.session_state.user_name = name.strip()
            st.success(f"Nice to meet you, {name.strip()}! 😊 What are you looking for today in lifestyle?")
else:
    # Chat Phase
    user_input = st.text_input("💬 Type your lifestyle question here:")
    if user_input:
        try:
            st.session_state.chat_history.append((st.session_state.user_name, user_input))
            reply = fetch_summary(user_input)
            st.session_state.chat_history.append(("Bot", reply))
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Display chat history
    for speaker, msg in st.session_state.chat_history:
        if speaker == "Bot":
            st.markdown(f"<div style='background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:10px'><strong>{speaker}:</strong> {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color:#f0f0f0; padding:10px; border-radius:10px; margin-bottom:10px; text-align:right'><strong>{speaker}:</strong> {msg}</div>", unsafe_allow_html=True)
