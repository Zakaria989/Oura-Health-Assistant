# Oura Data to LangChain Chatbot

This project demonstrates the creation of a retrieval-based question-answering chatbot using LangChain, a library for Natural Language Processing (NLP) tasks. The chatbot leverages a pre-trained language model, text embeddings, and efficient vector storage for answering questions based on a user's Oura health data.

## General Steps
1. Obtain Oura API Key: You'll need to obtain an API key from Oura to access the user's health data.

2. Fetch and Preprocess Data: Use the provided `oura_data.py` script to fetch the user's Oura health data, including daily activity, readiness, and sleep information. The fetched data will be saved as CSV files.

3. Create Embeddings: Generate text embeddings using the sentence-transformers library. These embeddings convert text data into a dense vector space, allowing for efficient semantic analysis. We use the "all-MiniLM-L6-v2" model from Hugging Face.

4. Create Vector Store: Utilize the faiss library to establish a vector store for saving the generated text embeddings. FAISS provides an efficient way to search for similar vectors.

5. Build the Chatbot: Implement the retrieval-based question-answering chatbot using LangChain components. Load the LLama 2 model, set up a QA chain with custom prompt templates, and use FAISS for retrieving relevant answers.

6. Interface with Streamlit: Create a user-friendly interface for the chatbot using Streamlit. Users can ask questions about their Oura health data, and the chatbot will provide relevant answers based on the user's input and their health data.

## How to Run

1. Run `oura_data.py`: Execute the command `python oura_data.py` to fetch and preprocess the user's Oura health data. The data will be saved in CSV files.

2. Run `ingest.py`: Execute the command `python ingest.py` to create embeddings from the generated CSV files and save them using the FAISS vector store.

3. Run the Chatbot: Run the chatbot interface using Streamlit. Execute the command `streamlit run app.py` to start the chatbot.

### oura_data.py
This script fetches the user's Oura health data using the Oura API, preprocesses it, and saves it as CSV files. It includes functions to fetch and return activity, readiness, and sleep information.

### ingest.py
This script uses LangChain to create text embeddings from the CSV files containing Oura health data. The embeddings are then stored using the FAISS vector store for efficient retrieval.

### app.py
The Streamlit application that provides an interactive interface for the retrieval-based question-answering chatbot. Users can ask questions about their Oura health data, and the chatbot will respond with relevant answers based on the user's input and their health data.

## Background

The goal of this project is to better understand Oura health information, but it can also be adapted to retrieve information from other CSV files.:

1. Quantized Model: We utilize a quantized version of the LLama 2 chat model from Hugging Face, optimized for power consumption and performance.
    * I tried two different models both dolphin-llama2-7b.ggmlv3.q8_0.bin, and llama-2-7b-chat.ggmlv3.q8_0.bin, I personally did not see much different in performance

2. CTransformers: The ctransformers library is used to load the quantized LLama 2 model. It provides Python bindings for efficient transformer model implementations in C/C++.

3. Sentence Transformers: We use the "all-MiniLM-L6-v2" model from Hugging Face to generate text embeddings, enabling efficient semantic analysis.

4. FAISS Vector Store: The FAISS library is employed to create a vector store for the text embeddings, allowing for efficient vector similarity search.

5. Streamlit Interface: The chatbot interface is created using Streamlit, providing an intuitive way for users to interact with the chatbot and receive health-related answers.

## Fixes and Improvements

- Refine LLama Model: Explore different LLama models (e.g., GPT) or fine-tune existing models to improve answer quality.
- Enhanced Data Support: Modify the code to handle multiple CSV files and provide coherent answers across datasets.
- Streamlit Enhancements: Improve the visual design and user experience of the Streamlit interface.
- Expand Health Data: Extend the chatbot's capabilities to provide information about heart rate, workouts, sessions, and more.
- Personalized Information: Enhance the chatbot to consider daily health trends and provide more personalized answers.
- Add Tags and Metadata: Implement a tagging system to associate metadata with health data and improve retrieval accuracy.

## Usage
- Upon starting the chatbot, users can ask health-related questions, and the bot will respond with relevant answers.
- The bot provides information about the user's Oura health data based on the fetched and processed CSV files.
- Users can interact with the chatbot through the Streamlit interface and receive health insights and advice.

## Disclaimer
This project is intended for educational and learning purposes, bugs might occur :). 
P.S. The chatbot's responses should not replace professional medical advice.
