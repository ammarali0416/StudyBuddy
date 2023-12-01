# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __classmanager.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ammar syed ali <https://www.linkedin.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/01 09:05:41 by ammar syed        #+#    #+#              #
#    Updated: 2023/12/01 09:05:41 by ammar syed       ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import streamlit as st
from Scripts import azsqldb, sessionvars

sessionvars.initialize_session_vars()

def fetch_class_data():
    return azsqldb.get_classes(st.session_state.user_info['user_id'],
                                st.session_state.user_info['role'],
                                st.session_state.sqlcursor)

def show_class():
    # Fetch class data
    class_data = fetch_class_data()

    if class_data:
        # Select box for choosing the class
        selected_class_name = st.selectbox("Select class:", list(class_data.keys()), index=list(class_data.keys()).index(st.session_state.selected_class_name) if st.session_state.selected_class_name in class_data else 0)
        st.session_state.selected_class_name = selected_class_name
        # Save the class code for the selected class
        if selected_class_name:
            selected_class_info = class_data[selected_class_name]
            st.session_state.class_info = selected_class_info
            st.write(f"Class Code: {selected_class_info['class_code']}")
    else:
        st.selectbox("Select class:", ["No classes available"])
        # if-else to show different messages for teachers and students with no classes
        if st.session_state.user_info['role'] == 'teacher':
            st.write("You haven't created any classes yet.")
        else:
            st.write("You are not enrolled in any classes yet.")

def create_new_class():
    # Input field and button for new class creation
    new_class_name = st.text_input("Enter the name for the new class")
    if st.button("Submit New Class"):
        if new_class_name:
            azsqldb.new_class(st.session_state.user_info['user_id'], st.session_state.sqlcursor, new_class_name)
            class_data = fetch_class_data()  # Refresh the class data
            st.session_state.selected_class_name = new_class_name  # Update the selected class name
            st.session_state.show_new_class_input = False  # Hide the input fields after submission
            st.experimental_rerun()  # Rerun the script to reflect the changes

def join_class():
    # Input field and button for joining a new class
    new_class_code = st.text_input("Enter the class code")
    join_class_button = st.button("Join Class", use_container_width= True)
    # Block to handle form submission
    if join_class_button and new_class_code:
        join_message = azsqldb.join_class(st.session_state.user_info['user_id'], st.session_state.sqlcursor, new_class_code)
        st.warning(join_message)
        # Handle the a successful class join
        if join_message == "You have successfully joined the class!":
            class_data = fetch_class_data()  # Refresh the class data
            st.session_state.selected_class_name = list(class_data.keys())[-1]  # Update the selected class name to the newly joined class
            st.experimental_rerun()  # Rerun the script to reflect the changes