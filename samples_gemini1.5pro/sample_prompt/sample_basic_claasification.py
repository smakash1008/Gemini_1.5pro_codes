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

classification_system= """

As a social media moderation system, your task is to categorize user comments under a post.
Analyze the comment related to the topic and classify it into one of the following categories:

Abusive
Spam
Offensive

If the comment does not fit any of the above categories, classify it as: Neutral.

Provide only the category as a response without explanations.

Topic: What can I do after highschool?
Comment: You should do a gap year!
Class: Neutral

Topic: Where can I buy a cheap phone?
Comment: You have just won an IPhone 15 Pro Max!!! Click the link to receive the prize!!!
Class: Spam

Topic: How long do you boil eggs?
Comment: Are you stupid?
Class: Offensive

Topic : My computer froze. What should I do?
Comment: Try turning it off and on.
Class: 

Topic: I am looking for a vet in our neighbourhood. Can anyone reccomend someone good? Thanks.
Comment: You can win 1000$ by just following me!
Class:
"""

response = model.generate_content(classification_system, request_options={'retry' : retry.Retry(predicate=retry.if_transient_error)})
print(response.text)
