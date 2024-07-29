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

instruction = "Behave like the best AI and give th answers as per the user request."

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

prompt = """
Summarize this text point by point.
Text: I am Akash SM. I am a Vlogger as well as a Content Creator. I love to travel to many Places and explore the places.
I would like to interact with diferent types of people in that places. I travelled all over the South India like Tamilnadu, Kerala, Karnataka, Telangana, Pondicherry and Andhra Pradesh.
My Youtube Channel name is AK VLOGS AND TRAVELS.
The Answer is:
"""

def get_response(prompt):
    response = model.generate_content(prompt, request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
    return response.text

final_data = get_response(prompt)
final_data = final_data.replace("**","")
print(final_data)