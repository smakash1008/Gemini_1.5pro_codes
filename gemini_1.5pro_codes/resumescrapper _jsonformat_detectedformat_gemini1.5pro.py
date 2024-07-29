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

# Uploading the File to the Gemini:

file_path = input("Enter the File Path: ") 

def upload_file_gemini(file_path):
    file = genai.upload_file(file_path)
    print(f"File Uploaded: {file.display_name} and File URI: {file.uri}")
    return file

file_uploaded = upload_file_gemini(file_path)
print(file_uploaded)

uploaded_file_name = file_uploaded.name
print(uploaded_file_name)

# Waiting If the File is Not Active:

def wait_for_active_file(file_uploaded):
    global file_get
    file_get = genai.get_file(uploaded_file_name)
    print(file_get)
    print(file_get.name, file_get.display_name)
    print(file_get.state.name)
    while file_get.state.name == 'PROCESSING':
        print("The file is still Processing.")
        time.sleep(20)
        file_get = genai.get_file(uploaded_file_name)
        print(file_get)
        print(file_get.name, file_get.display_name)
        print(file_get.state.name)
    if file_get.state.name != 'ACTIVE':
        raise Exception(f"File: {file_get.name} not processed till now.")
    

    return "The File is Active and it is ready for Data Scrapping..."

file_state = wait_for_active_file(file_uploaded)
print(file_state)

for file in genai.list_files():
    print(f"Name: {file.display_name} and Uri: {file.uri}")

# Getting the File Extension:

file_displayname = file_get.display_name
print(file_displayname)

def extract_file_extension(file_displayname):
    file_name_split = file_displayname.split(".",1)
    print(file_name_split)
    if len(file_name_split) == 2:
        file_extension = file_name_split[1]
        return file_extension
    else:
        return None
    
file_extension_extract = extract_file_extension(file_displayname)
print(file_extension_extract)

# Extracting the Text from the PDF Or Docx:

def extract_text_from_document(file_extension_extract):
    print(file_extension_extract)
    if file_extension_extract == 'docx':
        text = docx2txt.process(file_displayname)
        return text
    elif file_extension_extract == 'pdf':
        text = extract_text(file_displayname)
        return text
    else:
        return None
    
text = extract_text_from_document(file_extension_extract)
print(text)

# Configuring the Gemini Model:

instruction = "Behave like the best resume data scrapper and give the data which I needed only."

model = genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=genai.GenerationConfig(
    temperature=0.9,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
    response_mime_type='application/json',
),system_instruction=instruction)

input_prompt = """
Extract the following details mentioned in the below json pattern. If there is no data assign null only to the data that is not available in the text. Dont assign any unnecessary data that is not present in the above text extracted.
{
"Name":"<detected_name>",
"Email Address":"<detected_emailaddress>",
"Phone Number":"<detected_phonenumber>",
"Gender":"<detected_gender>",
"Marital Status":"<detected_maritalstatus>",
"Nationality":"<detected_nationality>",
"Langauges Known":["<detected_languages>"],
"Date of Birth":"<detected_dateofbirth>",
"Skills":["<detected_skills>"],
"Work Domain":["<detected_workdomain>"],
"Companies Worked":["<detected_companiesworked>"],
"Total Experience":"<detected_totalexperience>",
"Education Details":[
{
"Education Institution":"<detected_educationinstitution>",
"Education Course":"<detected_educationcourse>",
"Education Branch":"<detected_educationbranch>",
"Graducation Year":"<detected_graduationyear>",
"Exams Percentage":"<detected_examspercentage>"
}
],
"Courses and Certification":["<detected_coursesandcertification>"],
"Project Details":[
{
"Project Name":"<detected_projectname>",
"Project Description":"<detected_projectdescription>",
"Project Role":"<detected_Projectrole>",
"Project Domain":"<detected_Projectdomain>",
"Project Duration":"<detected_Projectduration>",
"Project Technologies":["<detected_Projecttechnologies>"]
}
]
}
Give the final data as like this indented pattern. The final data should not have \'n' characters in the Name, Email Address and Courses and Certification. The final data should be in the indent of 4. The Companies worked should not contain the Project Names. The Project Description should be summarized and should not exceed 2 lines. Dont assign anything if there is no Courses and Certifications in the text extracted. If there is no Project related section in the text extracted at that time dont assign anything. Dont skip any skills that is present in the text extracted. The work domain should be assigned from the text extracted only if the text extracted has the domain section. If there is no Work Domain section at that time assign most suitable only one domain from the text extracted. The work domain strictly should not contain skills name, tools name, technologies name and roles played in the companies. extract the work domain from the domain section only if it is present in the text extracted. If the text extracted has no domain section, at that time assign only one work domain. Dont skip any details regarding the education. If there is no value for any key, at that time assign NOT AVAILABLE. The work domain should not contain Roles played, tools, skills and technologies such as java, sql, python, Solution developer, Technical consultant etc. Dont change the order and pattern forever.
"""
text = text
input_prompt = input_prompt

prompt = """Text Extracted: {}

Input Prompt: {}""".format(text,input_prompt)

def response_text(prompt):
    response = model.generate_content(prompt,request_options={"retry": retry.Retry(predicate=retry.if_transient_error)})
    return response.text

details = response_text(prompt)
print(details)

dict_data = json.loads(details)
print(dict_data)

with open('finaldatajson.txt','w') as file:
    file.write(details)

print("Data Written Successfully...")

# Deleting the file from the Gemini:

def file_delete_from_gemini(file_uploaded):
    print(f"File To Be Deleted: {uploaded_file_name}")
    genai.delete_file(file_uploaded)

file_delete_from_gemini(file_uploaded)

try:
    genai.get_file(uploaded_file_name)
    print(f"File Name: {file_uploaded.display_name} still exists...")
    print(f"File State: {file_uploaded.state.name} and File Upload Name: {file_uploaded.name}")
except Exception:
    print(f"File Name: {file_uploaded.name} does not exists and deletion confirmed...")
finally:
    print("The Verification is done succesfully...")

print("File Deleted Successfully...")

for file in genai.list_files():
    print(f"Name: {file.display_name} and Uri: {file.uri}")