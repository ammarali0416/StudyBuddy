import streamlit as st
import pandas as pd
from datetime import datetime
from Scripts import azsqldb

#1 add a database function to get all the assignments already associated with the class
#  display that as a table in show_schedule
# add a function to add new assignments



def teacher_schedule():
    # Initialize session state variables
    if 'schedule_data' not in st.session_state:
        st.session_state.schedule_data = azsqldb.get_assignments(st.session_state.class_info['class_id'], st.session_state.sqlcursor)

    def add_task(task, due_date, class_id):
        azsqldb.add_assignment(st.session_state.sqlcursor, task, due_date, st.session_state.class_info['class_id'])
        #new_entry = {'Task': task, 'Due Date': due_date}
        st.session_state.schedule_data = azsqldb.get_assignments(st.session_state.class_info['class_id'], st.session_state.sqlcursor)
        # azsqldb.add_assignment(assignment_name, due_date, class_id)

    def show_schedule():
        st.table(st.session_state.schedule_data)

    with st.form("task_form"):
        task = st.text_input("Task")
        due_date = st.date_input("Due Date", min_value=datetime.today())
        submit_button = st.form_submit_button("Add Task")

    if submit_button and task:
        add_task( task, due_date, st.session_state.class_info['class_id'])

    show_schedule()




def student_schedule():
    # Initialize session state variables
    if 'schedule_data' not in st.session_state:
        st.session_state.schedule_data = azsqldb.get_assignments(st.session_state.class_info['class_id'], st.session_state.sqlcursor)

    if 'completed_tasks' not in st.session_state:
        st.session_state.completed_tasks = []

    def show_schedule():
        for i, row in st.session_state.schedule_data.iterrows():
            task = row['Task']
            due_date = row['Due Date']
            if task not in st.session_state.completed_tasks:
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(task)
                with col2:
                    st.write(due_date)
                with col3:
                    if st.button('Done', key=task):
                        st.session_state.completed_tasks.append(task)

    # Display the schedule
    show_schedule()

    # Optionally, display completed tasks
    st.write("## Completed Tasks")
    for task in st.session_state.completed_tasks:
        st.write(task)



