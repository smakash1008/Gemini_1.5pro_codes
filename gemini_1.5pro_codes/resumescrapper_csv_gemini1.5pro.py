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

safety={
        'HATE': 'BLOCK_NONE',
        'HARASSMENT': 'BLOCK_NONE',
        'SEXUAL' : 'BLOCK_NONE',
        'DANGEROUS' : 'BLOCK_NONE',
    }

model = genai.GenerativeModel(model_name="gemini-1.5-pro",generation_config=genai.GenerationConfig(
    temperature=0.9,
    top_p=0.95,
    top_k=64,
    max_output_tokens=8192,
    response_mime_type='text/plain',
), system_instruction=instruction, safety_settings=safety,)

prompt = f"""
Text Extracted : {text}

Extract the Name, Email Address, Phone Number, Skills, Date of Birth, Gender, Marital Status, Nationality, Total Experience, Companies Worked, Work Domain, Educational Institution, Educational Course, Educational Branch, Graduation Year, Exams Percentage, Courses and Certifications, Project Names, Project Descriptions, Project Roles, Project Domain, Project Duration and Project Technologies, Languages Known from the text extracted. The final data should not contain unrelated data. It should have details that is present in the text extracted strictly and no unrelevant details should occur in the final data. If any data is not present, simply assign "NA" without thinking. If there is no details about Project Roles, Project Technologies, Project Domain, Project Duration in the text extracted, at that time simply assign "NA". Strictly no extra details should present in the Projects. Analyze the text extracted and assign properly with care. The Project details should not have references and responsibilities. The final data should be in the csv format. The Skills, Languages, Companies Worked, Work Domain, Educational Institution, Educational Course, Educational Branch, Graduation Year, Exams Percentage, Courses and Certifications, Project Names, Project Descriptions, Project Roles, Project Domains, Project Durations, Project Technologies should have list datatype strictly and compulsorily. The final order should be Name, Email Address, Phone Number, Skills, Date of Birth, Gender, Marital Status, Nationality, Total Experience, Companies Worked, Work Domain, Educational Institution, Educational Course, Educational Branch, Graduation Year, Exams Percentage, Courses and Certifications, Project Names, Project Descriptions, Project Roles, Project Domains, Project Durations, Project Technologies and Languages. The Companies worked should not contain the Project Names. The Project Description should be summarized and should not exceed more than 1 line. Dont assign anything if there is no Courses and Certifications in the text extracted. If there is no Project related section in the text extracted at that time dont assign anything. Dont skip any skills that is present in the text extracted. The work domain should be assigned from the text extracted only if the text extracted has the domain section and at that time dont skip those in that section. If there is no Work Domain section at that time assign most suitable only one domain from the text extracted. The work domain strictly should not contain skills name, tools name, technologies name and roles played in the companies such as java, sql, python, solution developer, technical consultant, software developer, etc. extract the work domain from the domain section only if it is present in the text extracted. If the text extracted has no domain section, at that time assign only one work domain on your own but not more than one and it should be relevant. The project roles should have only the roles played in the projects and it should not exceed 6 words. Dont skip any details regarding the education. If there is no value, at that time assign "NA" at that place. The work domain should not contain Roles played, tools, skills and technologies such as java, sql, python, Solution developer, Technical consultant etc. Dont change the order and pattern forever. Inside the list if there is empty value assign "NA" at that place. Dont skip the total experience. Dont assign any unrelated data strictly. Strictly The double quotes are allowed inside the list and not allowed outside the list datatype because list is important for multiple value never skip list datatype. Remove the new line characters present in the name, email address, Courses and Certifications, Project Descriptions. Strictly dont consider the list datatypes as string and dont enclose list in the double quotes at any cost. All the values other than list should be enclosed within double quotes. The header is very important so the first row should contain the header and second row should contain the value in the csv format. The Project Technologies should have list of list datatypes. All the list datatypes and list of list datatypes should end properly. Dont skip the list and list of list datatypes for multiple values strictly. Dont change the order and pattern. Follow all the commands in the prompt strictly. Dont skip any work domain if the domain section is present in the text extracted strictly and give the proper relevant. All the "NA" should have double quotes compulsorily.  All the string and "NA" datas should be enclosed with proper double quotes. Dont skip any education details strictly all the education details needs to be present in the final data without fail. Dont take any work domain from the Projects strictly. The final data should not have any extra symbols strictly. The work domain should not contain details ending in developer, consultant, analyst, program etc and give the revelant and suitable work domain only. Dont forget the list and list of list types. The Project duration can be present in the format of days also. The final data should follow the order and pattern compulsorily and it should display the data consistently. The Project Technologies should have list of list datatype like this [["data"],["data"]]. If the list of list datatype has pattern this [["data"],["data"]]] and simply remove the extra last square braces ']' and give the format as [["data"],["data"]]. Dont iterate the data, Give all the details only once. Each list should contain all the details of the same time. The languages known does not include the Programming languages. The languages means people speaking languages. Dont change the order strictly and give all the details in the final data without fail. If the work domain section is present in the text extracted, take all the work domain and if the section itself not present assign only one related domain from the text extracted. If the list is empty put "NA" in the list. 
"""


def response_text(prompt):
    response = model.generate_content(prompt,request_options={"retry": retry.Retry(predicate=retry.if_transient_error)})
    return response.text

details = response_text(prompt)
print(details)


with open('csvdata.csv','w') as newfile:
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