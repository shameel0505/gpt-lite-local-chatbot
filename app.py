import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Light Chatbot", page_icon="🤖")

@st.cache_resource
def load_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

generator = load_model()

st.title("🧠 shameels Chatbot (Flan-T5)")
st.write("Ask me anything — I'll try my best!")

user_input = st.text_input("You:", key="user_input")

if user_input:
    with st.spinner("Generating response..."):
        result = generator(user_input, max_new_tokens=100)[0]['generated_text']
        st.markdown(f"**Bot:** {result}")