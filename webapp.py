import google.generativeai as genai
import os   
import streamlit as st
from pdfextractor import text_extractor_pdf
from docxextractor import text_extractor_docx
from imageextractor import extract_text_from_image


#configure the Model
key=os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=key)
model=genai.GenerativeModel('gemini-2.5-flash-lite')


#upload file in sidebar
user_text=None
st.sidebar.title(':blue[Upload Your MOM Notes Here]')
st.sidebar.subheader('Supported formats: pdf, docx, png, jpg, jpeg.')
user_file=st.sidebar.file_uploader("Upload your file",type=['pdf','docx','png','jpg','jpeg'])
if user_file:
    if user_file.type=='application/pdf':
     user_text=text_extractor_pdf(user_file)
    elif user_file.type=='application/vnd.openxmlformats-officedocument.wordprocessingml.document':
     user_text=text_extractor_docx(user_file)
    elif user_file.type in ['image/png','image/jpg','image/jpeg']:
     user_text=extract_text_from_image(user_file)
    else:
      st.sidebar.write('upload correct file format')

#Main Page
st.title(':green[Minutes Of Meeting Generator] : :yellow[AI assisted MOM generator in a Standardized format From Meeting Notes]')
tips='''Tips tp use this app:
* upload your meeting in side bar (image,PDF,DOCX)
* Click on Generate MOM and get the standardized MOM'S.'''
st.write(tips)


if st.button('Generate MOM'):
   if user_text is None:
     st.error('Text is not generated')
   else:
    with st.spinner('Generating MOM...'):
      prompt=f'''Assume you are an expert in creating minuties of metting .User has provided notes of meetingin text format.Using this data create a standarized minuties for the user.
      Keep the format as mentioned below and use bullet points where ever necessary.

      Output must follow word/docx format,strictly in the following manner
      Title:Title of the meeting
      Heading:Meeting Agenda
      Subheading:Name of attendees
      subheading:date of meeting and place of meeting (place means name of conference/meeting room if  not provided  keep it online)
      Body:The body must follow the following sequence of points 
      * Key points discussed
      * Highlight any decision that has been finalised.
      * Mention actionable items.
      * Any deadline that has been discussed.
      * Any next meeting date that has been discussed
      * 2 to 3 line of summary.
      * Use bullet points where ever necessary or bold important keywords such the context is clear.
      * Generate the output in such a way that it can be copied and paste in word 
      
       The data provided by user is as follows {user_text}.'''
      
      response=model.generate_content([prompt])
      st.write(response.text)

      st.download_button(label='Click to Download MOM',data=response.text,file_name='MOM.txt',mime='text/plain')
