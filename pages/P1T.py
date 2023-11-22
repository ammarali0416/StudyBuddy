import streamlit as st
from streamlit_extras.colored_header import colored_header
from markdownlit import mdlit

# Create a session state to persist data
if 'classes' not in st.session_state:
    st.session_state.classes = []

# Function to add a new class
def add_class(new_class):
    st.session_state.classes.append(new_class)

# Main application
#st.title("Welcome (Teacher) to your Home Page")#
def title():
    colored_header(
        label="[red]Welcome (Teacher)[/red] [blue]to your new home page[/blue]",
        color_name="violet-70",
        )

def title2():
    mdlit(
        " ## [red]Welcome (Teacher)[/red] [blue]to your new home page[/blue]"
        )

# Sidebar for class input
st.sidebar.title("Manage Classes")

# Add Class button with a plus sign
with st.form("add_class_form"):
    new_class = st.text_input("Enter Class Name")
    add_button = st.form_submit_button("Add Class (+)")

# Handle form submission
if add_button:
    if new_class:
        add_class(new_class)


# Display the list of classes as buttons on the left margin
st.sidebar.markdown("## Classes")
for c in st.session_state.classes:
    st.sidebar.button(c)

# Center the four buttons in a 2x2 formation
#st.markdown("## Buttons in a 2x2 Formation")

col1, col2 = st.columns(2)

if col1.button("FAQ"):
    st.write("Button 1 clicked!")

if col2.button("Upload Class Materials"):
    st.write("Button 2 clicked!")

col3, col4 = st.columns(2)

if col3.button("Schedule"):
    st.write("Button 3 clicked!")

if col4.button("Add Module"):
    st.write("Button 4 clicked!")


if st.session_state.user_info['user_id']:
    title()
if st.session_state.user_info['user_id']:  
    title2()