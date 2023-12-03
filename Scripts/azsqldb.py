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
import pandas as pd


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
            SELECT class_id, class_name, class_code, index_name 
            FROM master.STUDYBUDDY.Classes 
            WHERE teacher_id = ?
        """, (user_id,))
        class_records = sqlcursor.fetchall()
        # Create a dictionary mapping class names to their full information
        class_info_mapping = {record[1]: {'class_id': record[0], 'class_name': record[1], 'class_code': record[2], 'index_name':record[3]} for record in class_records}
        return class_info_mapping
    else:  # Assuming the only other role is 'student'
        sqlcursor.execute("""
            SELECT c.class_id, c.class_name, c.class_code, c.index_name
            FROM master.STUDYBUDDY.Classes c 
            INNER JOIN master.STUDYBUDDY.StudentClass sc 
            ON c.class_id = sc.class_id 
            WHERE sc.user_id = ?
        """, (user_id,))
        class_records = sqlcursor.fetchall()

        class_info_mapping = {record[1]: {'class_id': record[0], 'class_name': record[1], 'class_code': record[2],'index_name':record[3]} for record in class_records}
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

def new_class(user_id, sqlcursor, class_name, learnig_outcomes):
    """
    Create a new class
    """
    # Generate a random class code
    class_code = ''.join(random.choices('0123456789ABCDEF', k=6))

    # Execute a SQL query to insert the new class
    sqlcursor.execute("INSERT INTO master.STUDYBUDDY.classes (class_name, class_code, teacher_id, LearningOutcomes) VALUES (?, ?, ?, ?)", (class_name, class_code, user_id, learnig_outcomes))
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

def get_questions(class_id, sqlcursor):
    """
    Get all the questions and answers for a particular class
    and return them as a Pandas DataFrame.
    """
    # Execute a SQL query to get all the questions for the provided class_id
    sqlcursor.execute("SELECT class_id, user_id, question, answer, faq_id FROM master.STUDYBUDDY.FAQs WHERE class_id = ?", (class_id,))
    
    # Fetch all the records returned by the query
    question_records = sqlcursor.fetchall()

    # Create a list of dictionaries for each record
    data = []
    for record in question_records:
        data.append({
            'class_id': record[0],
            'user_id': record[1],
            'question': record[2],
            'answer': record[3],
            'faq_id': record[4]
        })

    # Create and return a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)
    return df

def update_faqs(original_df, edited_df, sqlcursor):
    # Separate new questions (with None in faq_id)
    new_questions = edited_df[edited_df['faq_id'].isnull()]
    existing_questions = edited_df[edited_df['faq_id'].notnull()]

    # Process existing questions
    edited_dict = existing_questions.set_index('faq_id').to_dict(orient='index')
    original_dict = original_df.set_index('faq_id').to_dict(orient='index')

    # Identify modified rows
    modified_rows = []
    for faq_id, row in edited_dict.items():
        if faq_id in original_dict:
            if row['question'] != original_dict[faq_id]['question'] or row['answer'] != original_dict[faq_id]['answer']:
                modified_row = row.copy()
                modified_row['faq_id'] = faq_id  # Include the faq_id
                modified_rows.append(modified_row)

    # Convert to DataFrame
    modified_rows_df = pd.DataFrame(modified_rows)
    
    # Check if there are modified rows and update them in the database
    if not modified_rows_df.empty:
        for index, row in modified_rows_df.iterrows():
            # Prepare the UPDATE statement
            update_query = """
            UPDATE STUDYBUDDY.FAQs 
            SET question = ?, answer = ?
            WHERE faq_id = ?
            """
            # Execute the UPDATE statement
            sqlcursor.execute(update_query, row['question'], row['answer'], row['faq_id'])     
        # Commit the changes after all updates
        sqlcursor.connection.commit()

    # Identify new questions
    new_questions = edited_df[~edited_df['faq_id'].isin(original_df['faq_id'])].reset_index(drop=True)

    # Get the user and class IDs from the original DataFrame
    default_class_id = original_df.iloc[0]['class_id']
    default_user_id = original_df.iloc[0]['user_id']

    # Add class_id and user_id to new_questions
    new_questions['class_id'] = default_class_id
    new_questions['user_id'] = st.session_state.user_info['user_id']

    # Check if there are new questions and insert them into the database
    if not new_questions.empty:
        for index, row in new_questions.iterrows():
            insert_query = """
            INSERT INTO STUDYBUDDY.FAQs (question, answer, class_id, user_id) 
            VALUES (?, ?, ?, ?)
            """
            sqlcursor.execute(insert_query, row['question'], row['answer'], row['class_id'], row['user_id'])

        # Commit the changes after all inserts
        sqlcursor.connection.commit()

    # Identify deleted questions
    deleted_questions = original_df[~original_df['faq_id'].isin(edited_df['faq_id'])].reset_index(drop=True)

    # Check if there are questions to delete and delete them from the database
    if not deleted_questions.empty:
        faq_ids_to_delete = tuple(deleted_questions['faq_id'])
        delete_query = """
        DELETE FROM STUDYBUDDY.FAQs 
        WHERE faq_id IN ({})
        """.format(','.join('?' * len(faq_ids_to_delete)))
        sqlcursor.execute(delete_query, faq_ids_to_delete)

        # Commit the changes after deletion
        sqlcursor.connection.commit()

def update_class(sqlcursor, class_id, field, new_value):
    """
    Update the class table with the new value for the provided field
    """
    # Prepare the UPDATE statement
    update_query = f"""
    UPDATE STUDYBUDDY.Classes 
    SET {field} = ?
    WHERE class_id = ?
    """
    # Execute the UPDATE statement
    sqlcursor.execute(update_query, new_value, class_id)

    # Commit the changes
    sqlcursor.connection.commit()

def get_modules(class_id, sqlcursor):
    """
    Get all the modules associated with a particular class
    Returns a dictionary mapping module names to their module IDs
    """
    # Execute SQL query to get all modules for the provided class_id
    sqlcursor.execute("""
        SELECT module_id, module_name
        FROM master.STUDYBUDDY.Modules
        WHERE class_id = ?
    """, (class_id,))
    
    # Fetch all records from the query
    module_records = sqlcursor.fetchall()
    
    # Create a dictionary mapping module names to their IDs
    module_info_mapping = {record[1]: record[0] for record in module_records}
    
    return module_info_mapping

def new_module(class_id, module_name, learning_outcome, sqlcursor):
    """
    Create a new module for a specific class.
    """
    # Execute a SQL query to insert the new module
    sqlcursor.execute("""
        INSERT INTO master.STUDYBUDDY.Modules (class_id, module_name, LearningOutcomes) 
        VALUES (?, ?, ?)
    """, (class_id, module_name, learning_outcome))
    # Commit the transaction
    sqlcursor.connection.commit()

def delete_module(module_id, sqlcursor):
    """
    Delete a module from the database.
    """
    # Execute a SQL query to delete the module
    sqlcursor.execute("""
        DELETE FROM master.STUDYBUDDY.Modules
        WHERE module_id = ?
    """, (module_id,))
    # Commit the transaction
    sqlcursor.connection.commit()

def get_learning_outcomes(class_id, selected_modules, sqlcursor):
    """
    Get the learning outcomes for the selected modules.
    Returns a dictionary mapping module names to their learning outcomes and class information.
    """
    # Execute a SQL query to get the learning outcomes for the selected modules
    sqlcursor.execute("""
        SELECT module_name, LearningOutcomes
        FROM master.STUDYBUDDY.Modules
        WHERE class_id = ?
        AND module_name IN ({})
    """.format(','.join('?' * len(selected_modules))), (class_id, *selected_modules))
    # Fetch all records from the query
    learning_outcome_records = sqlcursor.fetchall()
    # Create a dictionary mapping module names to their learning outcomes
    learning_outcomes = {}
    for record in learning_outcome_records:
        module_name = record[0]
        learning_outcome = record[1]
        learning_outcomes[module_name] = learning_outcome
    
    # Execute a SQL query to get the class information
    sqlcursor.execute("""
        SELECT class_name, LearningOutcomes
        FROM master.STUDYBUDDY.Classes
        WHERE class_id = ?
    """, (class_id,))
    # Fetch the record from the query
    class_record = sqlcursor.fetchone()
    class_learning_outcomes = class_record[1]
    
    return learning_outcomes, class_learning_outcomes
