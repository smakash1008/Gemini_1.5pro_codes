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

result1 = genai.embed_content(
    model="models/text-embedding-004",
    content="Hello world",
)

result2 = genai.embed_content(
    model="models/text-embedding-004",
    content="Hello world",
    output_dimensionality=10,
)

print(str(result1['embedding']))
print(str(result2['embedding']))

print(str(result1['embedding'])[:50], '... TRIMMED]')

print(str(result2['embedding'])[:50], '... TRIMMED]')

print(len(result1['embedding']))
print(len(result2['embedding']))