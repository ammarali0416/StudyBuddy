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
import azsqldb
import streamlit as st

# Store the user id
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Store the user role
if "role" not in st.session_state:
    st.session_state.role = None

# Create a cursor object
if "sqlcursor" not in st.session_state:
    st.session_state.sqlcursor = azsqldb.connect_to_azure_sql()

def signup():
    st.subheader("Sign Up")
    
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
            st.session_state.user_id = user_id   # Store the user_id in session_state
            st.session_state.role = role # Store the role to determine what gets shown on the other pages
            st.success(f"Welcome, {username}! \n Your dashboard is now available!")
            
        else:
            st.error(message)

# Main application
st.set_page_config(page_title="Study Buddy",
                   initial_sidebar_state="auto")

# Create a dropdown to select action (Sign Up or Log In)
selected_action = st.selectbox("Select an action:", ["Sign Up", "Log In"])

if selected_action == "Sign Up":
    signup()
elif selected_action == "Log In":
    login()
