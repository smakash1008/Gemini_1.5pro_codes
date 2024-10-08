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
    response_mime_type='application/json',
    max_output_tokens=8192,
),system_instruction=instructions, safety_settings=safety,)

# Getting the Response:

entity_recognition_text = "John Johnson, the CEO of the Oil Inc. and Coal Inc. companies, has unveiled plans to build a new factory in Houston, Texas."
prompt = f"""
Generate list of entities in text based on the following Python class structure:

class Category(str, str):
    Person = 'Person'
    Company = 'Company'
    State = 'State'
    City = 'City'

class Entity(TypedDict):
  name: str
  category: Category

class Entities(TypedDict):
  entities: list[Entities]

{entity_recognition_text}"""

response = model.generate_content(prompt)
print(response.text)