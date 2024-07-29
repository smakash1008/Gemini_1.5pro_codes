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
from google.generativeai import caching
# Configuring the Gemini API:

genai.configure(api_key=os.getenv("GOOGLE_API_KEY1"))

instruction = "Analyze the audio or Group of audios provided by the user and give the details correctly and briefly about 10 lines to the user whatever they want."

safety = {
    'HATE' : 'BLOCK_NONE',
    'HARASSMENT' : 'BLOCK_NONE',
    'SEXUAL' : 'BLOCK_NONE',
    'DANGEROUS' : 'BLOCK_NONE',
}

# Configuring the Gemini Model:

model = genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=genai.GenerationConfig(
    temperature=0.7,
    top_p=0.95,
    top_k=64,
    response_mime_type='text/plain',
    max_output_tokens=8192,
),system_instruction=instruction, safety_settings=safety,)

for file in genai.list_files():
    print(f"File Name: {file.display_name} and File URI: {file.uri}")
    print(f"File to be Deleted: {file.display_name}")
    genai.delete_file(file.name)

for file in genai.list_files():
    print(f"File Name: {file.display_name} and File URI: {file.uri}")

print("File Deleted Successfully...")

for c in caching.CachedContent.list():
    print(c)
    c.delete()

