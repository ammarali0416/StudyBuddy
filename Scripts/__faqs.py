# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    __faqs.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ammar syed ali <https://www.linkedin.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/19 14:40:30 by ammar syed        #+#    #+#              #
#    Updated: 2023/11/19 14:40:30 by ammar syed       ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
'''
Script for the FAQs on the dashboard
'''


import streamlit as st
from Scripts import azsqldb, sessionvars

def teacher_faqs():
    if st.button("FAQs"):
        st.session_state.show_faqs = not st.session_state.show_faqs  # Toggle the show_faqs state

    if st.session_state.show_faqs:
        # Fetch FAQs as a DataFrame
        faq_df = azsqldb.get_questions(st.session_state.class_info['class_id'], st.session_state.sqlcursor)
        
        if not faq_df.empty:
            st.info("Edit this table to answer, edit, add or delete questions.")
            # Display the DataFrame with an editable interface
            edited_data = st.data_editor(key="FAQ Editor", 
                                        data=faq_df[['question', 'answer', 'faq_id', 'class_id', 'user_id']],
                                        num_rows='dynamic',
                                        disabled=['faq_id', 'class_id', 'user_id'],
                                        column_config={'question': 'Question',
                                                        'answer': 'Answer',
                                                        'faq_id': None,
                                                        'class_id': None,
                                                        'user_id': None},
                                        hide_index=True)
        
            if st.button('Publish'):
                with st.spinner('Updating FAQs...'):
                    # Check for changes and update
                    azsqldb.update_faqs(faq_df, edited_data, st.session_state.sqlcursor)
                    st.success("FAQs updated successfully!")
        
        else:
            st.write("No FAQs available for this class.")

def student_faqs():
    if st.button("FAQs"):
        st.session_state.show_faqs = not st.session_state.show_faqs  # Toggle the show_faqs state

    if st.session_state.show_faqs:
        faq_df = azsqldb.get_questions(st.session_state.class_info['class_id'], st.session_state.sqlcursor)

        if not faq_df.empty:
            # Display the DataFrame with an editable interface
            st.info("Add new rows to the table to ask a new question.")
            edited_data = st.data_editor(key="FAQ Editor", 
                                        data=faq_df[['question', 'answer', 'faq_id', 'class_id', 'user_id']],
                                        num_rows='dynamic',
                                        disabled=['faq_id', 'class_id', 'user_id', 'answer'],
                                        column_config={'question': 'Question',
                                                        'answer': 'Answer',
                                                        'faq_id': None,
                                                        'class_id': None,
                                                        'user_id': None},
                                        hide_index=True)
            if st.button('Ask question'):
                with st.spinner('Updating FAQs...'):
                    # Check for changes and update
                    azsqldb.update_faqs(faq_df, edited_data, st.session_state.sqlcursor)
                    st.success("FAQs updated successfully!")
        else:
            st.write("No FAQs available for this class.")
