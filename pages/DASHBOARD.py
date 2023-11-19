import streamlit as st
import pandas as pd
from Scripts import azsqldb

# Initialize the user information
if "user_info" not in st.session_state:
    st.session_state.user_info = {'user_id': None,
                                  'role': None,
                                  'username': None}
# Initialize the class information
if "class_info" not in st.session_state:
    st.session_state.class_info = {'class_id': None,
                                   'class_name': None,
                                   'class_code': None}
# Store the class information
if "class_info" not in st.session_state:
    st.session_state.class_info = None
# Store the selected class so the dashboard remains the same after navigating to other pages
if 'selected_class_name' not in st.session_state:
    st.session_state.selected_class_name = None
# Store the new class input field state (teacher)
if 'show_new_class_input' not in st.session_state:
    st.session_state.show_new_class_input = False
# Store the join class input field state (student)
if 'show_join_class_input' not in st.session_state:
    st.session_state.show_join_class_input = False
# Initialize the FAQ toggle state in session_state if it doesn't exist
if 'show_faqs' not in st.session_state:
    st.session_state.show_faqs = False
# Initialize a session state variable for FAQ updates
if 'update_faqs' not in st.session_state:
    st.session_state.update_faqs = True



def fetch_class_data():
    return azsqldb.get_classes(st.session_state.user_info['user_id'],
                                st.session_state.user_info['role'],
                                st.session_state.sqlcursor)

def teacher_sidebar():
    # Fetch class data
    class_data = fetch_class_data()

    # Sidebar for class selection and new class creation
    with st.sidebar:
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
            st.session_state.show_new_class_input = True

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


def student_sidebar():
    # Fetch class data
    class_data = fetch_class_data()
    # Sidebar for class selection and new class joining
    with st.sidebar:
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
            st.session_state.show_join_class_input = True
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

def teacher_faqs():
    # Fetch FAQs as a DataFrame
    faq_df = azsqldb.get_questions(st.session_state.class_info['class_id'], st.session_state.sqlcursor)

    if not faq_df.empty:
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


def main():
    # Check if the user is logged in or not
    if not st.session_state.user_info['user_id']:
        st.title("Dashboard")
        st.warning('Please sign in first!')
    else:
        st.title(f"{st.session_state.user_info['username']}'s Dashboard")
        if st.session_state.user_info['role'] == 'teacher':
            teacher_sidebar()
            st.write("""
                Here's a quick guide to the buttons you'll find on this page: 
                - **FAQ**: View and answer students' questions. 🎓
                - **Schedule**: Use this to view and manage the class schedule. 🗓️
                - **Upload Files**: Upload class materials, assignments, and other resources. 📚
            """)
            # Button to toggle FAQs
            if st.button("FAQs"):
                st.session_state.show_faqs = not st.session_state.show_faqs  # Toggle the show_faqs state

            if st.session_state.show_faqs:
                teacher_faqs()
        
        else:
            student_sidebar()
            st.write("""
                Here's a quick guide to the buttons you'll find on this page: 
                - **FAQ**: View FAQs or ask a new one. 🎓
                - **Schedule**: Use this to view and manage the class schedule. 🗓️
                - **Upload Files**: Upload your notes, outlines, etc. 📚
            """)

if __name__ == "__main__":
    main()
