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

instruction = "Give the details as requested by the user strictly."

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
), system_instruction=instruction, safety_settings=safety)

chat = model.start_chat(history=[])
print(chat)

for i in range(5):
    response = chat.send_message(input("Enter the prompt message: "), request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
    print(response.text.replace("**","").replace("#",""))
    time.sleep(20)

print(chat.history)