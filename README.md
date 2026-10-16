# 🧠 GPT-Lite: High-Performance Local LLM Interface

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io/)
[![Zero Telemetry](https://img.shields.io/badge/Privacy-100%25%20Offline-success.svg)](#)

A production-grade, zero-telemetry local conversational AI interface built with **Streamlit** and **GPT4All (GGML/llama.cpp)**. Designed for air-gapped environments, edge compute, and privacy-critical workflows where sending proprietary code or sensitive data to third-party cloud APIs is unacceptable.

---

## 🏛️ Architectural Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Web UI                         │
│  - Native st.chat_message UI (Zero XSS / Sanitized Output)  │
│  - Dynamic Session State & Context History Pruning          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Cached Model Inference Layer                │
│  - @st.cache_resource (Eliminates Re-Instantiation Latency) │
│  - Multi-threaded CPU/Metal Execution (AVX2 / Accelerate)   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Local GGUF Weights Storage                  │
│  - 4-bit Quantization (Mistral 7B / Llama 3 8B / Orca 2)    │
│  - Low VRAM Footprint (~4.2 GB Memory Mapped)               │
└─────────────────────────────────────────────────────────────┘
```

### Key Engineering Decisions:
1. **Memory Preservation (`@st.cache_resource`):** In Streamlit, each user interaction triggers a script re-run. Caching the model pointer prevents multi-gigabyte weight reloads into memory and eliminates redundant file I/O overhead.
2. **Context Window Pruning:** Rather than passing unbounded chat logs into the context buffer (which degrades token throughput and causes context overflow), the engine automatically bounds the history to the last $N$ turns configurable via the sidebar.
3. **Safe Rendering:** Avoids raw DOM and JavaScript injection; all message strings are rendered through Streamlit's native security-hardened markdown parser.

---

## ⚡ Hardware Requirements & Performance

| Model | Quantization | RAM Required | Recommended Threads | Inference Speed (Tokens/s) |
| :--- | :--- | :--- | :--- | :--- |
| **Mistral 7B OpenOrca** | Q4_0 | ~4.5 GB | 4 - 8 | 18 - 32 tok/s (M-series / modern x86) |
| **Meta Llama 3 8B** | Q4_0 | ~5.2 GB | 4 - 8 | 15 - 28 tok/s |
| **Orca 2 7B** | Q4_0 | ~4.5 GB | 4 - 8 | 18 - 30 tok/s |

---

## 🛠️ Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher
- C++ build tools (standard on macOS and Linux)

### 2. Clone the Repository
```bash
git clone https://github.com/shameel0505/gpt-lite-local-chatbot.git
cd gpt-lite-local-chatbot
```

### 3. Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Optional: Pre-Fetch Model Weights
To pre-download the default GGUF model without launching the UI:
```bash
python download_model.py mistral-7b-openorca.Q4_0.gguf
```

### 6. Launch Application
```bash
streamlit run app.py
```
The interface will automatically open in your default browser at `http://localhost:8501`.

---

## ⚙️ Configuration & Features

- **Model Switcher:** Easily toggle between multiple quantized GGUF architectures directly from the sidebar.
- **Inference Tuners:** Adjust temperature (creativity vs determinism), max token generation, and CPU worker threads in real-time.
- **Session Export:** Export complete conversation transcripts into structured JSON for audit trails or offline evaluation.
- **Zero Cloud Footprint:** No external network requests during inference; completely safe for confidential business analysis.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
