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

instruction = "Behave like the best sentence translator. Give all the data to the users correctly after translating. Translate based on the users requirement and give only the answers. Give the final data in the bigger font strictly"

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
),system_instruction=instruction, safety_settings=safety,)

# Getting the Response:

prompt = str(input("Enter the Sentence Which You Want To Translate: "))

def get_response(prompt):
    response = model.generate_content(prompt)
    return response.text

final_data = get_response(prompt)
final_data = final_data.replace("**","")
final_data = final_data.replace("#","")
print(final_data)