import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from google import genai

# Load .env locally (Streamlit Cloud uses Secrets automatically)
load_dotenv()

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Create Gemini client (google-genai SDK)
client = genai.Client(api_key=GEMINI_API_KEY)

# Supported model for this SDK
MODEL_ID = "gemini-2.0-flash"


def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF using PyMuPDF"""
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text.strip()


def ask_gemini(prompt, max_tokens=500):
    """Send prompt to Gemini and return response text"""
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config={
            "temperature": 0.5,
            "max_output_tokens": max_tokens,
        },
    )
    return response.text.strip()
