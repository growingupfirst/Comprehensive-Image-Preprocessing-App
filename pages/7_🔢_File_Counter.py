import streamlit as st
import os
import time 
#---FUNCTION---
def count_files_in_directory(directory):
    total_files = 0
    for root, dirs, files in os.walk(directory):
        total_files += len(files)
    return total_files

def stream_data(data):
    for symbol in data:
        yield symbol
        time.sleep(0.05)

#---SESSIONS---
# if 'metric' not in st.session_state:
#     st.session_state.metric = 0
if 'delta' not in st.session_state:
    st.session_state.delta = 0

#---CODE---
st.markdown("<h1 style='text-align: center;'> File Counter🔢</h1>", unsafe_allow_html=True)
st.markdown("---")

file_path = st.text_input('Please enter the path to count:', value="D:\\cleaned_datasets")
sbm_btn = st.button('Submit')
if sbm_btn:
    total_files = count_files_in_directory(file_path)
    metric = st.metric('Total Files', value=total_files)
    #st.session_state.delta = st.session_state.metric
    st.write_stream(stream_data(f"Total number of files in {file_path} and its subfolders: {total_files}"))

