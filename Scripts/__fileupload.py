'''
    This file contains the file upload functionality for the dashboard page
'''
import openai
import os
import re
import streamlit as st
from io import BytesIO
from typing import Tuple, List
from dotenv import load_dotenv
from Scripts import azsqldb, sessionvars
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(BASEDIR, '.env'))


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
    # Initialize our embedding model
    embeddings=OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'),
                                model="text-embedding-ada-002",
                                chunk_size=1000)
    # Set our Azure Search
    acs = AzureSearch(azure_search_endpoint=os.getenv('AZURE_AI_SEARCH_ENDPOINT'),
                    azure_search_key=os.getenv('AZURE_AI_SEARCH_API_KEY'),
                    index_name=index_name,
                    embedding_function=embeddings.embed_query)
    # Update the database with the new class index name
    azsqldb.update_class(st.session_state.sqlcursor, 
                         st.session_state.class_info['class_id'], 
                        'index_name',
                         index_name)
    st.session_state.class_info['index_name'] = index_name

    return index_name

def parse_pdf(file, filename: str) -> Tuple[List[str], str]:
    pdf = PdfReader(file)
    output = []
    for page in pdf.pages:
        text = page.extract_text()
        text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
        text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
        text = re.sub(r"\n\s*\n", "\n\n", text)
        output.append(text)
    return output, filename

def text_to_docs(text: List[str], filename: str) -> List[Document]:
    if isinstance(text, str):
        text = [text]
    page_docs = [Document(page_content=page) for page in text]
    for i, doc in enumerate(page_docs):
        doc.metadata["page"] = i + 1

    doc_chunks = []
    for doc in page_docs:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
            chunk_overlap=0,
        )
        chunks = text_splitter.split_text(doc.page_content)
        for i, chunk in enumerate(chunks):
            doc = Document(
                page_content=chunk, metadata={"page": doc.metadata["page"], "chunk": i}
            )
            doc.metadata["source"] = f"{doc.metadata['page']}-{doc.metadata['chunk']}"
            doc.metadata["filename"] = filename  # Add filename to metadata
            doc_chunks.append(doc)
    return doc_chunks

def upload_file():
    if st.button("Upload File"):
        st.session_state.show_upload_file = not st.session_state.show_upload_file 

    if st.session_state.show_upload_file:
        pdf_files = st.file_uploader("Upload your files here",
                         accept_multiple_files=True,
                         help="Only .pdf files only please",
                         type='pdf') 
        if st.button("Submit"):
            # Display a warning if the user hasn't uploaded a file
            if not pdf_files:                 
                st.warning("Please upload a file first!")
            
            with st.spinner("Uploading your files..."):
                pdf_names = [file.name for file in pdf_files] # get the names for each file
                
                # Create the index if it doesn't exist
                if st.session_state.class_info['index_name'] is None:
                    index_name = create_class_index()

                # Upload the document to Azure Cognitive Search
                #1 Parse the PDF
                documents = []
                for pdf_file, pdf_name in zip(pdf_files, pdf_names):
                    text, filename = parse_pdf(pdf_file, pdf_name)
                    documents = documents + text_to_docs(text, filename)
                    st.write(f"Here is the documents: {documents}")
                #2 Upload the documents to Azure Cognitive Search
                embeddings=OpenAIEmbeddings(openai_api_key=os.getenv('OPENAI_API_KEY'),
                                model="text-embedding-ada-002",
                                chunk_size=1000)

                acs = AzureSearch(azure_search_endpoint=os.getenv('AZURE_AI_SEARCH_ENDPOINT'),
                    azure_search_key=os.getenv('AZURE_AI_SEARCH_API_KEY'),
                    index_name=st.session_state.class_info['index_name'],
                    embedding_function=embeddings.embed_query)
                
                acs.add_documents(documents=documents)

                