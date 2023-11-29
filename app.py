from Scripts import azsqldb, sessionvars, __login as lg, __sidebar as sb
import streamlit as st
from markdownlit import mdlit

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
    st.markdown(mdlit("""This is where the chat screen will be displayed."""))
    
    # Display the teacher sidebar
    if st.session_state.user_info['role']:
        sb.teacher_sidebar()  
    
