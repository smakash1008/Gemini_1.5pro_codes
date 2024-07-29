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

instruction = "Behave like a light assisting bot. Follow the prompt only as well as dont iterate again and again in the any mode."

safety = {
    'HATE' : 'BLOCK_NONE',
    'HARASSMENT' : 'BLOCK_NONE',
    'SEXUAL' : 'BLOCK_NONE',
    'DANGEROUS' : 'BLOCK_NONE',
}

# Configuring the Gemini Model:

def enable_light():
    """Light Bot should Enable the light. The light should glow after enabling."""
    print("Bot...Lights Enabled.")

def set_light_color(rgb_hex:str):
    """Light Bot should set the light color to the following color mentioned."""
    print(f"Bot... Light Color set to {rgb_hex}")

def disable_light():
    """Light Bot should turn off the light..."""
    print("Bot... Lights Turned Offf")

tools=["enable_light", "set_light_color", "disable_light"]

tool_config = {
    "function_calling_config":{
    "mode" : "any",
    "allowed_function_names" : ["enable_light", "set_light_color", "disable_light"]
    }
}

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",generation_config=genai.GenerationConfig(
    temperature=0.7,
    top_p=0.95,
    top_k=64,
    response_mime_type='text/plain',
    max_output_tokens=8192,
),system_instruction=instruction, safety_settings=safety,tools=[enable_light, set_light_color, disable_light], tool_config=tool_config)

print(model)

prompt = "Please switch on the light.."

chat = model.start_chat(enable_automatic_function_calling=True,history=[])

response = chat.send_message(prompt,request_options={'retry':retry.Retry(predicate=retry.if_transient_error)})
print(response.text)
print("Successfully Done...")