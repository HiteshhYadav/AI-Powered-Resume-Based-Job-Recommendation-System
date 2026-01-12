import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai

# Load .env for local development
# On Streamlit Cloud, secrets are loaded automatically
load_dotenv()

# Read API key (works locally + cloud)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Initialize model once
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_text_from_pdf(uploaded_file):
    """Extract text from uploaded PDF resume"""
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def ask_gemini(prompt):
    """Send prompt to Gemini and return response text"""
    response = model.generate_content(prompt)
    return response.text.strip()
