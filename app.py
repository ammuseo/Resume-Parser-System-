import csv
import os
import streamlit as st
import nltk
import nltk.tokenizers
import docx2txt
import pandas as pd
import sys
import re
import subprocess
from pdfminer.high_level import extract_text
import requests
from pathlib import Path

### Main fumction
def main():
    
    st.title("Resume Parser")
    menu=["Home","Upload the file", "Browse the file", "About"]
    choice=st.sidebar.selectbox("Menu", menu)

    ##### HOME
    if choice=="Home":
        st.subheader("Welcome to my project. This is resume parser. Please select anyone option on sidebar")
    #####UPLoad the File
    elif choice=="Upload the file":
        st.subheader("Upload the file")
        doc_file=st.file_uploader("Upload a Document", type=["pdf", "docx"])
        if st.button("Upload"):
            if doc_file is not None:
                # Save uploaded file to 'F:/tmp' folder.
                save_folder = 'C:/Users/amuth/OneDrive/ammu/AI-course/mentornessproject/resumeparser/ResumeParsing/resumes'
                save_path = Path(save_folder, doc_file.name)
                with open(save_path, mode='wb') as w:
                    w.write(doc_file.getvalue())

                if save_path.exists():
                    st.success(f'File {doc_file.name} is successfully saved!')
    #### Browse the file            
    elif choice=="Browse the file":
        #extracting from pdf
        def extract_text_from_pdf(pdf_path):
            return extract_text(pdf_path)
        def extract_text_from_docx(docx_path):
            txt=docx2txt.process(docx_path)
            if txt:
                return txt.replace('\t', ' ')
            return None
        #extracting the names from the tet
        def extract_names(txt):
            person_name=[]
            for sent in nltk.sent_tokenize(txt):
                for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                    if hasattr(chunk, 'label') and chunk.label()=='PERSON':
                        person_name.append(
                            ' '.join(chunk_leave[0] for chunk_leave in chunk.leaves())                   
                            )
            return person_name
        #extracting the phone number
        PHONE_REG=re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]')
        phone=[]
        def extract_phone_number(resume_txt):
            number=PHONE_REG.findall(resume_txt)
            phone.extend(number)
            if phone:
                for num in phone:
            
        ##number=' '.join(phone[0]) ###https://blog.apilayer.com/build-your-own-resume-parser-using-python-and-nlp/
        ##if resume_txt.find(number) >= 0 and len(number) < 16:
                    return num
                return None

        def file_selected(folder_path=r'C:/Users/amuth/OneDrive/ammu/AI-course/mentornessproject/resumeparser/ResumeParsing/resumes'):
            files=[]
            filenames=os.listdir(folder_path)
            files = ["select"] + filenames

            selected_filename=st.selectbox('Select a File', options=list(files))
            
            return os.path.join(folder_path, selected_filename)
        filename=file_selected()
        if filename=="C:/Users/amuth/OneDrive/ammu/AI-course/mentornessproject/resumeparser/ResumeParsing/resumes\select":
            st.write("")
        else:
            st.write("you selected '%s'" % os.path.basename(filename))

        ##file path
        def doc_to_text_catdoc(file_path):
            try:
                process=subprocess.Popen(
                    ['catdoc', '-w', file_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True,
                )
            except(
            FileNotFoundError,
            ValueError,
            subprocess.TimeoutExpired,
            subprocess.SubprocessError,
            
            ) as err:
                return (None, str(err))
            else:
                stdout, stderr=process.communicate()
            return (stdout.strip(), stderr.strip())
        ## end of filepath
        #extracting email address
        EMAIL_REG=re.compile(r'[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+')
        def extract_emails(resume_txt):
            return re.findall(EMAIL_REG, resume_txt)
        if filename.endswith(''):
            text="select"
        if filename.endswith('.pdf'):
            text=extract_text_from_pdf(filename)
        if filename.endswith('.docx'):
            text=extract_text_from_docx(filename)  # noqa: T001
    ##text, err = doc_to_text_catdoc('./resume-word.doc')
        ## poit
        if text=="select":
            st.write("Please select the file")
        else:
            names=extract_names(text)
            emails=extract_emails(text)
            phone_number=extract_phone_number(text)
            firstname=names[0]
            lastname=names[1]
            ##st.write(firstname + ' ' + lastname)
            st.write(firstname)
            lname=lastname.split(" ")
            st.write(lname[0])
            csv_file=open(r'C:/Users/amuth/OneDrive/ammu/AI-course/mentornessproject/resumeparser/ResumeParsing/Contact_information.csv', 'a', newline='')
            csv_data=csv.writer(csv_file, delimiter=',')
            csv_data.writerow([firstname + ' ' + lname[0],  phone_number,  emails[0]])
            csv_file.close()
            if names:
                print(f"Name: {firstname + ' ' + lname[0]}")   
                print(f"Phone Number: {phone_number}")
            if emails:
                print(f"Email: {emails[0]}")
            df=pd.read_csv(r'C:\Users\amuth\OneDrive\ammu\AI-course\mentornessproject\resumeparser\ResumeParsing\Contact_information.csv')
            st.dataframe(df)
       #### end of read.py/
        ##st.write("browse")
    else:
    ### About us    
        st.subheader("About This Project \n Resume Parser\n Thanks for visit")

    
    

## page load        
if __name__=='__main__':
    main()
os.system('clear') 
    