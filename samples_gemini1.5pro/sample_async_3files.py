# Importing the Necessary Libraries:

import json
import os
import time
import re
import docx2txt
import google.generativeai as genai
import pdfminer
from pdfminer.high_level import extract_text
from google.api_core import retry_async
from dotenv import load_dotenv
load_dotenv()
import asyncio
import tracemalloc

tracemalloc.start()

# Configuring the Gemini API:

genai.configure(api_key=os.getenv("GOOGLE_API_KEY1"))

instruction = "Behave like the best story teller. The stories should be understandable by all those who sees it. Give the story as per the user request in the prompt and the story should have more than 3000 words. Give the moral for each story."

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

async def get_response():
    async for chunk in await model.generate_content_async("Tell me a story about Cholas", stream=True, request_options={'retry': retry_async.AsyncRetry(predicate=retry_async.if_transient_error)}):
        if chunk.text:
            print(chunk.text)
        print("#"*100)

async def get_response1():
    async for chunk in await model.generate_content_async("Tell me a story about Pandyas", stream=True, request_options={'retry' : retry_async.AsyncRetry(predicate=retry_async.if_transient_error)}):
        if chunk.text:
            print(chunk.text)
        print("$"*100)

async def get_response2():
    async for chunk in await model.generate_content_async("Tell me a story about Pallavas", stream=True, request_options={'retry' : retry_async.AsyncRetry(predicate=retry_async.if_transient_error)}):
        if chunk.text:
            print(chunk.text)
        print("-"*100)

async def gather_response():
    task1 = asyncio.create_task(get_response())
    task2 = asyncio.create_task(get_response1())
    task3 = asyncio.create_task(get_response2())
    await asyncio.gather(task1, task2, task3)

asyncio.run(gather_response())