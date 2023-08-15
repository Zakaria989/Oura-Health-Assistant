from dotenv import load_dotenv
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import shutil
import os
import subprocess

# Load api from .env
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

#Data path to get data 
DATA_PATH = "data/csv"

#Data path to save embeddings
DB_FAISS_PATH = "data/db_faiss"

# Create a vector database
def create_vector_db():
    if os.path.exists(DB_FAISS_PATH):
        overwrite = input("Vector store already exists do you want to override? (y/n): ")
        if overwrite.lower() == 'y':
            shutil.rmtree(DB_FAISS_PATH)
        else:
            print("Vectore store were not override exiting...")
            return
       
    print("Loading the file")
    #Load the csv files as chunks   
    loader = DirectoryLoader(DATA_PATH,glob="*.csv", loader_cls=CSVLoader)
    data = loader.load()
    
    print("Creating embeddings")
    #Creating embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-ada-002")
    
    print("Storing embeddings in database")
    #Creating vector store
    db = FAISS.from_documents(data,embeddings)
    db.save_local(DB_FAISS_PATH)
 
 
#run oura_data.py
def run_oura_data():
    subprocess.run(["python","oura_data.py"])

if __name__ == "__main__":
    run_oura_data()
    create_vector_db()
    