# Importing the Necessary Libraries:

import json
import os
import time
import re
import docx2txt
import google.generativeai as genai
import pdfminer
from pdfminer.high_level import extract_text
from google.api_core import retry
from dotenv import load_dotenv
load_dotenv()
import typing_extensions

# Configuring the Gemini API:

genai.configure(api_key=os.getenv("GOOGLE_API_KEY1"))

instructions = "Behave like the best AI and give th answers as per the user request."

safety = {
    'HATE' : 'BLOCK_NONE',
    'HARASSMENT' : 'BLOCK_NONE',
    'SEXUAL' : 'BLOCK_NONE',
    'DANGEROUS' : 'BLOCK_NONE',
}

# Configuring the Gemini Model:

model = genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=genai.GenerationConfig(
    temperature=1,
    top_p=0.95,
    top_k=64,
    response_mime_type='text/plain',
    max_output_tokens=8192,
),system_instruction=instructions, safety_settings=safety,)

# Getting the Response:

triangle = "triangle.png"
square = "square.png"
pentagon = "pentagon.png"

prompt = """Look at this sequence of three shapes. What shape should come as the fourth shape? Explain
your reasoning with detailed descriptions of the first shapes."""

response = model.generate_content([prompt,triangle,square,pentagon])
print(response.text)