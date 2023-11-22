# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    azsearch.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ammar syed ali <https://www.linkedin.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/21 19:06:56 by ammar syed        #+#    #+#              #
#    Updated: 2023/11/21 19:06:56 by ammar syed       ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

'''
Script to contain all functions related to Azure Cognitive Search
'''
import openai
import os
from Scripts import azsqldb, sessionvars
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.azuresearch import AzureSearch
import streamlit as st

# Get the path to the directory one level up from where this script is located
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# Load the .env file
load_dotenv(os.path.join(BASEDIR, '.env'))

def create_index(index_name):
    '''
        Create an index in Azure Cognitive Search, and update the database
    '''
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

