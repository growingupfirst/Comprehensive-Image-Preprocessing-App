import os, json
import streamlit as st

#---SETTING UP THE PARAMETERS---
DEFAULT_PATH = 'D:\\processed_datasets'
DEFAULT_SLICING_PATH = 'D:\\sliceable_datasets'
DEFAULT_CLEANED_PATH = 'D:\\cleaned_datasets'

# setting up the functions
def remove_duplicate_filenames(file_list):
    unique_names = []
    #search for .rh to file the real name
    for filename in file_list:
        if '.rf' in filename:
            index_rf = filename.index('.rf')
            if filename[:index_rf] not in [name[:index_rf] for name in unique_names]:
                    unique_names.append(filename)
            else:
                os.remove(filename)    
    return unique_names

def clean(folder_path):
     for folder in os.listdir(folder_path):
        images_path_test = f'{folder}/test'
        images_path_train = f'{folder}/train'
        images_path_val = f'{folder}/valid'
        
        image_paths = [images_path_test, images_path_train, images_path_val]
        
        for path in image_paths:
            try:
                os.chdir(f'../../{path}')
            except FileNotFoundError:
                try:
                    os.chdir(f'{path}')
                except FileNotFoundError:
                    continue   
            # open annot file
            annotation_file = '_annotations.coco.json'
            with open(annotation_file, 'r') as file:
                data = json.load(file)
            # list of pictures
            filenames = os.listdir()
            unique_files = remove_duplicate_filenames(filenames)
            print(f'Cleaning folder: {folder}')
            print("Unique filenames after removing duplicates:", len(unique_files))
            print("The number of annotations before cleaning:", len(data['annotations']))
        
            #clearing annotation file
            image_ids = []
            for file in unique_files:
                for line in data['images']:
                    if file in line['file_name']:
                        image_ids.append(line['id'])
            print('The number of Image IDs', len(image_ids)) 
            
            #finding which lines for unique pictures to take
            nesessary_lines = [line for line in data['annotations'] if line['image_id'] in image_ids]
            print(len(nesessary_lines))
        
            #substitute the annotations
            data['annotations'] = nesessary_lines
            #save new annotation file
            with open('_annotations_cleared.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        os.chdir(folder_path)

#---CODE---
#---Cleaning---
st.markdown("<h1 style='text-align: center;'> Annotation Cleaner🧹</h1>", unsafe_allow_html=True)
st.markdown("---")
custom_clean = st.text_input('You can set the custom path to the folder if needed', value=DEFAULT_PATH)
cleaner_button = st.button('Submit')
if cleaner_button:
    if custom_clean != None:
        os.chdir(custom_clean)
        clean(custom_clean)
        print('Successfully cleaned')
    else:
        os.chdir(DEFAULT_PATH)
        clean(DEFAULT_PATH)
        print('Successfully cleaned')