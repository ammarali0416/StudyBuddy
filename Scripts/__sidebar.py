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
from Scripts import azsqldb, sessionvars, __faqs as fq, __fileupload as fu

sessionvars.initialize_session_vars()

def fetch_class_data():
    return azsqldb.get_classes(st.session_state.user_info['user_id'],
                                st.session_state.user_info['role'],
                                st.session_state.sqlcursor)

def teacher_sidebar():
    # Fetch class data
    class_data = fetch_class_data()
   
    # Sidebar for class selection and new class creation
    with st.sidebar:
        st.write("""
                Here's a quick guide to the buttons you'll find on this page: 
                - **FAQ**: View and answer students' questions. 🎓
                - **Schedule**: Use this to view and manage the class schedule. 🗓️
                - **Upload Files**: Upload class materials, assignments, and other resources. 📚
            """)
        ## Class management
        st.sidebar.title("Manage Classes")
        if class_data:
            # Select box for choosing the class
            selected_class_name = st.selectbox("Select class:", list(class_data.keys()), index=list(class_data.keys()).index(st.session_state.selected_class_name) if st.session_state.selected_class_name in class_data else 0)
            st.session_state.selected_class_name = selected_class_name
            # Display the class code for the selected class
            if selected_class_name:
                selected_class_info = class_data[selected_class_name]
                st.session_state.class_info = selected_class_info
                st.write(f"Class Code: {selected_class_info['class_code']}")
        else:
            st.selectbox("Select class:", ["No classes available"])
            st.write("You haven't created any classes yet.")

        # Button to create a new class
        if st.button("Create a new class"):
            st.session_state.show_new_class_input = not st.session_state.show_new_class_input

        if st.session_state.show_new_class_input:
            # Input field and button for new class creation
            if st.session_state.show_new_class_input:
                new_class_name = st.text_input("Enter the name for the new class")
                if st.button("Submit New Class"):
                    if new_class_name:
                        azsqldb.new_class(st.session_state.user_info['user_id'], st.session_state.sqlcursor, new_class_name)
                        class_data = fetch_class_data()  # Refresh the class data
                        st.session_state.selected_class_name = new_class_name  # Update the selected class name
                        st.session_state.show_new_class_input = False  # Hide the input fields after submission
                        st.experimental_rerun()  # Rerun the script to reflect the changes
        
        ### Faq functions
        st.sidebar.title("FAQs")
        fq.teacher_faqs()

        #file upload
        st.sidebar.title("Upload Files")
        fu.upload_file()


        


def student_sidebar():
    # Fetch class data
    class_data = fetch_class_data()
    # Sidebar for class selection and new class joining
    with st.sidebar:
        st.write("""
                Here's a quick guide to the buttons you'll find on this page: 
                - **FAQ**: View FAQs or ask a new one. 🎓
                - **Schedule**: Use this to view and manage the class schedule. 🗓️
                - **Upload Files**: Upload your notes, outlines, etc. 📚
            """)
        st.sidebar.title("Manage Classes")
        if class_data:
            # Select box for choosing the class
            selected_class_name = st.selectbox("Select class:", list(class_data.keys()), index=list(class_data.keys()).index(st.session_state.selected_class_name) if st.session_state.selected_class_name in class_data else 0)
            st.session_state.selected_class_name = selected_class_name
            # Display the class info for the selected class
            if selected_class_name:
                selected_class_info = class_data[selected_class_name]
                st.session_state.class_info = selected_class_info
        else:
            st.selectbox("Select class:", ["No classes available"])
            st.write("You are not enrolled in any classes yet.")
        # Button to join a new class
        if st.button("Join a new class"):
            st.session_state.show_join_class_input = not st.session_state.show_join_class_input

        if st.session_state.show_join_class_input:
            # Input field and button for joining a new class
            if st.session_state.show_join_class_input:
                new_class_code = st.text_input("Enter the class code")
                join_class_button = st.button("Join Class")
                # Block to handle form submission
                if join_class_button and new_class_code:
                    join_message = azsqldb.join_class(st.session_state.user_info['user_id'], st.session_state.sqlcursor, new_class_code)
                    st.warning(join_message)
                    # Handle the a successful class join
                    if join_message == "You have successfully joined the class!":
                        class_data = fetch_class_data()  # Refresh the class data
                        st.session_state.selected_class_name = list(class_data.keys())[-1]  # Update the selected class name to the newly joined class
                        st.experimental_rerun()  # Rerun the script to reflect the changes


        st.sidebar.title("FAQs")
        fq.student_faqs()

        #file upload
        st.sidebar.title("Upload Files")
        fu.upload_file()
