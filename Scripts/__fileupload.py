'''
    This file contains the file upload functionality for the dashboard page
'''
import os
import streamlit as st
from io import BytesIO
from dotenv import load_dotenv, find_dotenv
from Scripts import azsqldb, sessionvars, azblob as azb
from random import randint


load_dotenv(find_dotenv())

sessionvars.initialize_session_vars()

if st.session_state.user_info['role'] == 'teacher':
    help_text = 'Upload your class materials here!'
else:
    help_text = 'Upload your notes here!'

def upload_class_file():
    if st.session_state.show_upload_file:

        files = st.file_uploader("Upload files relevant to the class as a whole ie syllabus, schedule, etc",
                         accept_multiple_files=True,
                         help=help_text,
                         key = st.session_state.upload_key) 
        if st.button("Submit", key='class_upload_submit'):
            # Display a warning if the user hasn't uploaded a file
            if not files:                 
                st.warning("Please upload a file first!")
            else:
                with st.spinner("Uploading your files..."):
                    for file in files:
                        file_stream = BytesIO(file.getvalue())
                        blob_name = st.session_state.class_info['class_name'] + '/' + file.name
                        azb.upload_file_to_blob(file_stream, blob_name)
                    
                # Reset the file uploader widget
                st.session_state.upload_key = str(randint(1000, 1000000))

def upload_module_file():
    if st.button("Upload File"):
        st.session_state.show_upload_file2 = not st.session_state.show_upload_file2 

    if st.session_state.show_upload_file2:

        files = st.file_uploader("Upload files relevant to the lesson",
                         accept_multiple_files=True,
                         help=help_text,
                         key = st.session_state.upload_key_2) 
        if st.button("Submit"):
            # Display a warning if the user hasn't uploaded a file
            if not files:                 
                st.warning("Please upload a file first!")
            else:
                with st.spinner("Uploading your files..."):
                    for file in files:
                        file_stream = BytesIO(file.getvalue())
                        blob_name = st.session_state.class_info['class_name'] + '/' + file.name
                        azb.upload_file_to_blob(file_stream, blob_name)
                    
                # Reset the file uploader widget
                st.session_state.upload_key_2 = str(randint(1000, 1000000))