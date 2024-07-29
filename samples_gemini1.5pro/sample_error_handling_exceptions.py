# Importing the Necessary Libraries:

import json
import os
import time
import re
import docx2txt
import google.generativeai as genai
import pdfminer
from pdfminer.high_level import extract_text
from google.api_core import retry, exceptions
from dotenv import load_dotenv
load_dotenv()

# Configuring the Gemini API:

genai.configure(api_key=os.getenv("GOOGLE_API_KEY1"))

instruction = "Behave like the best facts teller. Give the best facts only."

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

@retry.Retry(
        predicate=retry.if_transient_error,
        initial=2.0,
        maximum=64.0,
        multiplier=2.0,
        timeout=300,
)

def generate_content_first_fail(prompt):
    if not hasattr(generate_content_first_fail, "call_counter"):
        generate_content_first_fail.call_counter = 0
        print(generate_content_first_fail.call_counter)

    generate_content_first_fail.call_counter += 1
    print(generate_content_first_fail.call_counter)
    try:
        if generate_content_first_fail.call_counter == 1:
            raise exceptions.ServiceUnavailable("Service Unavailable")

        response = model.generate_content(prompt)
        return response.text
    except exceptions.ServiceUnavailable as e:
        print(f"Error: {e}")
        raise

prompt = "Explain the 10 interesting facts about the Western Ghats?"

final_data = generate_content_first_fail(prompt)
final_data = final_data.replace("**","")
final_data = final_data.replace("#","")
print(final_data)