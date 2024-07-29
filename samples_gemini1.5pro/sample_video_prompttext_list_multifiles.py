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

instruction = "Analyze the video or Group of videos provided by the user and give the details correctly and briefly about 10 lines to the user whatever they want. Also identify the things/animals/birds present in the videos correctly without fail. If unable to identify dont give anything strictly. Give the final data in points."

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

# Uploading the File to the Gemini:

file_path = input("Enter the File Path:")

def upload_to_gemini(file_path):
    file = genai.upload_file(file_path)
    print(f"File Name: {file.display_name}, File Uri: {file.uri} and File Mime: {file.mime_type}")
    return file

file_uploaded = upload_to_gemini(file_path)
print(file_uploaded)

uploaded_file_name = file_uploaded.name
print(uploaded_file_name)

file_path1 = input("Enter the File Path:")

def upload_to_gemini1(file_path1):
    file1 = genai.upload_file(file_path1)
    print(f"File Name: {file1.display_name}, File Uri: {file1.uri} and File Mime: {file1.mime_type}")
    return file1

file_uploaded1 = upload_to_gemini1(file_path1)
print(file_uploaded1)

uploaded_file_name1 = file_uploaded.name
print(uploaded_file_name1)

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

def get_files1(file_uploaded1):
    get_file1 = genai.get_file(uploaded_file_name1)
    print(get_file1.name)
    print(get_file1.display_name, get_file1.uri)
    print(get_file1.state.name)
    while get_file1.state.name == "PROCESSING":
        print("The File is Still Processing...")
        time.sleep(10)
        get_file1 = genai.get_file(uploaded_file_name1)
        print(get_file1.name)
        print(get_file1.display_name, get_file1.uri)
        print(get_file1.state.name)
    if get_file1.state.name == "FAILED":
        raise ValueError(get_file1.state.name)
    if get_file1.state.name != "ACTIVE":
        raise Exception(f"File Name: {get_file1.name} Not Processed")
    return "The File is Ready Now..."

file_state1 = get_files1(file_uploaded)
print(file_state1)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")

# Getting the Response:

prompt = input("Enter the prompt: ")


def get_response(prompt,file_uploaded,file_uploaded1):
    response = model.generate_content([prompt,file_uploaded,file_uploaded1],request_options={'retry': retry.Retry(predicate=retry.if_transient_error)})
    return response.text

data = get_response(prompt,file_uploaded,file_uploaded1)
data = data.replace("**","")
data = data.replace("*","")
data = data.replace("#","")
print(data)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")

# Deleting the File from Gemini:

print(f"The file to be deleted: {file_uploaded.display_name}")
genai.delete_file(file_uploaded)

print(f"The file to be deleted: {file_uploaded1.display_name}")
genai.delete_file(file_uploaded1)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")

print("File Deleted Successfully.")