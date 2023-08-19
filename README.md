# LangChain Health Chatbot

This project showcases a chatbot designed to interact with users using LangChain, a library for Natural Language Processing (NLP) tasks. The chatbot integrates with health data from the Oura API, allowing users to ask health-related questions and receive insights and advice. The chatbot leverages OpenAI's GPT-based models for conversational capabilities and utilizes the FAISS library for efficient text embedding storage.

## Features

- **Data Collection:** The `oura_data_tocsv.py` script fetches health data from the Oura API, processes it, and saves it as CSV files.

- **Embeddings:** The `embedder.py` script generates text embeddings from CSV files using OpenAIEmbeddings and stores them in the FAISS vector store.

- **Interactive Chat:** The Streamlit-based interface allows users to interact with the chatbot, asking health-related questions and receiving relevant responses.

- **Conversational Insights:** Users can use the chatbot to obtain insights from their health data, visualize trends, and get advice.

## Getting Started

1. **Set Up API Keys:** Obtain API keys for the Oura API and OpenAI. Add these keys to your environment variables.

2. **Fetch Oura Data:** Run `python oura_data_tocsv.py <OURA_API_KEY> <START_DATE> <END_DATE>` to fetch and preprocess health data from the Oura API.

3. **Generate Embeddings:** Run `python embedder.py <OPENAI_API_KEY>` to create text embeddings and store them using the FAISS vector store.

4. **Run the Chatbot:** Launch the chatbot interface using `streamlit run Home.py`.

## Interface Overview

The interface consists of three main components:

1. **User Authentication:** Users can log in with their Oura API and OpenAI API keys to access their health data.

2. **Data Selection:** Users provide a time period for data analysis, and the chatbot fetches and processes the data.

3. **Chatbot Interaction:** Users can ask questions about their health data and receive insightful responses from the chatbot. The chatbot integrates GPT-based models to provide conversational capabilities.

## Next Steps

- **Enhanced Visualization:** Improve data visualization by incorporating charts and graphs based on user input and health data.

- **Personalized Insights:** Implement algorithms to provide personalized health insights based on trends and patterns in the data.

- **Mobile Accessibility:** Ensure the chatbot interface is responsive and accessible on mobile devices.

- **User Profiles:** Enable users to create profiles and save preferences for a more personalized experience.

- **Continuous Improvement:** Collect user feedback to refine the chatbot's functionality, improve response accuracy, and add new features.

## Disclaimer

This project is intended for educational purposes.

## Acknowledgments

This project utilizes LangChain for NLP tasks, OpenAI for conversational capabilities, and the FAISS library for efficient text embedding storage.
