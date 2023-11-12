import streamlit as st
import azsqldb

class_list = azsqldb.get_classes(st.session_state.user_id, st.session_state.role, st.session_state.sqlcursor)

st.title("Dashboard")

# Check if the user is logged in or not
if st.session_state.user_id == None:
    st.warning('Please sign in first!')
else:
    # Determine what title to show based on the role
    if st.session_state.role == 'teacher':
        selected_action = st.selectbox("Select an action:", ["Add Class", "Select Class"])
        if selected_action == 'Select Class':
            selected_class = st.selectbox("Classes:", class_list)
    else:
        selected_action = st.selectbox("Select class:", class_list)
