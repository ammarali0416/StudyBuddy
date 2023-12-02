# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    sessionvars.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ammar syed ali <https://www.linkedin.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/19 13:57:12 by ammar syed        #+#    #+#              #
#    Updated: 2023/11/19 13:57:12 by ammar syed       ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
"""
Initialize session variables for the app
"""

import streamlit as st
from Scripts import azsqldb
from random import randint

def initialize_session_vars():
    '''
        LOGIN vars
    '''
    # Store the user information in a dictionary
    if "user_info" not in st.session_state:
        st.session_state.user_info = {'user_id': None,
                    'role': None,
                    'username': None}

    # Create a cursor object
    if "sqlcursor" not in st.session_state:
        st.session_state.sqlcursor = azsqldb.connect_to_azure_sql()

    '''
    Dashboard vars
    '''

    #####
    # Sidebar vars
    # Initialize the class information
    if "class_info" not in st.session_state:
        st.session_state.class_info = {'class_id': None,
                                    'class_name': None,
                                    'class_code': None,
                                    'index_name': None}
    # Store the class information
    if "class_info" not in st.session_state:
        st.session_state.class_info = None
    # Store the selected class so the dashboard remains the same after navigating to other pages
    if 'selected_class_name' not in st.session_state:
        st.session_state.selected_class_name = None
    # New class toggle (teacher)
    if 'show_new_class_input' not in st.session_state:
        st.session_state.show_new_class_input = False
    # Join class toggle (student)
    if 'show_join_class_input' not in st.session_state:
        st.session_state.show_join_class_input = False

    #####
    # Faqs vars
    # The FAQ toggle
    if 'show_faqs' not in st.session_state:
        st.session_state.show_faqs = False

    ####
    # upload file vars
    if 'show_upload_file' not in st.session_state:
        st.session_state.show_upload_file = False
    
    if 'show_upload_file2' not in st.session_state:
        st.session_state.show_upload_file2 = False
        
    # Initialize the upload counter in session state
    if 'upload_key' not in st.session_state:
        st.session_state.upload_key = str(randint(0, 1000000))
    
        # Initialize the upload counter in session state
    if 'upload_key_2' not in st.session_state:
        st.session_state.upload_key_2 = str(randint(1000001, 10000000))

    ####
    # Module vars
        # Store the selected class so the dashboard remains the same after navigating to other pages
    if 'selected_module_name' not in st.session_state:
        st.session_state.selected_module_name = None
    # New module toggle (teacher)
    if 'new_module_toggle' not in st.session_state:
        st.session_state.new_module_toggle = False
    # Delete module toggle (teacher)
    if 'delete_module_toggle' not in st.session_state:
        st.session_state.delete_module_toggle = False
    # Store module information
    if "module_info" not in st.session_state:
        st.session_state.module_info = {
            'module_id': None,
            'module_name': None
        }
