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

instruction = """Behave like a best data scrapper. Scrap the data by comparing with the pattern. Give the final data that matches with the pattern only."""

model = genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=genai.GenerationConfig(
    temperature=0.9,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
response_mime_type='application/json',),system_instruction=instruction,)


input_prompt = """
Extract the data and convert the extracted data based on the patterns present inside the <format : Patterns>. For others extract the data based on the <detected>. Dont skip any patterns that is present inside the <format : Patterns> especially for the Phone Numbers and Date of Birth. Give the consistent data all the time by comparing with the patterns for Date of Birth and Phone Number. The Exams CGPA, Exams Percentage, Total Experience and Gender should follow the pattern present inside <format : Patterns> strictly the output should come following the pattern only. Read the full prompt and give the final data correctly as per the patterns especially in the Exams CGPA.
{
"Name":"<detected_name>",
"Email Address":"<format : username@domain>",
"Phone Number":"<format : +XX XXXXXXXXXX>",
"Date Of Birth":"<format : DD/MM/YYYY>",
"Gender":"<format : ML|FL>",
"Nationality":"<detected_nationality>",
"Marital Status":"<detected_maritalstatus>",
"Languages":["<detected_languages>"],
"Skills":["<detected_skills>"],
"Domain":["<detected_domain>"],
"Total Experience":"<format : [0-9]{1,2}>",
"Companies Worked":["<detected_companies>"],
"Education Details":[
{
"Education Institution":"<detected_educationinstitution>",
"Education Course":"<detected_educationcourse>",
"Education Branch":"<detected_educationbranch>",
"Graduation Year":"<format : [0-9]{4}>",
"Exams Percentage":"<format : [0-9]{2}%>",
"Exams CGPA":"<format : [0-9]{1}>"
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
Follow the above formats and pattern strictly. The Phone number, date of birth, gender, total experience, exams percentage and exams cgpa should follow the patterns strictly present inside the <format : Patterns>. The final data should not be changed and it should have this pattern mentioned above. If there is no Projects present in the text extracted dont assign anything and simply assign Not Available. If there is no Courses and Certifications in the text extracted, at that time dont assign anything simply assign Not Available. The Companies Worked should not have Project Names and client names strictly in the final data. The Work Domain should not contain roles played, tools, skills such as java, python, html, roles ending with developer, consultant, lead, Engineer, etc. If there is no Work domain in the text extracted, at that time dont assign anything simply assign only one work domain that is most suitable and dont assign more than one Work Domain. The project should not have Reference and Project Responsibilities. The Project Description should be summarized and should not exceed more than 2 lines. The final data should have the above pattern and it should not change and it should have indent of 4. Assign Not Available for all the null values. The Project Name should not be empty or Not Available. Dont assign any unrelated and unnecessary data in the final data. If Exams Cgpa is present only the values only for that and if Exams Percentage is present put the values for that and dont put values for both at the same time. The final data should have all the details following the above patterns and all other patterns compulsorily without any fail. Dont assign anything on your own if there is no Projects in the text extracted. Dont assign unwanted and unnecessary details in Project Name in the final data. If there is no Nationality dont assign anything. The Project name should not be Not Available, empty or null always. The languages are not the programming language. Dont skip the Project Names if the Project is present in the text extracted strictly. Assign the correct Project name from the text extracted if it is present and dont assign any unwanted data on your own. The Project Name should not contain roles played such as those ending in tester, engineer, analyst, etc. Assign only the data present in the text extracted in the Project Details. The final data should contain only the necessary relevant data.
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

with open('finaljsonformat.txt','w') as newfile:
    newfile.write(details)

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