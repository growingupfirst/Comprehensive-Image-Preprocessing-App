import os
import streamlit as st

#---FUNCTIONS---
def parse_folder_to_txt(folder_path, output_file):
    with open(output_file, 'w') as file:
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                file.write(os.path.join(root, filename) + '\n')
    st.success('Finished Successfully')

folder_path = 'C:\\Users\\user\\Downloads\\DroneTestDataset\\Drone_TestSet_XMLs'
output_file = 'C:\\Users\\user\\Downloads\\DroneTestDataset\\paths.txt'

#parse_folder_to_txt(folder_path, output_file)
#---CODE---

#---HEADLINE---
st.markdown("<h1 style='text-align: center;'> Path Writer </h1>", unsafe_allow_html=True)
st.markdown("---")

f_path = st.text_input('Please, write the path to the folder to save paths:', value=folder_path)
output_name = st.text_input('Write the output file name', value=output_file)
sbm_button = st.button('Submit', on_click=parse_folder_to_txt, args=[f_path, output_name,])
