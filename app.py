import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Set up Streamlit app config
st.set_page_config(page_title="Smart Chatbot", page_icon="🤖")

# Load the Falcon-RW-1B model from HuggingFace
@st.cache_resource
def load_model():
    tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-rw-1b")
    model = AutoModelForCausalLM.from_pretrained(
        "tiiuae/falcon-rw-1b",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"  # Automatically detects GPU if available
    )
    return pipeline("text-generation", model=model, tokenizer=tokenizer)

generator = load_model()

# UI for Streamlit
st.title("🧠 Smart Chatbot (Powered by Falcon-1B)")
st.write("Ask me anything, and I'll try my best!")

# Input field for user query
user_input = st.text_input("You:", key="user_input")

# When user inputs a query
if user_input:
    with st.spinner("Generating response..."):
        result = generator(user_input, max_new_tokens=150, do_sample=True)[0]['generated_text']
        st.markdown(f"**Bot:** {result.strip()}")