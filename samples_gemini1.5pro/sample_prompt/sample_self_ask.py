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

prompt = """
Question: Who was the president of the united states when Mozart died?
Are follow up questions needed?: yes.
Follow up: When did Mozart died?
Intermediate answer: 1791.
Follow up: Who was the president of the united states in 1791?
Intermediate answer: George Washington.
Final answer: When Mozart died George Washington was the president of the USA.

Question: Where did the Emperor of Japan, who ruled the year Maria Skłodowska was born, die?"""

response = model.generate_content(prompt)
print(response.text)