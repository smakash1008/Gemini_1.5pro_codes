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

for model in genai.list_models():
    print(model.name)

model_details = genai.get_model("models/gemini-1.5-pro")
print(model_details)

print(model_details.version)
print(model_details.display_name)
print(model_details.input_token_limit)
print(model_details.output_token_limit)
print(model_details.max_temperature)

response = chat.send_message("Explain the names of the Newtons laws?", request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
print(response.text.replace("**",""))

response = chat.send_message("Briefly explain the Newton's Third Law?", request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
print(response.text.replace("**",""))

response = chat.send_message("Father of our India name alone", request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
print(response.text.replace("**",""))

print(chat.history)