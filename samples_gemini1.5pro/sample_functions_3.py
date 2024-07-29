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

def destination_city(state:str):
    """The function should return the city name and the state where it is situated.
    Args: 
         state should be also in the string. The state is the name of the state where the city is present.
         The names can be case sensitive.
    Return: The destination city based on the state."""
    if state == "Karnataka":
        return "Bengaluru"
    elif state == "Telangana":
        return "Hyderabad"
    elif state == 'Tamilnadu':
        return "Chennai"
    else:
        return None

def start_city(state:str):
    """The function should return the city name and the state where it is situated.
    Args: 
         state should be also in the string. The state is the name of the state where the city is present.
         The name can be case sensitive.
    Return: The start city based on the state."""
    if state == "Karnataka":
        return "Bengaluru"
    elif state == "Telangana":
        return "Hyderabad"
    elif state == 'Tamilnadu':
        return "Chennai"
    else:
        return None

def get_train_info(start_city:str, destination_city:str):
    """The function should give the Train details such as start time, station names, end time of the journey
    Args:
         start_city is the starting station of the train.
         destination_city is the destination station of the train
         Chennai - Bemngaluru = Brindavan Express and Chennai - Hyderabad = Charminar Express"""
    if (start_city == "Chennai" and destination_city == "Bengaluru"):
        return "Brindavan Express"
    elif (start_city == "Bengaluru" and destination_city == "Chennai"):
        return "Brindavan Express"
    elif (start_city == "Hyderabad" and destination_city == "Chennai"):
        return "Charminar Express"
    elif (start_city == "Chennai" and destination_city == "Hyderabad"):
        return "Charminar Express"
    else:
        return None
    
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",generation_config=genai.GenerationConfig(
    temperature=0.7,
    top_p=0.95,
    top_k=64,
    response_mime_type='text/plain',
    max_output_tokens=8192,
),system_instruction=instruction, safety_settings=safety,tools=[start_city, destination_city, get_train_info])

print(model)

chat = model.start_chat(enable_automatic_function_calling=True,history=[])

prompt = "Tell me the start city which is located in Tamilnadu?"

response = chat.send_message(prompt,request_options={'retry':retry.Retry(predicate=retry.if_transient_error)})
print(response.text)

prompt1 = "Tell me the destination city which is located in Karnataka?"

response1 = chat.send_message(prompt1,request_options={'retry':retry.Retry(predicate=retry.if_transient_error)})
print(response1.text)

prompt2 = "Name of the train that goes from Chennai to Bengaluru?"

response2 = chat.send_message(prompt2,request_options={'retry':retry.Retry(predicate=retry.if_transient_error)})
print(response2.text)