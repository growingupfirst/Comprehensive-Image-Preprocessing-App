from sahi.slicing import slice_coco
import os
import streamlit as st
from streamlit_lottie import st_lottie_spinner
import json
import zipfile

SPINNER_PATH = 'C:\\Users\\user\\Desktop\\SA\\webapp\\crownfall_meepo.json'

@st.cache_data(persist=True)
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
meepo = load_lottiefile(SPINNER_PATH)


def slice(input_folder, ds_type):
    print(input_folder)
    if ds_type == 'all':
        for idx, i in enumerate(['train', 'valid', 'test']):
            ds_type = i
            try:
                with st_lottie_spinner(meepo, key=idx, height=32, width=32): ## st.spinner(f'Processing {i}'):
                    print(f'{input_folder}\\{ds_type}')
                    coco_dict, coco_path = slice_coco(
                    coco_annotation_file_path=f'{input_folder}\\{ds_type}\\_annotations.coco.json', ##change between train/valid/test
                    image_dir=f'{input_folder}\\{ds_type}',
                    slice_height=640,
                    slice_width=640,
                    overlap_height_ratio=0.2,
                    overlap_width_ratio=0.2,
                    output_dir=f'{input_folder}_sliced\\{ds_type}',
                    output_coco_annotation_file_name='_annotations.coco.json'
                )
                    st.empty().success(f'Done {ds_type}')
            except Exception as e:
                st.empty().warning(f'{e}')
                continue

    else:
        with st_lottie_spinner(meepo, key='lol', height=32, width=32): ## st.spinner(f'Processing.')
            try:
                coco_dict, coco_path = slice_coco(
                    coco_annotation_file_path=f'{input_folder}\\{ds_type}\\_annotations.coco.json', ##change between train/valid/test
                    image_dir=f'{input_folder}\\{ds_type}',
                    slice_height=640,
                    slice_width=640,
                    overlap_height_ratio=0.2,
                    overlap_width_ratio=0.2,
                    output_dir=f'{input_folder}_sliced\\{ds_type}',
                    output_coco_annotation_file_name='_annotations.coco.json'
                )
                st.success(f'Done {ds_type}')
            except Exception as e:
                st.warning(e)


def move_to_folder(extraction_path, destination_path):

    abs_ext_path = os.path.abspath(extraction_path)
    print(abs_ext_path)
    print(destination_path)
    print(f'robocopy \"{abs_ext_path}\" \"{destination_path}\" /mt /z /e /purge')
    with st_lottie_spinner(meepo, key='lol', height=32, width=32): ## st.spinner(f'Processing.')
        os.system(f'robocopy \"{abs_ext_path}\" \"{destination_path}\" /mt /z /e /move')
        st.spinner('Processing Sliced Folder. Please wait. Everything\'s fine')
        os.system(f'robocopy \"{abs_ext_path}_sliced\" \"{destination_path}_sliced\" /mt /z /e /move')
        st.success('Succefully transferred')

def preprocess(archive):
    with st_lottie_spinner(meepo, key='lol', height=32, width=32):
        with zipfile.ZipFile(archive, 'r') as zip_ref:
                extraction_path = archive.name
                zip_ref.extractall(extraction_path)
                st.empty().success("Extraction Successful!")
                slice(extraction_path, 'all')
                # Create a new zip file with the modified images