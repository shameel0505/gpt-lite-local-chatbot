"""
GPT-Lite: Production-ready local LLM chat interface.
Built with Streamlit and GPT4All for zero-telemetry, edge-accelerated inference.
"""

from datetime import datetime
import json
import logging
from typing import List, Dict, Any
import streamlit as st
from gpt4all import GPT4All

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("gpt-lite")

st.set_page_config(
    page_title="GPT-Lite | Local LLM",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Model Management & Caching
# ---------------------------------------------------------
AVAILABLE_MODELS = {
    "Mistral 7B OpenOrca (Q4_0)": "mistral-7b-openorca.Q4_0.gguf",
    "Llama 3 8B Instruct (Q4_0)": "Meta-Llama-3-8B-Instruct.Q4_0.gguf",
    "Orca 2 7B (Q4_0)": "orca-2-7b.Q4_0.gguf",
}

@st.cache_resource(show_spinner=False)
def load_model(model_name: str, n_threads: int = 4) -> GPT4All:
    """
    Cached model loader to prevent memory leaks and reload latency.
    Keeps model weights memory-mapped in RAM/VRAM.
    """
    logger.info(f"Loading local model: {model_name} with {n_threads} threads")
    return GPT4All(model_name, n_threads=n_threads)

# ---------------------------------------------------------
# Sidebar Configuration
# ---------------------------------------------------------
with st.sidebar:
    st.title("🧠 GPT-Lite Settings")
    st.caption("Zero-telemetry local inference engine")
    
    selected_model_label = st.selectbox(
        "Model Selection",
        options=list(AVAILABLE_MODELS.keys()),
        index=0,
        help="GGUF quantized weights stored locally in ~/.cache/gpt4all"
    )
    selected_model_file = AVAILABLE_MODELS[selected_model_label]
    
    st.divider()
    st.subheader("Inference Parameters")
    temperature = st.slider(
        "Temperature",
        min_value=0.1,
        max_value=1.5,
        value=0.7,
        step=0.05,
        help="Higher values yield more creative responses, lower values are more deterministic."
    )
    max_tokens = st.slider(
        "Max Output Tokens",
        min_value=64,
        max_value=2048,
        value=512,
        step=64,
        help="Maximum number of tokens to generate per response."
    )
    context_window = st.slider(
        "Context Memory (Turns)",
        min_value=1,
        max_value=10,
        value=4,
        step=1,
        help="Number of previous dialogue turns passed into the prompt context."
    )
    cpu_threads = st.slider(
        "CPU Worker Threads",
        min_value=1,
        max_value=16,
        value=4,
        step=1,
        help="Number of physical CPU threads allocated for GGML compute."
    )
    
    st.divider()
    system_prompt = st.text_area(
        "System Prompt",
        value="You are an expert AI software engineer and helpful assistant. Provide concise, accurate, and structured answers.",
        height=100
    )
    
    st.divider()
    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_tokens_est = 0
        st.rerun()

# ---------------------------------------------------------
# State Initialization
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens_est" not in st.session_state:
    st.session_state.total_tokens_est = 0

# ---------------------------------------------------------
# Chat Rendering
# ---------------------------------------------------------
st.title("🙋🏻 GPT-Lite Local Assistant")
st.caption(f"Running on `{selected_model_file}` | Fully Offline | Private")

# Render historical messages using native st.chat_message (safe from XSS)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "timestamp" in message:
            st.caption(f"_{message['timestamp']}_")

# ---------------------------------------------------------
# User Input & Prompt Construction
# ---------------------------------------------------------
prompt = st.chat_input("Ask a question or describe a task...")

if prompt:
    now_str = datetime.now().strftime("%H:%M")
    
    # Append and render user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "timestamp": now_str
    })
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"_{now_str}_")

    # Load model instance safely
    try:
        with st.spinner("Initializing runtime weights..."):
            model = load_model(selected_model_file, n_threads=cpu_threads)
    except Exception as e:
        st.error(f"Failed to load model `{selected_model_file}`: {str(e)}")
        st.stop()

    # Build memory-managed context prompt
    # Keep only the last N turns to avoid context overflow and latency degradation
    trimmed_history = st.session_state.messages[- (context_window * 2):]
    
    formatted_prompt = f"### System:\n{system_prompt}\n\n"
    for msg in trimmed_history:
        role_tag = "Human" if msg["role"] == "user" else "Assistant"
        formatted_prompt += f"### {role_tag}:\n{msg['content']}\n\n"
    formatted_prompt += "### Assistant:\n"

    # Generate model response
    with st.chat_message("assistant"):
        with st.spinner("Generating response..."):
            start_time = datetime.now()
            try:
                response = model.generate(
                    formatted_prompt,
                    max_tokens=max_tokens,
                    temp=temperature
                ).strip()
            except Exception as e:
                response = f"⚠️ Generation error: {str(e)}"
                logger.error(f"Inference failed: {e}", exc_info=True)
            elapsed = (datetime.now() - start_time).total_seconds()
            
            st.markdown(response)
            st.caption(f"_{datetime.now().strftime('%H:%M')} | Latency: {elapsed:.2f}s_")

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().strftime("%H:%M")
    })

# ---------------------------------------------------------
# Chat Export Options
# ---------------------------------------------------------
if st.session_state.messages:
    with st.sidebar:
        st.divider()
        chat_json = json.dumps(st.session_state.messages, indent=2)
        st.download_button(
            "💾 Export Chat (JSON)",
            data=chat_json,
            file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
