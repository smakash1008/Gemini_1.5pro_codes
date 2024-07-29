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

instruction = "Behave like the best AI and give th answers as per the user request."

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

prompt = """
Please choose the best explanation to the question:

Example 1:
Question: Why is sky blue?
Explanation1: The sky appears blue because of Rayleigh scattering, which causes shorter blue
wavelengths of light to be scattered more easily than longer red wavelengths, making the sky look
blue.
Explanation2: Due to Rayleigh scattering effect.
Answer: Explanation2

Example 2:
Question: What is the cause of earthquakes?
Explanation1: Sudden release of energy in the Earth's crust.
Explanation2: Earthquakes happen when tectonic plates suddenly slip or break apart, causing a
release of energy that creates seismic waves that can shake the ground and cause damage.
Answer: Explanation1

Question: How is snow formed?
Explanation1: Snow is formed when water vapor in the air freezes into ice crystals in the
atmosphere, which can combine and grow into snowflakes as they fall through the atmosphere and
accumulate on the ground.
Explanation2: Water vapor freezes into ice crystals forming snow.
Answer:

Give the answer based on the above 2 exmaples strictly. Give only the answers.
"""

def get_response(prompt):
    response = model.generate_content(prompt, request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
    return response.text

final_data = get_response(prompt)
print(final_data)