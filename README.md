![Study Buddy Logo](StudyBuddyLogo.png)
# StudyBuddy: An Intelligent Education App

StudyBuddy is an innovative educational application designed to streamline classroom management and enhance student engagement through intelligent digital interactions. It offers a range of features including class creation, FAQ management, file uploads for teachers, and interactive class joining and FAQ interactions for students.

# Demo the app
### User accounts
Sample teacher account (Username: t1, Password t1)
Sample student accounts (Username s1, Password s1)

### Try out some of the following prompts:
#### Sample Teacher prompt:
Log in as t1
Select the REL 3367 class from the dropdown menu
Select the Early Islam Module from the dropdown menu
Ask Study Buddy: Please make me an assignment that will allow students to learn about the characteristics of the Early Islamic time period and issues that arose following the death of Prophet Muhammad. This assignment should be a medium-hard level of difficulty and require some critical thinking components.

#### Sample Student prompt:
Log in as s1
Select the BUS 5000 class from the dropdown menu
Select the Introduction module from the dropdown menu
Ask Study Buddy: Can you explain to me the purpose and value of the education and skill set that comes from an MBA? Please give me some exercises I can work on throughout this course based on the textbook to practice the skills I will learn. Make some of the exercises easy and some more difficult.


# How it Works
![Study Buddy Architecture Diagram](Overview.png)

StudyBuddy operates through a user-friendly interface, allowing teachers to create classes, modules within their classes, manage FAQs, and upload files.

Teachers provide descriptions and key learning outcomes for every class and module within the class, which the chatbot takes into account when answering questions to tailor its responses to the specifics of that class.

Students can join classes using a class code and interact with the class materials provided by the teacher. Both teachers and students can interface with StudyBuddy’s built in chatbot, which utilizes OpenAI’s Chatgpt 4 model to answer questions based on the specific class and module selected.

When a conversation begins, the user selects the modules they want to chat about. Once these are selected, the app pulls the relevant files from Azure blob storage, and the relevant contextual information for the class and each selected module from Azure SQL DB, and uploads this to the OpenAI API endpoint. The OpenAI assistant retrieves this information as necessary to inform its responses.

Teachers can use the chatbot to ask about the extent of their students’ knowledge, since the chatbot analyzes notes uploaded by students. They can also use it as a tool for lesson planning and ensuring they meet federal, state, and local education requirements. Students can use the chatbot to ask about anything pertaining to the class; the chatbot’s prompting is set up in a way in which it does not directly give students all the answers, rather it aims to act as a teacher in guiding them to the answer so the student actively learns in the process.

### Features:
##### Add Classes
##### Add Modules within Classes
##### Add/Answer FAQs
##### Manage Assignments (Add/complete tasks)
##### Interactive chatbot 

## Technical Details

The application is structured with modularity in mind. Each feature, such as user authentication (`LOGIN.py`), dashboard management (`DASHBOARD.py`), FAQ handling (`__faqs.py`), and others, is encapsulated in its own script. This modular approach not only makes the codebase easier to navigate but also simplifies maintenance and future enhancements.

Modules are imported efficiently, ensuring that each script only loads the necessary dependencies. This reduces the app's overall memory footprint and improves performance. For instance, `sessionvars.py` is crucial for maintaining user state across the application and is imported in scripts where session management is required. Similarly, `azsqldb.py` handles all interactions with the Azure SQL Database and is imported in modules requiring database access.


## Tech Stack
### Azure Services
##### Azure SQL Database (https://azure.microsoft.com/en-us/services/sql-database/)
      – storing and retrieving user data
##### Azure Storage (https://azure.microsoft.com/en-us/products/storage/blobs)
      – for file storage
##### Azure App Service (https://azure.microsoft.com/en-us/products/app-service)
      – to host the project as a web app
### OpenAI Services (https://azure.microsoft.com/en-us/products/ai-services/openai-service)
##### OpenAI custom configured assistant
##### Code interpreter and knowledge retrieval are enabled

### Required Packages
Run `pip install -r requirements.txt` in your terminal to install necessary packages.

### Python Environment
Configure a `.env` file in the root directory with the following variables:

OPENAI_API_KEY= Your API key for Open AI services  
OPENAI_ASSISTANT= Your OpenAI model   
AZURE_SERVER= The server address for your Azure SQL Database  
AZURE_DATABASE= The name of your Azure SQL database  
AZURE_USERNAME= Your username for Azure SQL Database  
AZURE_PASSWORD= Your password for Azure SQL Database  
AZURE_STORAGE_CONNECTION_STRING= Your connection for Azure Storage account  
AZURE_CONTAINER= Your name for Azure Blob storage container  

### Features and Modules

#### `LOGIN.py`
Manages user authentication, redirecting to the appropriate interface based on user role (teacher/student).

#### `DASHBOARD.py`
Serves as the core interface after login, presenting a dashboard for class selection, and viewing schedules.

#### `__faqs.py`
Facilitates a dynamic FAQ section where teachers can add/edit FAQs, and students can view and add new questions.

#### `chatbot.py`
An AI-driven chatbot for real-time assistance, powered by [Azure Open AI](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/).

#### `__sidebar.py`
Provides a navigational sidebar for easy access to different sections of the app.

#### `__fileupload.py`
Enables file uploading for assignments or educational materials.

#### `azsqldb.py`
Handles interactions with [Azure SQL Database](https://azure.microsoft.com/en-us/services/sql-database/) for data storage and retrieval.

#### `sessionvars.py`
Manages session variables for maintaining state across the application.

## Future Configuration

In the upcoming updates, detailed steps on how to configure the OpenAI Assistant for StudyBuddy will be provided. This will include guidance on setting up the assistant, customizing its behavior to suit the educational context, and integrating it seamlessly with other components of the app. Stay tuned for these enhancements to maximize the capabilities of StudyBuddy.

### Future deplyoments

Current deployment is limited to one user funcationality at a time, with a future expansaion to increase the user limit. 

We will also be using Azure OpenAI Bot Service and OpenAI ChatGPT endpoint instead of ChatGPT and OpenAI ChatGPT Assistant Endpoint.

## Deployment

Run `streamlit run login.py` to deploy the app locally. For more information on Streamlit, visit [Streamlit's documentation](https://docs.streamlit.io).

## Built With

- [Streamlit](https://streamlit.io) - The framework used to build the app.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
