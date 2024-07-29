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

# Uploading the File to the Gemini:

file_path = "Audio from AKASH SM1.oga"

def upload_to_gemini(file_path):
    file = genai.upload_file(file_path)
    print(f"File Name: {file.display_name}, File Uri: {file.uri} and File Mime: {file.mime_type}")
    return file

file_uploaded = upload_to_gemini(file_path)
print(file_uploaded)

uploaded_file_name = file_uploaded.name   
print(uploaded_file_name)

# Getting the File:

def get_files(file_uploaded):
    get_file = genai.get_file(uploaded_file_name)
    print(get_file.name)
    print(get_file.display_name, get_file.uri)
    print(get_file.state.name)
    while get_file.state.name == "PROCESSING":
        print("The File is Still Processing...")
        time.sleep(10)
        get_file = genai.get_file(uploaded_file_name)
        print(get_file.name)
        print(get_file.display_name, get_file.uri)
        print(get_file.state.name)
    if get_file.state.name == "FAILED":
        raise ValueError(get_file.state.name)
    if get_file.state.name != "ACTIVE":
        raise Exception(f"File Name: {get_file.name} Not Processed")
    return "The File is Ready Now..."

file_state = get_files(file_uploaded)
print(file_state)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")

# Getting the Response:

def get_response(file_uploaded):
    response = model.generate_content(file_uploaded,request_options={"retry": retry.Retry(predicate=retry.if_transient_error)})
    return response.text

data = get_response(file_uploaded)
data = data.replace("**","")
data = data.replace("*","")
data = data.replace("#","")
print(data)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")

# Deleting the File from Gemini:

print(f"The file to be deleted: {file_uploaded.display_name}")
genai.delete_file(file_uploaded)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")

print("File Deleted Successfully.") 