import streamlit as st

st.title("Dashboard")

# Check if the user is logged in or not
if st.session_state.user_id == None:
    st.warning('Please sign in first!')
else:
    # Determine what title to show based on the role
    if st.session_state.role == 'teacher':
        st.subheader("Get ready to be empowered!")
    else:
        st.subheader("Get ready to learn!")