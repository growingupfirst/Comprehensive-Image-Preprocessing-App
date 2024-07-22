import os
import streamlit as st

#---DEFAULT PARAMS---
SOURCE_DIRECTORY = "D:\\cleaned_datasets\\"
DESTINATION_DIRECTORY = "D:\\cleaned_datasets\\images"


#---HEADLINE---
st.markdown("<h1 style='text-align: center;'> Images2Folder </h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'> Copies all images to one folder </h2>", unsafe_allow_html=True)
st.markdown("---")
# Source directory containing all the folders
source_path = st.text_input('Set the folder to look in', placeholder=SOURCE_DIRECTORY)
   # Destination directory where the files will be copied
destination_path = st.text_input('Where to put the all the images', placeholder=DESTINATION_DIRECTORY)
if source_path != '':
    folders=st.selectbox(options=os.listdir(source_path))
sbm_button = st.button('Submit')
if sbm_button and folders:
    placeholder1 = st.empty()
    placeholder2 = st.empty()
    spinner = st.spinner('Moving images')
    moved_counter = 0
    with spinner:
        for folder in folders:
            # Iterate through the source directory and its subdirectories
            for root, dirs, files in os.walk(source_path):
                for file in files:
                    if (file != "_annotations.coco.json") or (file != '_annotations.coco.json_coco.json') or (file != '_annotations_cleared.json'):
                        source_file_path = os.path.join(root, file)
                        destination_file_path = os.path.join(destination_path, file)
                        placeholder1.write(f'Moving {source_file_path} to {destination_file_path}')
                        placeholder2.write(moved_counter)
                        os.system(f'robocopy {source_file_path} {destination_file_path} /E /nfl /XO /np /mt:16 /ndl ')
                        moved_counter +=1
