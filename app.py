import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Chat with GPT-2", page_icon="🤖")

# Load HuggingFace model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="gpt2")

generator = load_model()

st.title("💬 Chatbot (Powered by HuggingFace GPT-2)")
st.write("Ask me anything!")

# Chat input
user_input = st.text_input("You:", key="user_input")

if user_input:
    with st.spinner("Thinking..."):
        result = generator(user_input, max_length=100, do_sample=True)[0]['generated_text']
        st.markdown(f"**Bot:** {result[len(user_input):].strip()}")