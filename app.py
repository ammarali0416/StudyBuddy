from Scripts import azsqldb
from Scripts import sessionvars
from Scripts import __login as lg
from Scripts import __sidebar as sb
from Scripts import __chatscreen as cs
from Scripts import azblob as azb
import streamlit as st
from markdownlit import mdlit
import pandas as pd

sessionvars.initialize_session_vars()

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
    
    # blob runs only after context has been selected
    if st.session_state.selected_modules not in [None, []]:
        col4, col5 = st.columns([1,1])

        col4.write(f"Chatting about: {st.session_state.selected_modules}")
        col5.write(f"Current session: {st.session_state.session_id}")
        
        azb.get_class_and_module_files('BUS5000')
        st.session_state.blobs_to_retrieve = st.session_state.blobs_df[st.session_state.blobs_df['module_name'].isin(st.session_state.selected_modules + ['CLASS_LEVEL'])]
        #########################
        #st.dataframe(st.session_state.blobs_to_retrieve)

        st.write(cs.initialize_chat())


