from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from datetime import datetime
import streamlit as st
import subprocess
import numpy as np

# Load API keys from .env
load_dotenv()

# Global variables
# oura_api_key = ""
# start_date = ""
# end_date = ""

def log_in_user(username, oura_api, openai_api):
    global user_logged_in
    st.session_state['user_info'] = {"username": username, "oura_api_key": oura_api, "openai_api_key": openai_api}

def re_login_user():
    global user_logged_in
    st.session_state['user_info'] = {"username": "", "oura_api_key": "", "openai_api_key": ""}

if 'user_info' not in st.session_state:
    st.session_state['user_info'] = {"username": "", "oura_api_key": "", "openai_api_key": ""}


if all(value == "" for value in  st.session_state.user_info.values()):
    st.markdown("# Welcome to your health automated")
    st.markdown("### Type some of your information below:")

    username = st.text_input(label="Username")
    oura_api_key = st.text_input(label="Oura API Key", type="password")
    openai_api_key = st.text_input(label="OpenAI API Key", type="password")
    
    if st.button(label="Login"):
        log_in_user(username, oura_api_key, openai_api_key)
        
elif all(value != "" for value in  st.session_state.user_info.values()):
    st.markdown(f"# So good to see you {st.session_state.user_info['username']}")
    
    st.markdown(f"### Put down the time period for when you want to see your data")
    start_date = st.text_input(label="Start date",placeholder="yyyy-mm-dd")
    end_date = st.text_input(label="End date",placeholder="yyyy-mm-dd")
    
    
    if st.button(label="Get data"):
        if datetime.strptime(start_date,"%Y-%m-%d") > datetime.strptime(end_date,"%Y-%m-%d"):
            st.error(body="Start date can't be greater then end date")
        else:
            subprocess.run(["python", "oura_data_tocsv.py", st.session_state.user_info["oura_api_key"], start_date, end_date])
            subprocess.run(["python", "embedder.py", st.session_state.user_info["openai_api_key"]])

with st.sidebar:
    st.button(label="Re-login", on_click=re_login_user)