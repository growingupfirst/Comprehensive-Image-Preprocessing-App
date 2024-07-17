import os
import shutil
import streamlit as st
from streamlit_lottie import st_lottie_spinner
#---SETTING PARAMETERS---
# Source directory containing all the folders
SOURCE_DIRECTORY = "D:\\cleaned_datasets"
# Destination directory where the renamed files will be copied
DESTINATION_DIRECTORY = "D:\\cocos"
SPINNER_PATH = 'spinner\\crownfall_meepo.json'

#---FUNCTIONS---
@st.cache_data(persist=True)
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
meepo = load_lottiefile(SPINNER_PATH)

# Iterate through the source directory and its subdirectories
def extract_coco(source_directory, destination_directory):
    file_counter = 1
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if (file == "_annotations.coco.json") or (file == '_annotations.coco.json_coco.json') or (file == '_annotations_cleared.json'):
                main_folder_name = os.path.split(root).split('/')[-1] #dataset name
                subfolder_name = os.path.basename(root) #train/valid/test
                new_filename = f"{main_folder_name}_{subfolder_name}_{file_counter}.json" 
                file_counter += 1
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_directory, new_filename)
                shutil.copyfile(source_file_path, destination_file_path)

#---HEADLINE---
st.markdown("<h1 style='text-align: center;'> COCO EXTRACTOR</h1>", unsafe_allow_html=True)
st.markdown("---")

#---WEBAPP CODE---
source_directory = st.text_input('Select the Folder where to find Cocos:', value=SOURCE_DIRECTORY)
destination_directory = st.text_input('Select the Folder to send the files to:', value=DESTINATION_DIRECTORY)

sbm_btn = st.button('Submit')
if sbm_btn:
    with st_lottie_spinner(meepo, key='lol', height=32, width=32):
        extract_coco(source_directory, destination_directory)