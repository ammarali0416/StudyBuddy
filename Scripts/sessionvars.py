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