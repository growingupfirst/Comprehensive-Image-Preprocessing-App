import streamlit as st
from pycocotools.coco import COCO
import json
import io

#---FUNCTIONS---

#---DEFAULT PARAMETERS---

#---FUNCTIONS---
def merge_coco_json(json_files, output_file):
    merged_annotations = {
        "info": {},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }

    image_id_offset = 0
    annotation_id_offset = 0
    category_id_offset = 0
    existing_category_ids = set()

    for idx, file in enumerate(json_files):
        data = json.loads(file.read())
        temp_json = 'temp.json'
        with open(temp_json, 'w') as f:
            json.dump(data, f)
        
        coco = COCO(temp_json)
        print(coco)

        # Update image IDs to avoid conflicts
        for image in coco.dataset['images']:
            image['id'] += image_id_offset
            merged_annotations['images'].append(image)

        # Update annotation IDs to avoid conflicts
        for annotation in coco.dataset['annotations']:
            annotation['id'] += annotation_id_offset
            annotation['image_id'] += image_id_offset
            merged_annotations['annotations'].append(annotation)

        # Update categories and their IDs to avoid conflicts
        for category in coco.dataset['categories']:
            if category['id'] not in existing_category_ids:
                category['id'] += category_id_offset
                merged_annotations['categories'].append(category)
                existing_category_ids.add(category['id'])

        image_id_offset = len(merged_annotations['images'])
        annotation_id_offset = len(merged_annotations['annotations'])
        category_id_offset = len(merged_annotations['categories'])

    # Save merged annotations to output file
    with open(output_file, 'w') as f:
        json.dump(merged_annotations, f)
    st.success('Successfully merged')

#---HEADLINE---
st.markdown("<h1 style='text-align: center;'> COCO MERGER</h1>", unsafe_allow_html=True)
st.markdown("---")

#---MERGER---

annotations = st.file_uploader('Please drag and drop COCO json files here',accept_multiple_files=True, type='json')
output_path = st.text_input('Please set up the folder for the output:', value='C:\\Users\\user\\Downloads')
submit_btn = st.button('Submit') #on_click(merge)
if submit_btn:
    output_file = output_path + '\\annotations_coco_merged.json'
    merge_coco_json(annotations, output_file)