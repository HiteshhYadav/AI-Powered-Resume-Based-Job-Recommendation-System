import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from google import genai

# Load .env locally (Streamlit Cloud uses Secrets)
load_dotenv()

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Create model (ONCE)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.5,
        "max_output_tokens": 500,
    },
)

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF using PyMuPDF"""
    text = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text() + "\n"
    return text.strip()


def ask_gemini(prompt):
    """Send prompt to Gemini and return response"""
    response = model.generate_content(prompt)
    return response.text.strip()

