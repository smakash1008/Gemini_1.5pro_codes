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
Answer the question using the text below. Respond with only the text provided.
Question: What should I do to fix my Samsung M31 Phone? It is restarting again and again after the recent software update and I can also see green lines on the screen.


Text:
Phone: Samsung M31.
Problem: Restart after Software Update and Green Line Problem.
What to do:
Safe Mode Restart.
Wipe Cache Partition.
Factory Reset.
If still persists contact Customer Support.

Phone: Iphone 15pro.
Problem: Restart after Software Update and Green Line Problem.
What to do:
Safe Mode Restart.
Wipe Cache Partition.
Factory Reset.
If still persists contact Customer Support.

Phone: ne Plus Nord 5.
Problem: Restart after Software Update and Green Line Problem.
What to do:
Safe Mode Restart.
Wipe Cache Partition.
Factory Reset.
If still persists contact Customer Support.

Phone: Samsung Galaxy S23.
Problem: Restart after Software Update and Green Line Problem.
What to do:
Safe Mode Restart.
Wipe Cache Partition.
Factory Reset.
If still persists contact Customer Support.
"""

def get_response(prompt):
    response = model.generate_content(prompt, request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
    return response.text

final_data = get_response(prompt)
print(final_data)