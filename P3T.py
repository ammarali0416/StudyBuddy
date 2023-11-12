import streamlit as st
import pandas as pd

# Create a DataFrame to store the data
df = pd.DataFrame(columns=['Question', 'Answer'])

# Function to show the popup for input
def show_popup():
    with st.form("popup_form"):
        question = st.text_input("Enter Question:")
        answer = st.text_input("Enter Answer:")
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if question and answer:
            df.loc[len(df)] = [question, answer]

# Main Streamlit app
def main():
    st.title("Q&A Streamlit App")

    # Plus button in the sidebar to show the popup
    with st.sidebar:
     if show_popup():
        pass

    # Display the data in a column on the right
    st.write("## Q&A List")
    st.write(df)

if __name__ == "__main__":
    main()

