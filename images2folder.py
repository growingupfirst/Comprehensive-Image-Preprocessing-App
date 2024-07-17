import os
import shutil

folders=['military', 'aircrafts']

for folder in folders:
    # Source directory containing all the folders
    source_directory = f"D:\\cleaned_datasets\\{folder}"

    # Destination directory where the files will be copied
    destination_directory = "D:\\cleaned_datasets\\new_dir"

    # Iterate through the source directory and its subdirectories
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if (file != "_annotations.coco.json") or (file != '_annotations.coco.json_coco.json') or (file != '_annotations_cleared.json'):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_directory, file)
                shutil.copyfile(source_file_path, destination_file_path)
