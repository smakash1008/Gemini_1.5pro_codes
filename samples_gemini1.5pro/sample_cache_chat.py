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
import datetime

# Configuring the Gemini API:

genai.configure(api_key=os.getenv("GOOGLE_API_KEY1"))

file_path = input("Enter the file path: ")

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

# Creating the cache:

cache = caching.CachedContent.create(
    model="models/gemini-1.5-flash-001",
    display_name="smaple-answers.pdf",
    system_instruction="Behave like the best pdf reader. Answer all the questions asked in the prompt by the user. Answer all the questions only from the content present in the uploaded pdf. The final answer should match the content in the uploaded file.",
    contents=[file_uploaded],
    ttl=datetime.timedelta(minutes=5),
)

model = genai.GenerativeModel.from_cached_content(cached_content=cache)

chat = model.start_chat(history=[])

response = chat.send_message(input("Enter the Question: "),request_options={'retry':retry.Retry(predicate=retry.if_transient_error)})
print(response.text)

print(chat.history)

for c in caching.CachedContent.list():
    print(c)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")

# Deleting the File from Gemini:

print(f"The file to be deleted: {file_uploaded.display_name}")
genai.delete_file(file_uploaded)

for file in genai.list_files():
    print(f"File Name: {file.display_name}  and File URI: {file.uri}")

print("File Deleted Successfully.")

cache.update(ttl=datetime.timedelta(hours=2))

for c in caching.CachedContent.list():
    print(c)

cache.delete()

for c in caching.CachedContent.list():
    print(c)