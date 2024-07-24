import os
import random
import streamlit as st
import shutil
from pathlib import Path

#---CONFIG---
# if 'train' not in st.session_state:
#     st.session_state.train = 0.7
#     st.session_state.val = 0.2
#     st.session_state.test = 0.1

#---FUNCTIONS---
def copy_files(files, split_name, output_folders):
    placeholder = st.empty()
    for image_path in files:
        try:
            label_path = label_folder / 'output' /(image_path.stem + '.txt')
            placeholder.write(f'Copying {image_path}\nCopying TO {output_folders[split_name]['images'] / image_path.name}')
            shutil.move(image_path, output_folders[split_name]['images'] / image_path.name)
            shutil.move(label_path, output_folders[split_name]['labels'] / label_path.name)
        except:
            continue

def split_data(image_folder, label_folder):
# Parameters
    output_folders = {
        'train': {'images': image_folder / 'train', 'labels': label_folder / 'train'},
        'test': {'images': image_folder / 'test', 'labels': label_folder / 'test'},
        'val': {'images': image_folder / 'val', 'labels': label_folder / 'val'}
    }
    train_ratio = 0.7
    test_ratio = 0.2
    val_ratio = 0.1
    for key, paths in output_folders.items():
        paths['images'].mkdir(parents=True, exist_ok=True)
        paths['labels'].mkdir(parents=True, exist_ok=True)

    # Get list of images and corresponding labels
    images = list(image_folder.glob('*.jpg')) + list(image_folder.glob('*.png'))
    labels = list(label_folder.glob('*.txt'))

    # Shuffle images
    random.shuffle(images)

    # Split data
    total_images = len(images)
    print(total_images)
    train_split = int(train_ratio * total_images)
    test_split = int(test_ratio * total_images)
    val_split = total_images - train_split - test_split

    train_files = images[:train_split]
    test_files = images[train_split:train_split + test_split]
    val_files = images[train_split + test_split:]
    # Copy files to corresponding directories
    copy_files(train_files, 'train', output_folders)
    copy_files(test_files, 'test', output_folders)
    copy_files(val_files, 'val', output_folders)

    st.success("Dataset split completed successfully!")

# def update(slider):
#     if slider == 'train':
#         st.session_state.val = 1 - st.session_state.train - st.session_state.test
#         st.session_state.test = 1 - st.session_state.train - st.session_state.test
#     else: 
#         st.session_state.train = 1 - st.session_state.val - st.session_state.test
#---HEADLINE---
st.markdown("<h1 style='text-align: center;'> Data Splitter ✂️</h1>", unsafe_allow_html=True)
st.markdown("---")

#---CODE---

path_input = st.text_input('Please set the folder with images/labels:', placeholder="C:\\Users")
train_ratio = st.slider('Train Ratio', key='train', min_value=0.1, max_value=0.9, value=0.7, step=0.1) #value=st.session_state.train, on_change=update, args=('train',))
val_ratio = st.slider('Val Ratio', key='val', min_value=0.1, max_value=0.9, value=0.2, step=0.1) #value=st.session_state.train, on_change=update, args=('valid',))
test_ratio = st.slider('Test Ratio', key='test', min_value=0.1, max_value=0.9, value=0.1, step=0.1) #value=st.session_state.train, on_change=update, args=('test',))

if path_input:
    image_folder = Path(path_input / 'images')
    label_folder = Path(path_input / 'labels')
# Ensure output directories exist
sbm_btn = st.button('Submit')


if sbm_btn: 
    if (train_ratio+val_ratio+test_ratio) != 1.0:
        st.warning("The sum of Train, Test, and Validation ratios must be equal to 1.")
    else:
        with st.spinner('Splitting Data...'):
            split_data(image_folder, label_folder)



