# StudyBuddy
An Intelligent Education App

Prerequisites

This program uses the following Azure services:
- Azure Open AI
- Azure SQL Database
- Azure AI Search

If you do not have an Azure account, you can use this link to create one.
- [Azure Homepage](azure.microsoft.com)

## Installing

Prior to running the program you must run ```pip install -r requiremnets.txt``` in your terminal. The terminal will check if you have all the necessary packages installed to run the program, and if not it will install them for you.


## Deployment
Once login.py is run and the user inputs their credentials, the dashboard and {insert other pages} will be available.
Once the dashboard is accessed, the user must select a class to interact with from the drop down menu. If the teacher interface is visible and no classes have been created yet, the teacher must first add a class. If the student interface is visible and the student has not joined any classes, the student must first input a class code correlated to an existing class to join that class.

-If the FAQ button is selected on the teacher interface, the user can add a new FAQ or edit existing FAQs in both the question and answer columns.
If the FAQ button is selected on the student interface, the user can only add new questions but not edit any existing questions or answers.

-File Upload

-Schedule


## Built With

-[Streamlit](streamlit.io)


## License

This project is licensed under the MIT License - see the LICENSE.md file for details
