import streamlit as st
from pycocotools.coco import COCO
import json
import os 
import tkinter as tk
from tkinter import filedialog

#---DEFAULT PARAMETERS---


SOURCE_FILE = 'output.json'
temp_json = {
    'info': {},
    'licenses':[],
    'categories':[],
    'images':[],
    'annotations':[]
}
#---FUNCTIONS---

def select_folder():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    folder_path = filedialog.askdirectory(master=root)
    return folder_path

def coco_merge(
    input_extend: str, input_add: str, output_file: str, indent = None,
) -> str:
    """Merge COCO annotation files.

    Args:
        input_extend: Path to input file to be extended.
        input_add: Path to input file to be added.
        output_file : Path to output file with merged annotations.
        indent: Argument passed to `json.dump`. See https://docs.python.org/3/library/json.html#json.dump.
    """
    with open(input_extend, "r") as f:
        data_extend = json.load(f)
    with open(input_add, "r") as f:
        data_add = json.load(f)

    output = {
        k: data_extend[k] for k in data_extend if k not in ("images", "annotations")
    }

    output["images"], output["annotations"] = [], []

    for i, data in enumerate([data_extend, data_add]):
        print(f'Processing {input_add}')
        print(
            "Input {}: {} images, {} annotations".format(
                i + 1, len(data["images"]), len(data["annotations"])
            )
        )

        cat_id_map = {}
        for new_cat in data["categories"]:
            new_id = None
            for output_cat in output["categories"]:
                if new_cat["name"] == output_cat["name"]:
                    new_id = output_cat["id"]
                    break

            if new_id is not None:
                cat_id_map[new_cat["id"]] = new_id
            else:
                try:
                    new_cat_id = max(c["id"] for c in output["categories"]) + 1
                except ValueError:
                    new_cat_id = 0
                cat_id_map[new_cat["id"]] = new_cat_id
                new_cat["id"] = new_cat_id
                output["categories"].append(new_cat)

        img_id_map = {}
        for image in data["images"]:
            n_imgs = len(output["images"])
            img_id_map[image["id"]] = n_imgs
            image["id"] = n_imgs

            output["images"].append(image)

        for annotation in data["annotations"]:
            n_anns = len(output["annotations"])
            annotation["id"] = n_anns
            annotation["image_id"] = img_id_map[annotation["image_id"]]
            annotation["category_id"] = cat_id_map[annotation["category_id"]]

            output["annotations"].append(annotation)

    print(
        "Result: {} images, {} annotations".format(
            len(output["images"]), len(output["annotations"])
        )
    )

    with open(output_file, "w") as f:
        json.dump(output, f, indent=indent)

    return output_file

def merge_coco_json(input_path, output_file):
    if len(os.listdir(input_path)) == 0:
        st.warning('The directory is empty!')
    else:
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)
        progress_step = 100 / len(os.listdir)
        begin = 0
        for file in os.listdir(input_path):
            if file.endswith('json'):
                file_path = os.path.join(input_path, file)
                coco_merge(output_file, file_path, output_file)
                my_bar.progress(begin+progress_step, progress_text)

#---DEFAULT PARAMETERS--

#---FUNCTIONS---

#---HEADLINE---
st.markdown("<h1 style='text-align: center;'> COCO MERGER</h1>", unsafe_allow_html=True)
st.markdown("---")

#---MERGER---
input_folder_path = st.session_state.get("input_folder_path", None)
output_folder_path = st.session_state.get("output_folder_path", None)
input_button = st.button("Select Input Folder")
if input_folder_path != None:
    input_path = st.text_input('Please set up the path to folder for the input', value=input_folder_path)
output_button = st.button("Select Output Folder")
if output_folder_path != None:
    output_path = st.text_input('Please set up the folder for the output:', value=output_folder_path)
if input_button:
    selected_folder_path = select_folder()
    st.session_state.input_folder_path = selected_folder_path
    input_path = st.text_input('Please set up the path to folder for the input', value=selected_folder_path)
    print('here!')
if output_button:
    selected_folder_path = select_folder()
    st.session_state.output_folder_path = selected_folder_path
    output_path = st.text_input('Please set up the folder for the output:', value=selected_folder_path)
    print('there')
submit_btn = st.button('Submit') #on_click(merge)
if submit_btn:
    if os.path.isdir(input_path) and os.path.isdir(output_path):
        output_file = output_path + '\\annotations_coco_merged.json'
        with open(output_file, 'w', encoding="ISO-8859-1") as f:
            json.dump(temp_json, f, indent=4, ensure_ascii=False)
        merge_coco_json(input_path, output_file)