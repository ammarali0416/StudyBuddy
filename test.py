import openai
import os
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import TextLoader, PyPDFLoader
import streamlit as st

BASEDIR = os.path.abspath(os.path.dirname(__file__))

print(BASEDIR)
# Load the variables from the .env file located at the topmost level
load_dotenv(os.path.join(BASEDIR, '.env'))
AZURE_AI_SEARCH_API_KEY = os.getenv('AZURE_AI_SEARCH_API_KEY')
AZURE_AI_SEARCH_ENDPOINT = os.getenv('AZURE_AI_SEARCH_ENDPOINT')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize our embedding model
embeddings=OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,
                            model="text-embedding-ada-002",
                            chunk_size=1000)

index_name = 'test-index'

# Set our Azure Search
acs = AzureSearch(azure_search_endpoint=AZURE_AI_SEARCH_ENDPOINT,
                 azure_search_key=AZURE_AI_SEARCH_API_KEY,
                 index_name=index_name,
                 embedding_function=embeddings.embed_query)
