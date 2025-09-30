import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List all models available to your API key
models = genai.list_models()
for model in models:
    print("Model name:", model.name)
    print("Supports generate_content:", hasattr(model, "generate_content"))
    print("Supports chat:", hasattr(model, "chat"))
    print("------")
