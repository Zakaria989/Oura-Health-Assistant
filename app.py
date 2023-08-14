import streamlit as st 
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers, OpenAI
from langchain.chains import ConversationalRetrievalChain

DB_FAISS_PATH = "data/db_faiss"


#Loading the model
def load_llm():
    llm = CTransformers(
        model="llama-2-7b-chat.ggmlv3.q8_0.bin",
        model_type="llama",
        max_new_tokens = 512,
        temperature = 0.6
    )
    return llm



st.title("Chat with your OURA data")

embeddings = HuggingFaceEmbeddings(model_name ="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device':'cuda'})

db = FAISS.load_local(DB_FAISS_PATH,embeddings)
llm = load_llm()
chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever= db.as_retriever())


def conversational_chat(query):
    print("Running query")
    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query,result["answer"]))
    print(result["answer"])
    return result["answer"]

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)



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
            
            