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
    help_text = 'Any files, like notes or outlines'

def upload_class_file():
    files = st.file_uploader("Upload files relevant to the class as a whole ie syllabus, schedule, etc",
                        accept_multiple_files=True,
                        help=help_text,
                        key = st.session_state.upload_key) 
    if st.button("Submit", key='class_upload_submit', use_container_width=True):
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
            st.session_state.upload_key = str(randint(0, 1000000))
            st.rerun()

def upload_module_file():
    files = st.file_uploader("Upload files your files for this module",
                        accept_multiple_files=True,
                        help=help_text,
                        key = "fufuf" + st.session_state.upload_key_2) 
    if st.button("Submit", use_container_width=True):
        # Display a warning if the user hasn't uploaded a file
        if not files:                 
            st.warning("Please upload a file first!")
        else:
            with st.spinner("Uploading your files..."):
                for file in files:
                    file_stream = BytesIO(file.getvalue())
                    if st.session_state.user_info['role'] == 'teacher': 
                        blob_name = st.session_state.class_info['class_name'] + '/' + st.session_state.selected_module_name + '/' + file.name
                    else:
                        blob_name = st.session_state.class_info['class_name'] + '/' + st.session_state.selected_module_name + '/STUDENT_NOTES/' + st.session_state.user_info['username'] + '/' + file.name
                    azb.upload_file_to_blob(file_stream, blob_name)
                
            # Reset the file uploader widget
                st.session_state.upload_key_2 = str(randint(1000001, 10000000))
                st.rerun()
