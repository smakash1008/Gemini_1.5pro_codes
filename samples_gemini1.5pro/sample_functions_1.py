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

instruction = "Use the functions wisely and give the result as per the user request. Give the final data strictly without fail."

safety = {
    'HATE' : 'BLOCK_NONE',
    'HARASSMENT' : 'BLOCK_NONE',
    'SEXUAL' : 'BLOCK_NONE',
    'DANGEROUS' : 'BLOCK_NONE',
}

# Configuring the Gemini Model:

def add(a : int, b : int):
    '''retrun a + b'''
    return a + b

def subtract(a : int, b : int):
    '''return a - b'''
    return a - b

def multiply(a : int, b : int):
    '''return a * b'''
    return a * b

def divide(a : int, b : int):
    '''return a / b'''
    return a / b

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",generation_config=genai.GenerationConfig(
    temperature=0.7,
    top_p=0.95,
    top_k=64,
    response_mime_type='text/plain',
    max_output_tokens=8192,
),system_instruction=instruction, safety_settings=safety, tools=[add, subtract, multiply, divide])

print(model)

chat = model.start_chat(enable_automatic_function_calling=True, history=[])

prompt = input("Enter the Prompt: ")

response = chat.send_message(prompt,request_options={'retry':retry.Retry(predicate=retry.if_transient_error)})
print(response.text)