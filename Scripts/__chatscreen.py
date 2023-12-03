# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __chatscreen.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ammar syed ali <https://www.linkedin.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/12/02 15:17:52 by ammar syed        #+#    #+#              #
#    Updated: 2023/12/02 15:17:52 by ammar syed       ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
import streamlit as st
import openai
from Scripts import azsqldb, sessionvars, azblob as azb

sessionvars.initialize_session_vars()

def context_selection():
    """
    A widget that allows the user to select what context the chatbot has access to
    """
    modules = azsqldb.get_modules(st.session_state.class_info['class_id'], st.session_state.sqlcursor)
    context_container = st.container()
    with context_container:
        st.info("Choose the modules StudyBuddy will help you with")
        # Counter to track the current column
        col_counter = 0
        # Iterating over the modules
        for module_name, module_id in modules.items():
            # Every three modules, create a new row of columns
            if col_counter % 3 == 0:
                col1, col2, col3 = st.columns(3)

            # Place the checkbox in the current column
            if col_counter % 3 == 0:
                with col1:
                    st.checkbox(module_name, key=f"module_{module_id}")
            elif col_counter % 3 == 1:
                with col2:
                    st.checkbox(module_name, key=f"module_{module_id}")
            elif col_counter % 3 == 2:
                with col3:
                    st.checkbox(module_name, key=f"module_{module_id}")

            # Increment the column counter
            col_counter += 1
        
        # Add a button to submit the selected modules
        if st.button("Let's Study!"):
            # Get the selected modules
            selected_modules = []
            for module_name, module_id in modules.items():
                if st.session_state[f"module_{module_id}"]:
                    selected_modules.append(module_name)
            # If the user didn't select any modules, display a warning
            if len(selected_modules) == 0:
                st.warning("Please select at least one module")
            else:
                st.session_state.selected_modules = selected_modules
                st.session_state.context_selection_toggle = False
                st.experimental_rerun()

def initialize_chat():
    module_learning_outcomes, class_learning_outcomes = azsqldb.get_learning_outcomes(
                                                            st.session_state.class_info['class_id'], 
                                                            st.session_state.selected_modules, 
                                                            st.session_state.sqlcursor)

    initial_prompt = f"""
<INFO> INITIAL PROMPT </INFO>
You're chatting with {st.session_state.user_info['username']}\n
Their role is : {st.session_state.user_info['role']}\n
The class is : {st.session_state.class_info['class_name']}\n
The class learning outcomes are:\n {class_learning_outcomes}\n
You are going to discuss the following modules:\n
"""

    for module, outcome in module_learning_outcomes.items():
        initial_prompt += f" -Module: {module}\n\n"
        initial_prompt += f" -Learning outcomes: {outcome}\n\n"

    return initial_prompt
