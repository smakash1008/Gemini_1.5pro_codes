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

model_details = genai.get_model("models/gemini-1.5-pro")
print(model_details)
print(model_details.input_token_limit)
print(model_details.output_token_limit)
print(model_details.display_name)
print(model_details.temperature)
print(model_details.max_temperature)
print(model_details.top_p)
print(model_details.top_k)

# Getting the Response:

file_path = input("Enter the File Path: ")

def upload_to_gemini(file_path):
    file = genai.upload_file(file_path)
    print(f"File Name: {file.display_name}, File Uri: {file.uri} and File Mime: {file.mime_type}")
    return file

file_uploaded = upload_to_gemini(file_path)
print(file_uploaded)

prompt = "Describe the content of the file."

tokens = model.count_tokens([prompt,file_uploaded])
print(tokens.total_tokens)

def get_response(prompt):
    response = model.generate_content([prompt,file_uploaded],request_options={'retry': retry.Retry(predicate=retry.if_transient_error)})
    print(response.usage_metadata)
    print(response.parts)
    print(response.candidates)
    print(response.candidates[0].finish_reason)
    print(response.candidates[0].safety_ratings)
    print(response.candidates[0])
    return response.text
    
final_data = get_response(prompt)
print(final_data)

for file in genai.list_files():
    print(f"File Name: {file.display_name} and File URI: {file.uri}")

print(f"File to be deleted: {file.display_name}")
genai.delete_file(file)

for file in genai.list_files():
    print(f"File Name: {file.display_name} and File URI: {file.uri}")

print("File Deleted Successfully...")

# Note:

# For Images : 258 tokens by default.
# For Videos : 263 tokens per second by default.
# For Audio : 32 tokens per second by default.
# For Text : Tokens can be based on a word, charcters, etc. The symbols are also considered.
# If we use system instruction and tools (functions), at that time the count of tokens will increase based on that.
