import streamlit as st
from gpt4all import GPT4All

# Initialize the local model
model = GPT4All("mistral-7b-openorca.Q4_0.gguf")

st.set_page_config(page_title="shameel's GPT-Lite", layout="centered")

# Custom title styling
st.markdown("<h1 style='text-align: center; font-size: 42px;'>💬 shameel's GPT-Lite</h1>", unsafe_allow_html=True)

# Add custom CSS for better chat look
st.markdown(
    """
    <style>
    .user-msg {
        background-color: #DCF8C6;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: right;
        color: #000;
    }
    .ai-msg {
        background-color: #F1F0F0;
        padding: 10px 15px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: left;
        color: #000;
    }
    button[kind="primary"] {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 8px;
    }
    button[kind="primary"]:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Input form with Send button
with st.form(key='chat_form'):
    prompt = st.text_area("Type your message:", height=100)
    submitted = st.form_submit_button("🚀 Send", type="primary")

if submitted and prompt:
    full_prompt = f"You are a helpful assistant.\n\nUser: {prompt}\nAI:"
    response = model.generate(full_prompt)
    st.markdown(f'<div class="user-msg">{prompt}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="ai-msg">{response}</div>', unsafe_allow_html=True)