import streamlit as st
import os
import numpy as np
import pandas as pd

# st.set_page_config(page_title="Tables", page_icon="🔢")



#Path to our csv data
DATA_PATH = "data/csv"

# Logic for handling multiple csv files

csv_files = [file for file in os.listdir(DATA_PATH) if file.endswith(".csv")] # Finds all the files that end with csv in our path

dfs = {} # Empty dic to store dataframes with different titles

# Loop through each CSV files and store them into the our dictionary dfs
for csv_file in csv_files:
    file_path = os.path.join(DATA_PATH,csv_file)
    df = pd.read_csv(file_path)

    dfs[csv_file[:-4]] = df


st.set_page_config(page_title="Tables", page_icon="🔢")

st.sidebar.header("Look at different parts of your data in table format")

st.markdown("# Table of your activity data")
edited_df = st.dataframe(dfs["activity_data"],use_container_width=True)


st.markdown("# Table of your readiness data")
edited_df = st.dataframe(dfs["readiness_data"],use_container_width=True)

st.markdown("# Table of your sleep data")
edited_df = st.dataframe(dfs["sleep_data"],use_container_width=True)