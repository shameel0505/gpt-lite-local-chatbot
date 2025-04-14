import streamlit as st
from gpt4all import GPT4All
from datetime import datetime

model = GPT4All("mistral-7b-openorca.Q4_0.gguf")

st.markdown(f"<h1 style='text-align: center; font-size: 42px; color:#FFFFFF'>🙋🏻 shameel's GPT-Lite</h1>", unsafe_allow_html=True)

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input form
with st.form(key='chat_form'):
    prompt = st.text_area("Type your message:", height=100)
    submitted = st.form_submit_button("Send")

# Generate and save conversation
if submitted and prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    full_prompt = "You are a helpful assistant.\n\n"
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "AI"
        full_prompt += f"{role}: {msg['content']}\n"
    full_prompt += "AI:"

    with st.spinner("Thinking..."):
        response = model.generate(full_prompt)
    st.session_state.messages.append({
        "role": "ai",
        "content": response,
        "timestamp": datetime.now().strftime("%H:%M")
    })

    # Scrollable chat area
    st.markdown("<div style='height: 400px; overflow-y: auto;'>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        align = "right" if msg["role"] == "user" else "left"
        bg_color = "#DCF8C6" if msg["role"] == "user" else "#FFFFFF"
        border_color = "#ddd" if msg["role"] != "user" else "transparent"
        st.markdown(
            f"<div style='background-color: {bg_color}; border: 1px solid {border_color}; "
            f"padding: 10px 15px; border-radius: 18px; margin: 10px 0; max-width: 75%; "
            f"float: {align}; clear: both; word-wrap: break-word; color: #000000;'>"
            f"{msg['content']}<br><span style='font-size: 10px; color: #999;'>{msg['timestamp']}</span>"
            "</div>", unsafe_allow_html=True
        )
    st.markdown("</div><div style='clear:both;'></div>", unsafe_allow_html=True)

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []

# JavaScript for enter key submission
st.markdown(f"""
<script>
document.addEventListener("keydown", function(e) {{
    if (e.key === "Enter" && !e.shiftKey && !e.isComposing) {{
        const textarea = document.activeElement;
        if (textarea && textarea.tagName === "TEXTAREA") {{
            e.preventDefault();
            const buttons = window.parent.document.querySelectorAll('button');
            buttons.forEach(btn => {{
                if (btn.innerText === "Send") {{
                    btn.click();
                }}
            }});
        }}
    }}
}});
</script>
<style>
body {{
    background-color: #f0f2f6;
}}
button[kind="primary"] {{
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    font-size: 16px;
    border-radius: 8px;
}}
button[kind="primary"]:hover {{
    background-color: #45a049;
}}
</style>
""", unsafe_allow_html=True)