# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __sidebar.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ammar syed ali <https://www.linkedin.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/19 14:14:18 by ammar syed        #+#    #+#              #
#    Updated: 2023/11/19 14:14:18 by ammar syed       ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

'''
    This file contains the sidebar for the dashboard page
'''
import streamlit as st
from Scripts import azsqldb, sessionvars, __faqs as fq, __fileupload as fu, __schedule as sc, __classmanager as cm, __modules as md

sessionvars.initialize_session_vars()

def teacher_sidebar():   
    # Sidebar for class selection and new class creation
    with st.sidebar:
        st.write("""
                Here's a quick guide to the buttons you'll find on this page: 
                - **FAQ**: View and answer students' questions. 🎓
                - **Schedule**: Use this to view and manage the class schedule. 🗓️
                - **Upload Files**: Upload class materials, assignments, and other resources. 📚
            """)
        ## Class management
        st.sidebar.title("Class")
        cm.show_class()

        col1, col2 = st.columns([1,1])

        with col1:
            # Button to create a new class
            if st.button("Create a new class"):
                st.session_state.show_new_class_input = not st.session_state.show_new_class_input
                st.session_state.show_upload_file = False

        with col2:
            # Button to upload class level files
            if st.button("Upload File", key='class_upload'):
                st.session_state.show_upload_file = not st.session_state.show_upload_file ## Upload class files
                st.session_state.show_new_class_input = False

        
        # Block to create a new class
        if st.session_state.show_new_class_input:
            cm.create_new_class()

        # Block to upload class level files
        if st.session_state.show_upload_file:
            fu.upload_class_file()

        ####################################
        #  Module management
        st.sidebar.title("Modules")
        md.show_module()

        col3, col4, col5 = st.columns([1,1,1])
        
        with col3:
            if st.button("Create a new module"):
                st.session_state.new_module_toggle = not st.session_state.new_module_toggle
                st.session_state.delete_module_toggle = False
                st.session_state.show_upload_file2 = False
    
        with col4:  
            if st.button("Delete a module"):
                st.session_state.delete_module_toggle = not st.session_state.delete_module_toggle
                st.session_state.new_module_toggle = False
                st.session_state.show_upload_file2 = False

        with col5:
            if st.button("Upload File", key='module_upload'):
                st.session_state.show_upload_file2 = not st.session_state.show_upload_file2
                st.session_state.new_module_toggle = False
                st.session_state.delete_module_toggle = False

        if st.session_state.new_module_toggle:
            md.create_new_module()
        
        if st.session_state.delete_module_toggle:
            md.delete_module()
        
        if st.session_state.show_upload_file2:
            fu.upload_module_file()

        ####################################
        ### Faq functions
        st.sidebar.title("FAQs")
        fq.teacher_faqs()

        #schedule
        st.sidebar.title("Manage Assignments")
        sc.teacher_schedule()


def student_sidebar():
    # Sidebar for class selection and new class joining
    with st.sidebar:
        st.write("""
                Here's a quick guide to the buttons you'll find on this page: 
                - **FAQ**: View FAQs or ask a new one. 🎓
                - **Schedule**: Use this to view and manage the class schedule. 🗓️
                - **Upload Files**: Upload your notes, outlines, etc. 📚
            """)
        st.sidebar.title("Manage Classes")
        cm.show_class()

        # Button to join a new class
        if st.button("Join a new class"):
            st.session_state.show_join_class_input = not st.session_state.show_join_class_input

        if st.session_state.show_join_class_input:
            cm.join_class()
        

        ################################
        # Modules
        st.sidebar.title("Modules")
        md.show_module()

        if st.button("Upload File", key='module_upload'):
            st.session_state.show_upload_file2 = not st.session_state.show_upload_file2

        if st.session_state.show_upload_file2:
            fu.upload_module_file()

        st.sidebar.title("FAQs")
        fq.student_faqs()
        

        #schedule
        st.sidebar.title("Upcoming Assignments")
        sc.student_schedule()
