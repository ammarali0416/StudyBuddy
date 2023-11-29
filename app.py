from Scripts import azsqldb, sessionvars, __login as lg
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
while not st.session_state.user_info['user_id']:
    lg.LoginContainer()