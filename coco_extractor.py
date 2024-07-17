import os
import shutil

# Function to find all files with a specific name in a directory and its subdirectories
def find_files(directory, filename):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == filename:
                yield os.path.join(root, file)

# Source directory containing all the folders
source_directory = "D:\\cleaned_datasets"

# Destination directory where the renamed files will be copied
destination_directory = "D:\\cocos"

# Iterate through the source directory and its subdirectories
file_counter = 1
for root, dirs, files in os.walk(source_directory):
    for file in files:
        if (file == "_annotations.coco.json") or (file == '_annotations.coco.json_coco.json') or (file == '_annotations_cleared.json'):
            folder_name = os.path.basename(root)
            new_filename = f"{folder_name}_{file_counter}.json"
            file_counter += 1
            source_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_directory, new_filename)
            shutil.copyfile(source_file_path, destination_file_path)
