# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ui.py                                              :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ammar syed ali <https://www.linkedin.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/05 20:20:07 by ammar syed        #+#    #+#              #
#    Updated: 2023/11/05 20:20:07 by ammar syed       ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
from Scripts import azsqldb
import streamlit as st
from markdownlit import mdlit

# Set the page title and the initial state of the sidebar
st.set_page_config(page_title="Study Buddy",
                   initial_sidebar_state="auto")



# Store the user information in a dictionary
if "user_info" not in st.session_state:
    st.session_state.user_info = {'user_id': None,
                 'role': None,
                 'username': None}

# Create a cursor object
if "sqlcursor" not in st.session_state:
    st.session_state.sqlcursor = azsqldb.connect_to_azure_sql()

def signup():
    st.subheader(":rainbow[Sign Up]")
    

    
    # User details input
    new_username = st.text_input("Create a new username")
    new_password = st.text_input("Create a password", type="password")
    email = st.text_input("Enter your email")
    school = st.text_input("Enter your school")
    
    # Role selection using radio buttons
    role = st.radio("Select your role", ["student", "teacher"])
    
    if st.button("Sign Up"):
        if new_username and new_password and email and school:
            message = azsqldb.create_new_user(st.session_state.sqlcursor, new_username, new_password, email, school, role)
            st.success(message)
        else:
            st.warning("Please fill in all the details.")

def login():
    st.subheader("Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Log In"):
        is_authenticated, message, role, user_id = azsqldb.authenticate_user(st.session_state.sqlcursor, username, password)
        
        if is_authenticated:
            user_info = {'user_id': user_id,
                         'role': role,
                         'username': username}
            st.session_state.user_info = user_info
        else:
            st.error(message)



def main():
    # Main application
    # Create a dropdown to select action (Sign Up or Log In)
    selected_action = st.selectbox("Select an action:", ["Log In", "Sign Up"])

    if selected_action == "Sign Up":
        signup()
    elif selected_action == "Log In":
        login()

    # check if the user is logged in and if so display this at the bottom of the screeon
    if st.session_state.user_info['user_id'] != None:
        st.success(f"Welcome, {st.session_state.user_info['username']}! \n Your dashboard is now available!")

if __name__ == "__main__":
    main()
