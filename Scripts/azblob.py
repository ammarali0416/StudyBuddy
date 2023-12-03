# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    azblob.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ammar syed ali <https://www.linkedin.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/30 18:45:03 by ammar syed        #+#    #+#              #
#    Updated: 2023/11/30 18:45:03 by ammar syed       ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
import streamlit as st
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceExistsError
from io import BytesIO
import os

load_dotenv(find_dotenv())

# Function to upload a file to Azure Blob Storage
def upload_file_to_blob(file, blob_name):
    try:
        # Create a blob service client
        blob_service_client = BlobServiceClient.from_connection_string(os.getenv("AZURE_STORAGE_CONNECTION_STRING"))

        # Create a blob client using the container name and blob name
        blob_client = blob_service_client.get_blob_client(container=os.getenv("AZURE_CONTAINER"), blob=blob_name)

        # Upload the file
        blob_client.upload_blob(file, blob_type="BlockBlob")

    except ResourceExistsError:
        # Ask the user whether to overwrite the file
        if st.button("The file already exists. Click here to overwrite it."):
            try:
                # Overwrite the file
                blob_client.upload_blob(file, blob_type="BlockBlob", overwrite=True)
                st.success("File overwritten successfully.")
            except Exception as e:
                st.error(f"Error occurred while overwriting file: {e}")
        elif st.button("Click here to keep the existing file."):
            st.info("File not overwritten.")
    except Exception as e:
        st.error(f"Error occurred while uploading file: {e}")


def get_class_and_module_files(class_name):
    '''
    Outputs a function that returns a dataframe of all files in the class and module folders
    '''
    # Retrieve environment variables
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER")

    # Initialize BlobServiceClient
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # List to store all blob paths
    all_blobs = []

    # Define the root folder for the class
    class_folder = f"{class_name}/"

    # Get all blobs within the class folder
    blobs = container_client.list_blobs(name_starts_with=class_folder)
    for blob in blobs:
        all_blobs.append(blob.name)

    # Initialize DataFrame
    df = pd.DataFrame(columns=['full_path', 'module_name', 'student_name'])

    # Process each file path
    for path in all_blobs:
        parts = path.split('/')
        module_name = parts[1] if len(parts) > 1 and "." not in parts[1] else None
        student_name = parts[3] if len(parts) > 3 and "STUDENT_NOTES" in parts else None
        if len(parts) > 1 and "." in parts[1]:
            module_name = "CLASS_LEVEL"
        df = pd.concat([df, pd.DataFrame({'full_path': path, 'module_name': module_name, 'student_name': student_name}, index=[0])], ignore_index=True)
    ## when a fileis a the class level make the module name CLASS_LEVEL
    ## filter the data fram checking the blob path for two 
    st.session_state.blobs_df = df