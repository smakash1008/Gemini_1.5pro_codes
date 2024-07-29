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


for i in range(2):
    file_uploaded = 0
    file_uploaded1 = 0
    prompt = []
    file_path = input("Enter the File Path:")
    file_uploaded = genai.upload_file(file_path)
    print(f"File Name: {file_uploaded.display_name}, File Uri: {file_uploaded.uri} and File Mime: {file_uploaded.mime_type}")
    print(file_uploaded)
    file_path1 = input("Enter the File Path:")
    file_uploaded1 = genai.upload_file(file_path1)
    print(f"File Name: {file_uploaded1.display_name}, File Uri: {file_uploaded1.uri} and File Mime: {file_uploaded1.mime_type}")
    print(file_uploaded1)
    get_file = genai.get_file(file_uploaded.name)
    print(get_file.name)
    print(get_file.display_name, get_file.uri)
    print(get_file.state.name)
    while get_file.state.name == "PROCESSING":
        print("The File is Still Processing...")
        time.sleep(10)
        get_file = genai.get_file(file_uploaded.name)
        print(get_file.name)
        print(get_file.display_name, get_file.uri)
        print(get_file.state.name)
    if get_file.state.name == "FAILED":
        raise ValueError(get_file.state.name)
    if get_file.state.name != "ACTIVE":
        raise Exception(f"File Name: {get_file.name} Not Processed")
    print("The File is Ready Now...")
    get_file1 = genai.get_file(file_uploaded1.name)
    print(get_file1.name)
    print(get_file1.display_name, get_file1.uri)
    print(get_file1.state.name)
    while get_file1.state.name == "PROCESSING":
        print("The File is Still Processing...")
        time.sleep(10)
        get_file1 = genai.get_file(file_uploaded1.name)
        print(get_file1.name)
        print(get_file1.display_name, get_file1.uri)
        print(get_file1.state.name)
    if get_file1.state.name == "FAILED":
        raise ValueError(get_file1.state.name)
    if get_file1.state.name != "ACTIVE":
        raise Exception(f"File Name: {get_file1.name} Not Processed")
    print("The File is Ready Now...")
    for file in genai.list_files():
        print(f"File Name: {file.display_name}  and File URI: {file.uri}")
    prompt = [input("Enter the prompt: "), file_uploaded, file_uploaded1]
    response = chat.send_message(prompt, request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
    print(response.text.replace("**","").replace("#",""))
    prompt.clear()
    file_uploaded = 0
    print(file_uploaded)
    file_uploaded1 = 0
    print(file_uploaded1)
    time.sleep(30)
        
print(chat.history)

for file in genai.list_files():
        print(f"File Name: {file.display_name}  and File URI: {file.uri}")
        print(f"The file to be deleted: {file.display_name}")
        genai.delete_file(file)
for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")
print("File Deleted Successfully...")