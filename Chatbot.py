from dotenv import load_dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import streamlit as st 
import os
import numpy as np


# Load api from .env
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

DB_FAISS_PATH = "data/db_faiss"


#Loading the model
def load_llm():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-0613",
        openai_api_key=openai_api_key
    )
    return llm

# Create a answer based on prompt and chat history
def conversational_chat(query):
    print("Running query")
    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query,result["answer"]))
    print(result["answer"])
    return result["answer"]

def clear_chat_history():
    st.session_state.messages = None
    st.session_state.history = None   
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]


# Setup streamlit

st.set_page_config(page_title="Chatbot", page_icon=":robot_face:")

st.title("Chat with your OURA data")

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-ada-002")

db = FAISS.load_local(DB_FAISS_PATH,embeddings)
llm = load_llm()
chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever= db.as_retriever())






if 'history' not in st.session_state:
    st.session_state['history'] = []

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role":"assistant", "content":"Hello, ask me anything about your oura health data"}]
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


if user_input := st.chat_input():
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)


        
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = conversational_chat(user_input)
            placeholder = st.empty()
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message)        
    with st.chat_message("assistant"):
        st.write(response)


st.sidebar.button(label= ":wastebasket: Clear chat and history", on_click=clear_chat_history)        

    
# with table_tab:
#     data = np.random.randn(10, 1)

#     tab1.subheader("A tab with a chart")
#     tab1.line_chart(data)
