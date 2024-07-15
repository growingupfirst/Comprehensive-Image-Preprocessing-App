from sahi.slicing import slice_coco
import os
import streamlit as st
from streamlit_lottie import st_lottie_spinner
import json
import zipfile
#from cleaner import remove_duplicate_filenames, clean
import shutil

SPINNER_PATH = 'spinner\\crownfall_meepo.json'
#---FUNCTIONS---
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

#---CODE---

#---SETTING UP THE PARAMETERS---
DEFAULT_PATH = 'D:\\processed_datasets'
DEFAULT_SLICING_PATH = 'D:\\sliceable_datasets'
DEFAULT_CLEANED_PATH = 'D:\\cleaned_datasets'


if 'sbm_clicked' not in st.session_state:
    st.session_state.sbm_clicked = False

if 'mtf_clicked' not in st.session_state:
    st.session_state.sf_clicked = False


# Slicing
st.markdown("<h1 style='text-align: center;'> Slicing✂️</h1>", unsafe_allow_html=True)
st.markdown("---")
custom_slice = st.text_input('You can set the custom path to the folder if needed', value=DEFAULT_SLICING_PATH)
if custom_slice != None:
    slice_folder = st.radio('Select folder here too', options=(foldername for foldername in os.listdir(custom_slice)), key='folderlist')
data_type = st.radio('Select DataType:', options=('train', 'valid', 'test', 'all'))
slicer_button = st.button('Submit', key='sl_btn')
if slicer_button:
    if (custom_slice != None) and (slice_folder != None):
        slice_path = custom_slice + '\\' + slice_folder
        with st.spinner('Please wait...'): 
            slice(slice_path, data_type)
        st.success('Slicing finished successfully')
    else:
        st.warning('Something is not set')

st.markdown("<h1 style='text-align: center;'> ✂️Slicing Using Archive📦 </h1>", unsafe_allow_html=True)

archive = st.file_uploader('Zipfile', type='zip')
if archive:
    submit_btn = st.button('Sumbit', on_click=preprocess, args=[archive])
    if submit_btn or st.session_state.sbm_clicked == True: #something to change here
        st.session_state.sbm_clicked = True
        show_folder_btn = st.button('Show in folder')
        move_to_folder_btn = st.button('Move to Cleaned')
        delete_btn = st.button('Delete Folders')
        explorer_path = os.path.abspath(archive.name)
        extraction_path=archive.name
        if show_folder_btn:
            print(explorer_path)
            os.startfile(os.getcwd())
        if move_to_folder_btn:
            abs_dest_path = os.path.join(DEFAULT_SLICING_PATH, extraction_path) # SUBSTITUTE SLICING WITH `CLEANED` LATER
            move_to_folder(extraction_path, abs_dest_path)
        if delete_btn:
            shutil.rmtree(archive.name)
            shutil.rmtree(f'{archive.name}_sliced')
            st.success('Deleted!')
else:
    st.session_state.sbm_clicked = False
