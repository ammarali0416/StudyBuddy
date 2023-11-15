import streamlit as st
import azsqldb

if "user_info" not in st.session_state:
    st.session_state.user_info = {'user_id': None,
                 'role': None,
                 'username': None}
# Store the class information
if "class_info" not in st.session_state:
    st.session_state.class_info = None

# Store the selected class so the dashboard remains the same after navigating to other pages
if 'selected_class_name' not in st.session_state:
    st.session_state.selected_class_name = None

def dashboard():
    def fetch_class_data():
        return azsqldb.get_classes(st.session_state.user_info['user_id'],
                                   st.session_state.user_info['role'],
                                   st.session_state.sqlcursor)

    if 'selected_class_name' not in st.session_state:
        st.session_state.selected_class_name = None

    if 'show_new_class_input' not in st.session_state:
        st.session_state.show_new_class_input = False

    # Fetch class data
    class_data = fetch_class_data()

    if st.session_state.user_info['role'] == 'teacher':
        col1, col2 = st.columns([3, 1])  # Adjust the ratio as needed

        with col1:
            if class_data:
                selected_class_name = st.selectbox("Select class:", list(class_data.keys()), index=list(class_data.keys()).index(st.session_state.selected_class_name) if st.session_state.selected_class_name in class_data else 0)
                st.session_state.selected_class_name = selected_class_name
                
                if selected_class_name:
                    selected_class_info = class_data[selected_class_name]
                    st.write("Selected class details:", selected_class_info)
            else:
                st.selectbox("Select class:", ["No classes available"])
                st.write("You haven't created any classes yet.")

        with col2:
            if class_data and st.session_state.selected_class_name:
                st.write(f"Class Code: {class_data[st.session_state.selected_class_name]['class_code']}")

            if st.button("Create a new class"):
                st.session_state.show_new_class_input = True

        if st.session_state.show_new_class_input:
            new_class_name = st.text_input("Enter the name for the new class")
            if st.button("Submit New Class"):
                if new_class_name:
                    azsqldb.new_class(st.session_state.user_info['user_id'], st.session_state.sqlcursor, new_class_name)
                    class_data = fetch_class_data()  # Refresh the class data
                    st.session_state.selected_class_name = new_class_name  # Update the selected class name
                    st.session_state.show_new_class_input = False  # Hide the input fields after submission
                    st.experimental_rerun()  # Rerun the script to reflect the changes


def main():
    st.title("Dashboard")

    # Check if the user is logged in or not
    if not st.session_state.user_info['user_id']:
        st.warning('Please sign in first!')
    else:
        dashboard()

if __name__ == "__main__":
    main()