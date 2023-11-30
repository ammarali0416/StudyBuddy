import streamlit as st
import openai
# used to create the memory
from langchain.memory import ConversationBufferMemory
# used to create the retriever
from langchain.retrievers import AzureCognitiveSearchRetriever
# used to create the retrieval tool
from langchain.agents.agent_toolkits import create_retriever_tool
# used to create the prompt template
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema import SystemMessage
from langchain.prompts import MessagesPlaceholder
# used to create the agent executor
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
# To load environment variables
from dotenv import load_dotenv
import os

# Load environment variables
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

st.header("Study Buddy") # temporary

# Initialize the memory
# This is needed for both the memory and the prompt
memory_key = "history"

if "memory" not in st.session_state.keys():
    st.session_state.memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)

# Initialize the chat message history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome! Let's get ready to learn!"}
    ]

# Initialize the retriever
@st.cache_resource
def get_retriever():
    return AzureCognitiveSearchRetriever(
        content_key="content",
        top_k=3,
        index_name="anams-class",
        api_key=os.getenv("AZURE_AI_SEARCH_API_KEY"),
        service_name="studybuddysearchservice",
    )

retriever = get_retriever()

# define the retriever tool
tool = create_retriever_tool(
    retriever=retriever,
    name="search_class_materials",
    description="Search the class materials for information relevant to the question, and return the most relevant documents and metadata.",
)

tools = [tool]

# define the prompt
system_message = SystemMessage(
        content=("""You are a knowledgeable tutor to guide students:
                - You have tools letting you search the class materials and return relevant documents. Use them to answer questions about class materials.
                - When a question is about class material, guide students to this material for a more in-depth understanding including citations if possible
                - For questions outside class materials, guide them toward discovering the answer.
                - If you don't know an answer, refer them to their teacher.
                Your role is not to answer questions, but to guide students towards learning how to find answers themselves.
"""
        )
)
prompt_template = OpenAIFunctionsAgent.create_prompt(
        system_message=system_message,
        extra_prompt_messages=[MessagesPlaceholder(variable_name=memory_key)]
    )

# Initialize the LLM
llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                 )

# instantiate agent
agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=st.session_state.memory, verbose=True)

# Prompt for user input and display message history
if prompt := st.chat_input("Ask about your class!"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Pass query to chat engine and display response
# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = agent_executor({"input": prompt})
            st.write(response["output"])
            message = {"role": "assistant", "content": response["output"]}
            st.session_state.messages.append(message) # Add response to message history