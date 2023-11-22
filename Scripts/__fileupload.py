'''
    This file contains the file upload functionality for the dashboard page
'''
import streamlit as st
from Scripts import azsqldb, sessionvars, chatbot as cb
import os
import re
from dotenv import load_dotenv
"""
# Get the path to the directory one level up from where this script is located
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASEDIR = os.path.abspath(os.path.dirname(__file__))
# Load the variables from the .env file located at the topmost level
load_dotenv(os.path.join(BASEDIR, '.env'))
AZURE_AI_SEARCH_API_KEY = os.getenv('AZURE_AI_SEARCH_API_KEY')
AZURE_AI_SEARCH_ENDPOINT = os.getenv('AZURE_AI_SEARCH_ENDPOINT')
"""
sessionvars.initialize_session_vars()

def create_class_index():
    """
        Create the index for the class if it doesn't exist
    """
    # Replace spaces with dashes and convert to lowercase
    index_name = st.session_state.class_info['class_name'].replace(" ", "-").lower()

    # Replace all non-alphanumeric characters (except dashes) with empty strings
    index_name = re.sub(r'[^a-z0-9-]', '', index_name)

    # Remove leading and trailing dashes
    index_name = index_name.strip('-')    
    # Create the index in Azure Cognitive Search, and update the database
    cb.create_index(index_name)

    return index_name

#def vecotordb_upload():

def upload_file():
    if st.button("Upload File"):
        st.session_state.show_upload_file = not st.session_state.show_upload_file 

    if st.session_state.show_upload_file:
        pdf_docs = st.file_uploader("Upload your files here",
                         accept_multiple_files=True,
                         help="Only .pdf files only please",
                         type='pdf') 
        if st.button("Submit"):
            # Create the index if it doesn't exist
            if st.session_state.class_info['index_name'] is None:
                index_name = create_class_index()
                st.write(f"Created index {index_name}")
            