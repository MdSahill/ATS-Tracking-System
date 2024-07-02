import streamlit as st
import google.generativeai as genai
import pdf2image
import os
from dotenv import load_dotenv
load_dotenv()
import base64
import io
from PIL import Image
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generative_ai_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(upload_file):
    if upload_file is not None:
        ## COnvert pdf to image
        file_bytes = upload_file.read()

        images=pdf2image.convert_from_bytes(file_bytes)
        
        first_page=images[0]

        ##Convert to bytes
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr,format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()

        pdf_parts = [
            {
            "mime_type":"image/jpeg",
            "data":base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##Streamlit app

st.set_page_config(page_title='ATS Rsume Expert')
st.header("ATS Tracking System")
input_text=st.text_area("Job Description",key="input")
uploaded_file=st.file_uploader("Upload your resume in pdf",type=["pdf"])

if uploaded_file is not None:
    st.write("Resume uploaded Successfully")

submit1=st.button("Tell me about the Resume")

submit2=st.button("Percentage Match")

input_prompt1="""
  You are an experienced Technical Human Resource Manager .your task is to review the provided resume against the job description.
  Please share your professional evaluation on whether the condidate's profile allign with the role.
  Highlight the strengths and weakness of the applicant in relation to the specified job requirements.
    """

input_prompt2="""
    You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
    your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
    the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=generative_ai_response(input_prompt1,pdf_content,input_text)
        st.write(response)
    else:
        st.write("Please upload your resume")

if submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=generative_ai_response(input_prompt2,pdf_content,input_text)
        st.write(response)
    else:
        st.write("Please upload your resume")