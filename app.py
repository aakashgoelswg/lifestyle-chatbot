# app.py

import streamlit as st
from duckduckgo_search import DDGS
import openai

# Set your OpenAI key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Set app theme and layout
st.set_page_config(page_title="All About Lifestyle", layout="centered")

# Styling (light grey/oasis green with olive green accents)
st.markdown("""
    <style>
        body {
            background-color: #f3f5f4;
        }
        .block-container {
            border: 2px solid #708238;
            border-radius: 15px;
            padding: 20px;
        }
        .stTextInput > div > div > input {
            background-color: #f3f5f4;
            border: 1px solid #708238;
        }
        .stButton>button {
            background-color: #708238;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("<h1 style='text-align: center; color: #708238;'>All About Lifestyle 🌿</h1>", unsafe_allow_html=True)

# Session state to remember name
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to search web and summarize
def fetch_summary(prompt):
    with DDGS() as ddgs:
        results = ddgs.text(prompt, max_results=5)
        text = "\n".join([f"{r['title']}: {r['href']}" for r in results])
    
    ai_prompt = f"Summarize the following lifestyle-related web results in a friendly, helpful tone:\n\n{text}\n\nAnswer:"
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": ai_prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# 1. Ask for Name
if not st.session_state.user_name:
    name = st.text_input("👋 Hey Dear User! What’s your name?", "")
    if name:
        st.session_state.user_name = name
        st.success(f"Nice to meet you, {name}! 😊 What are you looking for today in lifestyle?")
else:
    # 2. Continue the chat
    user_input = st.text_input("💬 Type your lifestyle question here:")

    if user_input:
        st.session_state.chat_history.append((st.session_state.user_name, user_input))
        reply = fetch_summary(user_input)
        st.session_state.chat_history.append(("Bot", reply))

    # 3. Display chat
    for speaker, msg in st.session_state.chat_history:
        if speaker == "Bot":
            st.markdown(f"<div style='background-color:#e8f5e9; padding:10px; border-radius:10px; margin-bottom:10px'><strong>{speaker}:</strong> {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background-color:#f0f0f0; padding:10px; border-radius:10px; margin-bottom:10px; text-align:right'><strong>{speaker}:</strong> {msg}</div>", unsafe_allow_html=True)
