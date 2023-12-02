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


# Streamlit UI to upload files
def main():
    st.title("Upload Files to Azure Blob Storage")

    # Connection string and container name (ensure these are secure and not hard-coded in production)
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    container_name = os.getenv("AZURE_CONTAINER")

    # File uploader widget
    uploaded_files = st.file_uploader('file_uplaods', accept_multiple_files=True, label_visibility='hidden')

    if st.button("Submit"):
        # Handle file upload
        if uploaded_files:
            for uploaded_file in uploaded_files:
                # Create a file-like object
                file_stream = BytesIO(uploaded_file.getvalue())
                blob_name = 'test/' + uploaded_file.name
                # Call the upload function
                upload_file_to_blob(file_stream, container_name, blob_name, connection_string)
                st.success(f"Uploaded {blob_name}")

if __name__ == "__main__":
    main()