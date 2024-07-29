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
Question: 11 factories can make 22 cars per hour. How much time would it take 22 factories to make 88 cars?
Answer: A factory can make 22/11=2 cars per hour. 22 factories can make 22*2=44 cars per hour. Making 88 cars would take 88/44=2 hours. The answer is 2 hours.
Question: 5 people can create 5 donuts every 5 minutes. How much time would it take 25 people to make 100 donuts?
Answer:"""

response = model.generate_content(prompt, request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
print(response.text)