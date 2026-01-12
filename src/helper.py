import os
from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

# load env (local) + Streamlit secrets (cloud)
load_dotenv()

GENAI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GENAI_API_KEY)

# create model once
model = genai.GenerativeModel("gemini-1.5-flash")


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text
