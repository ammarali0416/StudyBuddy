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
        st.sidebar.title(f"Welcome, {st.session_state.user_info['username']}!")

        st.write("""
                Here's a quick guide to the buttons you'll find on this page: 
                - **Class**: Navigate through classes.
                - **Modules**: Upload class materials, assignments, and other resources. 📚
                - **FAQs**: View and answer students' questions. 🎓
                - **Manage Assignments**: Use this to view and manage the class's tasks. 🗓️
                
                 Clicking on a button toggles the corresponding function.""")
        ## Class management
        st.sidebar.title("Class")

        class_description = """
        **The Class feature allows the instructor to:**
        - Create new classes.
        - Upload educational materials pertaining to the class as a whole.
        - Auto generate class code to enable students to join their class.
        """

        st.write(class_description)

        cm.show_class()

        col1, col2 = st.columns([1.4,1])

        with col1:
            # Button to create a new class
            if st.button("New Class", use_container_width=True):
                st.session_state.show_new_class_input = not st.session_state.show_new_class_input
                st.session_state.show_upload_file = False

        with col2:
            # Button to upload class level files
            if st.button("Upload File", key='class_upload', use_container_width=True):
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

        module_description = """
        **This functionality assists the educator in structuring their course by:**
        - Creating and deleting distinct modules within classes. 
        - Uploading specific educational materials within each module.
        - Enabling students to pose targeted questions related to each module through the Study Buddy chat box.
        """

        st.write(module_description)
        md.show_module()

        col3, col4, col5 = st.columns([1,1,1])
        
        with col3:
            if st.button("New module"):
                st.session_state.new_module_toggle = not st.session_state.new_module_toggle
                st.session_state.delete_module_toggle = False
                st.session_state.show_upload_file2 = False
    
        with col4:  
            if st.button("Delete module"):
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

        FAQs_description = """
        **The FAQ feature empowers the instructor to:**
        - Curate a set of frequently asked questions relevant to the class.
        - Display this FAQ repository prominently in the student interface.
        - Offer comprehensive answers to address any queries about the course.
        - Answer questions directly sent by students. 
        """

        st.write(FAQs_description)

        fq.teacher_faqs()

        #schedule
        st.sidebar.title("Manage Assignments")
    
        manage_description = """
        **The Managing Assignments function allows teachers to:**
        - This is a future feature we plan to release in the next version of Study Buddy.
        - Generate tasks with due dates corresponding to the selected class.
        - Make these tasks visible on the student interface.
        - Enable students to mark them as completed.
        """

        st.write(manage_description)

        sc.teacher_schedule()

        if st.sidebar.button("Reset Chat", use_container_width=True, ):
            st.session_state.user_info['user_id'] = None
            st.session_state.cleanup = False
            st.experimental_rerun()


def student_sidebar():
    # Sidebar for class selection and new class joining
    with st.sidebar:
        st.sidebar.title(f"Welcome, {st.session_state.user_info['username']}!")

        st.write("""
                Here's a quick guide to the buttons you'll find on this page: 
                - **Manage Classes**: Navigate through courses.
                - **Modules**: Upload your notes to a specified class module. 📚
                - **FAQ**: View FAQs or create a new one. 🎓
                - **Upcoming Assignments**: Use this to view and manage the class's assignments. 🗓️
                 
                 Clicking on a button toggles the corresponding function.""")
        st.sidebar.title("Manage Classes")
        manage_classes_description = """
        **The Manage Class feature allows the student to:**
        - View and select their classes from a list. 
        - Join a new class using a class code provided by the instructor.
        """
        st.write(manage_classes_description)
        cm.show_class()

        col111, col222 = st.columns([1.4,1])

        # Button to join a new class
        if col111.button("Join a new class", use_container_width=True):
            st.session_state.show_join_class_input = not st.session_state.show_join_class_input

        if st.session_state.show_join_class_input:
            cm.join_class()
        

        ################################
        # Modules
        st.sidebar.title("Modules")
        modules_description = """
        **This Modules functionality allows the student to:**
        - Navigate the modules in their selected course.
        - Upload files pertaining to modules within the selected course which can then be used by the Study Buddy chat bot. 
        """

        st.write(modules_description)
        md.show_module()

        if st.button("Upload File", key='module_upload', use_container_width=True):
            st.session_state.show_upload_file2 = not st.session_state.show_upload_file2

        if st.session_state.show_upload_file2:
            fu.upload_module_file()

        st.sidebar.title("FAQs")
        faqs_description = """
        **The FAQ feature empowers the student to:**
        - Access and explore the FAQ repository, featuring questions deemed useful by the teacher.
        - Directly pose questions to the teacher.
        """
        st.write(faqs_description)
        if st.button("FAQs", use_container_width=True):
            st.session_state.show_faqs = not st.session_state.show_faqs    
        
        if st.session_state.show_faqs:
            fq.student_faqs()
        

        #schedule
        st.sidebar.title("Upcoming Assignments")
        upcoming_assignments_description = """
       **The Upcoming Assignments function allows the student to:**
        - Review tasks assigned by the instructor along with their respective due dates.
        - Utilize the 'Done' button upon completing an assignment for organizational purposes, and the accomplished tasks will be displayed in the 'Completed Tasks' section.
        """
        st.write(upcoming_assignments_description)

        sc.student_schedule()

        if st.sidebar.button("Reset Chat", use_container_width=True, ):
            st.session_state.user_info['user_id'] = None
            st.session_state.cleanup = False
            st.experimental_rerun()
