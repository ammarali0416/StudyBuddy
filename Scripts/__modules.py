# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __modules.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ammar syed ali <https://www.linkedin.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/01 09:45:29 by ammar syed        #+#    #+#              #
#    Updated: 2023/12/01 09:45:29 by ammar syed       ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import streamlit as st
from Scripts import azsqldb, sessionvars

sessionvars.initialize_session_vars()

def fetch_module_data():
    return azsqldb.get_modules(st.session_state.class_info['class_id'],
                        st.session_state.sqlcursor)

def show_module():
    # Fetch module data for the selected class
    module_data = fetch_module_data()

    if module_data:
        # Select box for choosing the module
        selected_module_name = st.selectbox("Select module:", list(module_data.keys()), index=list(module_data.keys()).index(st.session_state.selected_module_name) if st.session_state.selected_module_name in module_data else 0)
        st.session_state.selected_module_name = selected_module_name
        # Save the module info for the selected module
        if selected_module_name:
            selected_module_info = module_data[selected_module_name]
            st.session_state.module_info = {'module_id': selected_module_info, 'module_name': selected_module_name}
    else:
        st.selectbox("Select module:", ["No modules available"])

def create_new_module():
    # Input field and button for new module creation
    new_module_name = st.text_input("Enter the name for the new module")
    if st.button("Submit New Module"):
        if new_module_name:
            # Call the function to add a new module to the database
            azsqldb.new_module(st.session_state.class_info['class_id'], new_module_name, st.session_state.sqlcursor)
            
            # Optionally, fetch the updated module data to refresh the page or to show the updated list
            # module_data = fetch_module_data()
            # Do something with module_data if needed
            
            # Provide feedback to the user and reset the input field
            st.success(f"New module '{new_module_name}' created successfully for class '{st.session_state.class_info['class_name']}'")
            st.session_state.selected_module_name = new_module_name  # Update the selected class name
            st.session_state.new_module_toggle = False  # Hide the input fields after submission
            st.experimental_rerun()  # Rerun the script to reflect the changes

def delete_module():
    # Fetch module data for the selected class
    module_data = fetch_module_data()

    if module_data:
        # Select box for choosing the module to delete
        selected_module_name = st.selectbox("Select module to delete:", list(module_data.keys()))
        # Get the module id using the selected module name
        module_id = module_data[selected_module_name]  # Assuming module_data maps module names to their ids

        # Button to delete the selected module
        if st.button("Delete Module"):
            # Call the function to delete the module from the database
            azsqldb.delete_module(module_id, st.session_state.sqlcursor)
            st.session_state.delete_module_toggle = False  # Hide the input fields after submission
            st.experimental_rerun()  # Rerun the script to reflect the changes
    else:
        st.write("No modules available to delete.")

