# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ammar syed ali <https://www.linkedin.co    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/05 13:35:20 by ammar syed        #+#    #+#              #
#    Updated: 2023/11/05 13:35:20 by ammar syed       ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
from dotenv import load_dotenv
import pyodbc
import random
import streamlit as st


def connect_to_azure_sql():
    # Get the path to the directory one level up from where this script is located
    BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # Load the variables from the .env file located at the topmost level
    load_dotenv(os.path.join(BASEDIR, '.env'))

    # Retrieve the connection string variables
    AZURE_SERVER = os.getenv('AZURE_SERVER')
    AZURE_DATABASE = os.getenv('AZURE_DATABASE')
    AZURE_USERNAME = os.getenv('AZURE_USERNAME')
    AZURE_PASSWORD = os.getenv('AZURE_PASSWORD')

    # Create the connection string
    conn_str = f'DRIVER=ODBC Driver 18 for SQL Server;SERVER={AZURE_SERVER};DATABASE={AZURE_DATABASE};UID={AZURE_USERNAME};PWD={AZURE_PASSWORD}'

    try:
        # Connect to the DB
        conn = pyodbc.connect(conn_str)
        # Return a cursor
        return conn.cursor()
    except pyodbc.Error as e:
        if 'IM002' in str(e):
            st.warning("ERROR: The ODBC driver for SQL Server is not installed or configured correctly. \
                        Please download and install the driver from this link: \
                        https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
        else:
            st.warning(f"An error occurred while connecting to the database: {e}")
        return None


def authenticate_user(sqlcursor, username, password):
    # Check if the username exists and retrieve the password, role, and user_id
    sqlcursor.execute("SELECT password, role, user_id FROM master.STUDYBUDDY.Users WHERE username = ?", (username,))
    result = sqlcursor.fetchone()

    if not result:
        # Username doesn't exist
        return False, "No user was found with that username.", None, None

    stored_password, role, user_id = result
    
    if stored_password != password:
        # Passwords don't match
        return False, "Incorrect password for the provided username.", None, None
    
    # If we reached this point, the user is authenticated
    return True, "Authenticated successfully.", role, user_id

def create_new_user(sqlcursor, username, password, email, school, role):
    # Check if the username is already in use
    sqlcursor.execute("SELECT username FROM master.STUDYBUDDY.Users WHERE username = ?", (username,))
    user_result = sqlcursor.fetchone()

    if user_result:
        return "Username is already in use. Please choose a different username."

    # Check if the email is already in use
    sqlcursor.execute("SELECT email FROM master.STUDYBUDDY.Users WHERE email = ?", (email,))
    email_result = sqlcursor.fetchone()

    if email_result:
        # Email is already in use
        return "Email is already in use. Please use a different email address."

    # Insert a new user into the table
    # Assuming user_id is auto-incremented, so we don't need to provide it
    insert_query = '''
    INSERT INTO master.STUDYBUDDY.Users (username, password, email, school, role)
    VALUES (?, ?, ?, ?, ?)
    '''
    sqlcursor.execute(insert_query, (username, password, email, school, role))
    
    # Commit the transaction
    sqlcursor.connection.commit()

    return "User successfully created!"

def get_classes(user_id, role, sqlcursor):
    """
    Get all the classes associated with a particular user
    Returns a dictionary mapping class names to their full information
    """
    # Check if the role is 'teacher'
    if role == 'teacher':
        sqlcursor.execute("""
            SELECT class_id, class_name, class_code 
            FROM master.STUDYBUDDY.Classes 
            WHERE teacher_id = ?
        """, (user_id,))
        class_records = sqlcursor.fetchall()
        # Create a dictionary mapping class names to their full information
        class_info_mapping = {record[1]: {'class_id': record[0], 'class_name': record[1], 'class_code': record[2]} for record in class_records}
        return class_info_mapping
    else:  # Assuming the only other role is 'student'
        sqlcursor.execute("""
            SELECT c.class_id, c.class_name, c.class_code 
            FROM master.STUDYBUDDY.Classes c 
            INNER JOIN master.STUDYBUDDY.StudentClass sc 
            ON c.class_id = sc.class_id 
            WHERE sc.user_id = ?
        """, (user_id,))
        class_records = sqlcursor.fetchall()

        class_info_mapping = {record[1]: {'class_id': record[0], 'class_name': record[1], 'class_code': record[2]} for record in class_records}
        return class_info_mapping
       
"""Example usage of get_classes() function:
#classes = get_classes(4, 'teacher', connect_to_azure_sql())
# outputs a dictionary like this:
# {"Anam's Class": 
    {'class_id': 1,
     'class_name': "Anam's Class",
     'class_code': 'abc123'}, 
   "DANESH'S CLASS": 
    {'class_id': 2, 
     'class_name': "DANESH'S CLASS", 
     'class_code': '555FFF'}
  }
# classes["Anam's Class"]['class_id'] would return 1]"""

def new_class(user_id, sqlcursor, class_name):
    """
    Create a new class
    """
    # Generate a random class code
    class_code = ''.join(random.choices('0123456789ABCDEF', k=6))

    # Execute a SQL query to insert the new class
    sqlcursor.execute("INSERT INTO master.STUDYBUDDY.classes (class_name, class_code, teacher_id) VALUES (?, ?, ?)", (class_name, class_code, user_id))
    # Commit the transaction
    sqlcursor.connection.commit()

def join_class(user_id, sqlcursor, class_code):
    """
    Join a class using the class code.
    """
    # Execute a SQL query to get the class details where the class_code matches the provided class_code
    sqlcursor.execute("SELECT class_id FROM master.STUDYBUDDY.Classes WHERE class_code = ?", (class_code,))
    # Fetch the record returned by the query
    class_record = sqlcursor.fetchone()

    if not class_record:
        # No class was found with the provided class_code
        return "No class was found with the provided class code. Please check the code and try again."

    class_id = class_record[0]

    # Check if the user is already in the class
    sqlcursor.execute("SELECT * FROM master.STUDYBUDDY.StudentClass WHERE user_id = ? AND class_id = ?", (user_id, class_id))
    class_member_record = sqlcursor.fetchone()

    if class_member_record:
        # The user is already in the class
        return "You are already in this class."

    # Execute a SQL query to insert the new class member into the StudentClass table
    sqlcursor.execute("INSERT INTO master.STUDYBUDDY.StudentClass (user_id, class_id) VALUES (?, ?)", (user_id, class_id))
    # Commit the transaction
    sqlcursor.connection.commit()

    return "You have successfully joined the class!"

def ask_question(class_id, user_id, question, sqlcursor):
    """
    Add a new question to the Questions table
    add_question(
        st.session_state.class_info['class_id'],
        st.session_state.user_info['user_id'],
        some_question_variable,
        st.session_state.sqlcursor
    )
    """
    # Execute a SQL query to insert the new question
    sqlcursor.execute("INSERT INTO master.STUDYBUDDY.FAQs (class_id, user_id, question) VALUES (?, ?, ?)", (class_id, user_id, question))
    # Commit the transaction
    sqlcursor.connection.commit()

def get_questions(class_id, sqlcursor):
    """
    Get all the questions and answers for a particular class
    use this to populate the FAQs
    get_questions(st.session_state.class_info['class_id'], st.session_state.sqlcursor)
    """
    # Execute a SQL query to get all the questions for the provided class_id
    sqlcursor.execute("SELECT class_id, user_id, question, answer, faq_id FROM master.STUDYBUDDY.FAQs WHERE class_id = ?", (class_id,))
    # Fetch all the records returned by the query
    question_records = sqlcursor.fetchall()

    # Create a dictionary mapping question_ids to their full information
    question_info_mapping = {record[0]: {'class_id': record[0],
                                         'user_id': record[1],
                                         'question': record[2],
                                         'answer':record[3],
                                         'faq_id':record[4]} for record in question_records}

    return question_info_mapping

def add_faq(user_id, class_id, question, answer, sqlcursor):
    """
    Add a new FAQ to the FAQs table. For teachers only.
    add_faq(st.session_state.user_info['user_id'], 
            st.session_state.class_info['class_id'], 
            some_question_variable, 
            some_answer_variable, 
            st.session_state.sqlcursor)
    """
    # Execute a SQL query to insert the new FAQ
    sqlcursor.execute("INSERT INTO master.STUDYBUDDY.FAQs (user_id, class_id, question, answer) VALUES (?, ?, ?, ?)", (user_id, class_id, question, answer))
    # Commit the transaction
    sqlcursor.connection.commit()