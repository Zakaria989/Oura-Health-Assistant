from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import numpy as np
import time
import os
import openai
import json


# Load api from .env
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

DB_FAISS_PATH = "data/db_faiss"

#Path to our csv data
DATA_PATH = "data/csv"


# Context and other prompts
context = """context: Given the information the user gives you, with your own information find the correct column 
    titles that fit the description, and return them like this 'x = {column name for x}, y = {column name for y}'. Be sure to give 
    the correct column name, watch out for big and small letters, example for what you should return:
    
    To plot your activity steps against your sleep duration, you can use the following column titles:

        1. X-axis: Steps
        2. Y-axis: Sleep Duration
    """



if 'history' not in st.session_state:
    st.session_state['history'].append((
        "Be sure to follow this ->",context))

if 'chart_messages' not in st.session_state:
    st.session_state['chart_messages'] = []


# Function that checks if file contains column
def csv_file_exists(data_path,column):
    # Search for csv files in data path
    csv_files = os.listdir(data_path)
    column_data_file = None
    for file in csv_files:
        file_path = os.path.join(DATA_PATH,file)
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            if column in df.columns:
                column_data_file = file_path
        if column_data_file :
            break
    if not column_data_file:
        st.error(f"Sorry, a column for {column} does not exists")
        return None
    else:
        return column_data_file
        

# Function that is going to be called from gpt
def plot(x,y):
    # Search for csv files in data path
    x_data_file = csv_file_exists(DATA_PATH,x)
    y_data_file = csv_file_exists(DATA_PATH,y)
    
    # Load data from found csv files
    x_df = pd.read_csv(x_data_file)
    y_df = pd.read_csv(y_data_file)
    
    # set up streamlit widgets
    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    chart = st.line_chart()
    
    # Hold the x and y values
    x_values = []
    y_values = []
    # Loop through our x and y files
    for i in range(len(x_df)):
        x_values.append(x_df.loc[i,x])
        y_values.append( y_df.loc[i,y])
        
    x_df_values = pd.DataFrame({x:x_values})
    y_df_values = pd.DataFrame({y:y_values})

    values = pd.concat([x_df_values,y_df_values],axis=1)
    # status_text.text("%i%% Complete" % ((i+1) /len(x_df)*100))
    values.set_index(x,inplace=True)
    chart.add_rows(values)
    # progress_bar.progress((i+1)/len(x_df)*100)
    # time.sleep(0.05)

    progress_bar.empty()


# Loading the model
def load_llm():
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-0613",
        openai_api_key=openai_api_key,
    )
    return llm

def run_conversation(query):
    # Step 1: send the conversation and available functions to GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages = [{"role": "user", "content": query}],    
        functions=[
            {
                "name": "plot",
                "description": "Generate a plot by plotting values of the x-axis column against the y-axis column.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "x": {
                            "type": "string",
                            "description": "Title of the column to be plotted on the x-axis.",
                        },
                        "y": {
                            "type": "string",
                            "description": "Title of the column to be plotted on the y-axis. Values from this column will be plotted against the x-axis column.",
                        }
                    },
                    "required": ["x", "y"],
                    "description": "Specify both the x and y columns to create the plot."
                }
            }
        ],
        function_call = "auto",
    )  
    response_message = response["choices"][0]["message"]
    # Check if GPT want to call the function
    if response_message.get("function_call"):
        function_args = json.loads(response_message["function_call"]["arguments"])
        # Calling the function
        plot(function_args["x"], function_args["y"])
        # Update messages
        st.session_state.chart_messages.append({"role":"assistant","content":response_message})
    
    return response_message



def conversational_chat(query):
    print("Running query")
        
    st.session_state['history'].append((
        "Be sure to follow this ->",context))
    result = chain({"question": query, "chat_history": st.session_state['history']})
    
    print("Result to FUNCTION GPT:",result["answer"])
    print("\n")
    
    response = run_conversation(result["answer"])
    st.session_state['history'].append((query,result["answer"]))
    

    print("\n\t")
    print("\n")
    print(response)
 

    return result["answer"]


st.set_page_config(page_title="Plots", page_icon="📈")

st.markdown("# What chart do you want to visualize?")
st.sidebar.header("Plotting charts")
st.sidebar.write(
    """This demo illustrates function calling with GPT, calling a function that plots"""
)





embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-ada-002")
db = FAISS.load_local(DB_FAISS_PATH,embeddings)
llm = load_llm()
chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever())


# Handle user input and return assistant answer 
if user_input := st.text_input("Enter your message"):
    st.session_state.chart_messages.append({"role": "user", "content": user_input})
    if st.button(label="Get plot"):
        if st.session_state.chart_messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = conversational_chat(user_input)
                    placeholder = st.empty()
            message = {"role": "assistant", "content": response}
            st.session_state.chart_messages.append(message)
            with st.chat_message("assistant"):
                st.write(response)




