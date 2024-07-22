import os
import json
import xml.etree.ElementTree as ET
import streamlit as st
from streamlit_lottie import st_lottie_spinner
#--DEFAULT PARAMETERS---

DEFAULT_XML_FOLDER = 'C:\\Users\\user\\Downloads\\DroneTrainDataset\\Drone_TrainSet_XMLs'
DEFAULT_OUTPUT_FILE = 'C:\\Users\\user\\Downloads\\DroneTrainDataset\\annotations_coco.json'
SPINNER_PATH = 'spinner\\crownfall_meepo.json'

#---FUNCTION---
@st.cache_data(persist=True)
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
    
meepo = load_lottiefile(SPINNER_PATH)

def convert_pascal_voc_to_coco(xml_folder, output_file):
    data = {
        "info": {},
        "licenses": [],
        "images": [],
        "annotations": [],
        "categories": []
    }
    bar = st.progress(0)
    # Mapping of Pascal VOC class names to COCO category IDs
    class_mapping = {}

    # Read the XML files in the folder
    for idx, filename in enumerate(os.listdir(xml_folder)):
        bar.progress(idx)
        if filename.endswith(".xml"):
            xml_file = os.path.join(xml_folder, filename)
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Extract image information
            image_info = {
                "id": len(data["images"]) + 1,
                "file_name": root.find("filename").text,
                "height": int(root.find("size/height").text),
                "width": int(root.find("size/width").text)
            }
            data["images"].append(image_info)

            # Extract object annotations
            for obj in root.findall("object"):
                category = obj.find("name").text
                if category not in class_mapping:
                    class_mapping[category] = len(class_mapping) + 1

                category_id = class_mapping[category]
                bbox = obj.find("bndbox")
                x_min = int(bbox.find("xmin").text)
                y_min = int(bbox.find("ymin").text)
                x_max = int(bbox.find("xmax").text)
                y_max = int(bbox.find("ymax").text)
                width = x_max - x_min
                height = y_max - y_min

                annotation = {
                    "id": len(data["annotations"]) + 1,
                    "image_id": image_info["id"],
                    "category_id": category_id,
                    "bbox": [x_min, y_min, width, height],
                    "area": width * height,
                    "iscrowd": 0
                }
                data["annotations"].append(annotation)

    # Create COCO categories
    for category, category_id in class_mapping.items():
        coco_category = {
            "id": category_id,
            "name": category,
            "supercategory": "object"
        }
        data["categories"].append(coco_category)

    # Save the COCO JSON file
    with open(output_file, "w") as outfile:
        json.dump(data, outfile)
    st.success('Succefully converted')


#---CODE---
st.markdown("<h1 style='text-align: center;'> Voc2Coco Converter 📦</h1>", unsafe_allow_html=True)
st.markdown("---")
xml_folder = st.text_input('Please setup the path to XML Folder:', value=DEFAULT_XML_FOLDER)
output_file = st.text_input('The path where to put the resulting JSON:',value=DEFAULT_OUTPUT_FILE)
sbm_btn = st.button('Submit')
if sbm_btn:
    with st_lottie_spinner(meepo, key='lol', height=32, width=32):
        convert_pascal_voc_to_coco(xml_folder, output_file)
