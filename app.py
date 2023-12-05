from Scripts import azsqldb
from Scripts import sessionvars
from Scripts import __login as lg
from Scripts import __sidebar as sb
from Scripts import __chatscreen as cs
from Scripts import azblob as azb
import streamlit as st
from markdownlit import mdlit
import pandas as pd
import os
import time
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

sessionvars.initialize_session_vars()


if st.session_state.cleanup == False:
    print("Cleaning up files from OpenAI")
    cs.delete_files_from_openai()
    print("DONE")
    st.session_state.cleanup = True

custom_width = 250

# Assuming the image is in the same directory as your script
logo_path = 'StudyBuddyLogo.png'

col1, col2, col3 = st.columns([1,1,1])


# Display the logo at the top of the page
with col2:
    st.image(logo_path, width= custom_width)

st.subheader("An Intelligent Education App", )
# Display the login container
# This block defining what the app does when the user_id value is equal to None
if not st.session_state.user_info['user_id']:
    lg.LoginContainer()
    with st.sidebar:
        st.warning("Please sign in first!")
    if st.session_state.user_info['user_id']:
        st.experimental_rerun()


# If the user is logged in, display the chat screen
if st.session_state.user_info['user_id']:    
    # Display the teacher sidebar
    if st.session_state.user_info['role'] == 'teacher':
        sb.teacher_sidebar()  
    else:
        sb.student_sidebar()
    
    # Display the chat screen
    if st.session_state.context_selection_toggle:
        cs.context_selection()
    
    # block runs only after context has been selected
    if st.session_state.selected_modules not in [None, []]:
        col4, col5 = st.columns([1,1])

        col4.write(f"Chatting about: {st.session_state.selected_modules}")
        col5.write(f"Current session: {st.session_state.session_id}")
        
        # Get all the class and module files
        azb.get_class_and_module_files(st.session_state.class_info['class_name'])
        # Retrieve only the selected modules' files
        st.session_state.blobs_to_retrieve = st.session_state.blobs_df[st.session_state.blobs_df['module_name'].isin(st.session_state.selected_modules + ['CLASS_LEVEL'])]
        #########################
        #st.dataframe(st.session_state.blobs_to_retrieve)
        # Store the openai file ids of all the files uploaded to the assistant
        if st.session_state.uploaded_to_openai == False: # To ensure this only happens once
            st.session_state.openai_fileids = cs.upload_files_ai(st.session_state.blobs_to_retrieve['full_path'])
            st.session_state.uploaded_to_openai = True
        # Initialize the assistant
        if "studybuddy" not in st.session_state:
            st.session_state.studybuddy = st.session_state.ai_client.beta.assistants.retrieve(os.getenv('OPENAI_ASSISTANT'))
            st.session_state.studybuddy = st.session_state.ai_client.beta.assistants.update(
                assistant_id=st.session_state.studybuddy.id,
                file_ids=st.session_state.openai_fileids
            )
            # Create a new thread for this session
            st.session_state.thread = st.session_state.ai_client.beta.threads.create(
                metadata={
                    'session_id': st.session_state.session_id,
                }
            )
        # If the run is completed, display the messages
        elif hasattr(st.session_state.run, 'status') and st.session_state.run.status == "completed":
            # Retrieve the list of messages
            st.session_state.messages = st.session_state.ai_client.beta.threads.messages.list(
                thread_id=st.session_state.thread.id
            )
        # Display sources
            for thread_message in st.session_state.messages.data:
                for message_content in thread_message.content:
                    # Access the actual text content
                    message_content = message_content.text
                    annotations = message_content.annotations
                    citations = []
                    
                    # Iterate over the annotations and add footnotes
                    for index, annotation in enumerate(annotations):
                        # Replace the text with a footnote
                        message_content.value = message_content.value.replace(annotation.text, f' [{index}]')
                    
                        # Gather citations based on annotation attributes
                        if (file_citation := getattr(annotation, 'file_citation', None)):
                            cited_file = st.session_state.ai_client.files.retrieve(file_citation.file_id)
                            citations.append(f'[{index}] {file_citation.quote} from {cited_file.filename}')
                        elif (file_path := getattr(annotation, 'file_path', None)):
                            cited_file = st.session_state.ai_client.files.retrieve(file_path.file_id)
                            citations.append(f'[{index}] Click <here> to download {cited_file.filename}')
                            # Note: File download functionality not implemented above for brevity

                    # Add footnotes to the end of the message before displaying to user
                    message_content.value += '\n' + '\n'.join(citations)
        # Display messages
            for message in reversed(st.session_state.messages.data):
                if message.role in ["user", "assistant"]:
                    for content_part in message.content:
                        message_text = content_part.text.value
                        # Check if the message contains the specified phrase
                        if "<INFO> INITIAL PROMPT </INFO>" not in message_text:
                            with st.chat_message(message.role):
                                st.markdown(message_text)
                        else:
                            # Optionally, you can print a message to the console for debugging
                            print("Skipped a message containing the initial prompt info.")
        
        if st.session_state.initialized == False:
            prompt = cs.initialize_chat()
            st.session_state.initialized = True
        else:
            prompt = st.chat_input("How can I help you?")

        if prompt:
            with st.chat_message('user'):
                st.write(prompt)

            # Add message to the thread
            st.session_state.messages = st.session_state.ai_client.beta.threads.messages.create(
                thread_id=st.session_state.thread.id,
                role="user",
                content=prompt
            )
        # Do a run to process the messages in the thread
            st.session_state.run = st.session_state.ai_client.beta.threads.runs.create(
                thread_id=st.session_state.thread.id,
                assistant_id=st.session_state.studybuddy.id,
            )
            print(f"Current run id: {st.session_state.run.id}")
            if st.session_state.retry_error < 3:
                time.sleep(1) # Wait 1 second before checking run status
                st.rerun()
        # Check if 'run' object has 'status' attribute
        if hasattr(st.session_state.run, 'status'):
            # Handle the 'running' status
            if st.session_state.run.status == "running":
                with st.chat_message('assistant'):
                    st.write("Thinking ......")
                if st.session_state.retry_error < 3:
                    time.sleep(5)  # Short delay to prevent immediate rerun, adjust as needed
                    st.rerun()

            # Handle the 'failed' status
            elif st.session_state.run.status == "failed":
                st.session_state.retry_error += 1
                with st.chat_message('assistant'):
                    if st.session_state.retry_error < 3:
                        st.write("Run failed, retrying ......")
                        time.sleep(5)  # Longer delay before retrying
                        st.rerun()
                    else:
                        st.error("FAILED: The OpenAI API is currently processing too many requests. Please try again later ......")

            # Handle any status that is not 'completed'
            elif st.session_state.run.status != "completed":
                print("""# Handle any status that is not 'completed'
            elif st.session_state.run.status != "completed":""")
                print(f"Current run status: {st.session_state.run.status}")
                print(f"Current run id: {st.session_state.run.id}")
                # Attempt to retrieve the run again, possibly redundant if there's no other status but 'running' or 'failed'
                st.session_state.run = st.session_state.ai_client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread.id,
                    run_id=st.session_state.run.id,
                )
                if st.session_state.retry_error < 3:
                    time.sleep(3)
                    st.rerun()