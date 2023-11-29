# **StudyBuddy: An Intelligent Education App**

StudyBuddy is an innovative educational application designed to streamline classroom management and enhance student engagement through intelligent digital interactions.

# How it Works
![Study Buddy Architecture Diagra,](Overview.png)


Teachers can create classes, manage FAQs, and upload files.
Students join classes using a class code and interact with the FAQs and chatbot.


## Prerequisites
#### Azure Services
This program uses the following Azure services:
- Azure SQL Database
- Azure AI Search
- Create an Azure account here (make as a link).

#### Required packages
Execute ```pip install -r requirements.txt``` to install necessary packages.

#### Python environment
Please create a .env file in the root directory of this project with the following variables:
```
OPENAI_API_KEY: Your API key for OpenAI services.
AZURE_SERVER: The server address for your Azure SQL Database.
AZURE_DATABASE: The name of your Azure SQL database.
AZURE_USERNAME: Your username for Azure SQL Database.
AZURE_PASSWORD: Your password for Azure SQL Database.
AZURE_AI_SEARCH_API_KEY: Your API key for Azure AI Search services.
AZURE_AI_SEARCH_ENDPOINT: The endpoint URL for Azure AI Search services.
```
Replace the placeholder values with your actual credentials to ensure proper functionality of the application.

## Features and Modules

#### LOGIN.py
Manages user authentication. Users can log in with their credentials, redirecting to the appropriate interface based on their role (teacher/student). User data is stored in an Azure SQL database

#### DASHBOARD.py
The core interface after login. It presents a dashboard where users can navigate through different functionalities like class selection, and viewing schedules.

#### __faqs.py
A dynamic FAQ section. Teachers can add/edit FAQs, while students can view and add new questions.

#### chatbot.py
An AI-driven chatbot for real-time assistance, powered by Azure Open AI.

#### __sidebar.py
Provides a navigational sidebar for easy access to different sections of the app, like FAQs, file uploads, and schedules.

#### __fileupload.py
Enables file uploading for assignments or educational materials.

#### azsqldb.py
Handles interactions with Azure SQL Database for data storage and retrieval.

#### sessionvars.py
Manages session variables for state maintenance across the application.

## Deployment
Run ```streamlit run login.py`` to deploy the app locally

## Packages Used

Streamlit - The framework used to build the app.

## License

This project is licensed under the MIT License.
