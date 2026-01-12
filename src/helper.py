import fitz  # PyMuPDF
import os
from dotenv import load_dotenv
from google.generativeai import genai

load_dotenv()

GENAI_API_KEY = os.getenv("GENAI_API_KEY")

client = genai.Client(api_key=GENAI_API_KEY)
MODEL_ID = "gemini-2.5-flash"


def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def ask_gemini(prompt, max_tokens=500):
    """Send a prompt to Gemini and return the response."""

    response = client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config={
            "temperature": 0.5,
            "max_output_tokens": max_tokens,
        },
    )

    return response.text

