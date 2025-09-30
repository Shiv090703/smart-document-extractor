import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Gemini with API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables. Check your .env file.")

genai.configure(api_key=api_key)

def ask_ai(prompt: str) -> str:
    """
    Sends a question to Google's free Gemini AI and returns the answer.
    """
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    # Safely extract text
    if hasattr(response, "text") and response.text:
        return response.text.strip()
    elif hasattr(response, "candidates") and response.candidates:
        return response.candidates[0].content.parts[0].text.strip()
    else:
        return "⚠️ No valid response from Gemini."
