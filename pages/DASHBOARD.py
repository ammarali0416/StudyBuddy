import streamlit as st
import pandas as pd
from Scripts import azsqldb, sessionvars, __sidebar as sb, __faqs as fq

sessionvars.initialize_session_vars()

def main():
    # Check if the user is logged in or not
    if not st.session_state.user_info['user_id']:
        st.title("Dashboard")
        st.warning('Please sign in first!')
    else:
        st.title(f"{st.session_state.user_info['username']}'s Dashboard")
        if st.session_state.user_info['role'] == 'teacher':
            sb.teacher_sidebar()
            st.write("""
                Here's a quick guide to the buttons you'll find on this page: 
                - **FAQ**: View and answer students' questions. 🎓
                - **Schedule**: Use this to view and manage the class schedule. 🗓️
                - **Upload Files**: Upload class materials, assignments, and other resources. 📚
            """)
            # Display the faq button
            fq.teacher_faqs()
        
        else:
            sb.student_sidebar()
            st.write("""
                Here's a quick guide to the buttons you'll find on this page: 
                - **FAQ**: View FAQs or ask a new one. 🎓
                - **Schedule**: Use this to view and manage the class schedule. 🗓️
                - **Upload Files**: Upload your notes, outlines, etc. 📚
            """)
            # Student FAQs
            fq.student_faqs()


if __name__ == "__main__":
    main()
