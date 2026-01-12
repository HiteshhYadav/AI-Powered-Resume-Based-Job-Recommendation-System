import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
import google.generativeai as genai

# Load .env locally (Streamlit Cloud uses Secrets)
load_dotenv()

# Read API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model once
model = genai.GenerativeModel("gemini-2.5-flash")


def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF using PyMuPDF"""
    text = ""

    # Open PDF from uploaded file bytes
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text() + "\n"

    return text.strip()


def ask_gemini(prompt):
    """Send prompt to Gemini and return response text"""
    response = model.generate_content(prompt)
    return response.text.strip()
