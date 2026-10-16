"""
Pre-fetch quantized GGUF model weights for offline inference.
Usage: python download_model.py [model_filename.gguf]
"""
import sys
from gpt4all import GPT4All

DEFAULT_MODEL = "mistral-7b-openorca.Q4_0.gguf"

def main() -> None:
    model_name = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MODEL
    print(f"[*] Downloading/verifying local GGUF weights: {model_name}")
    _ = GPT4All(model_name)
    print(f"[✓] Model ready at ~/.cache/gpt4all/{model_name}")

if __name__ == "__main__":
    main()
