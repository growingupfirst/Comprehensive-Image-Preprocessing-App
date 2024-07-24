import os
import random
import shutil
from pathlib import Path

# Parameters
image_folder = Path('images')
print(image_folder)
label_folder = Path('labels')
output_folders = {
    'train': {'images': image_folder / 'train', 'labels': label_folder / 'train'},
    'test': {'images': image_folder / 'test', 'labels': label_folder / 'test'},
    'val': {'images': image_folder / 'val', 'labels': label_folder / 'val'}
}
train_ratio = 0.7
test_ratio = 0.2
val_ratio = 0.1

# Ensure output directories exist
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

def copy_files(files, split_name):
    print(len(files))
    for image_path in files:
        try:
            print(f'Copying {image_path}')
            label_path = label_folder / 'output' /(image_path.stem + '.txt')
            print(f'Copying TO {output_folders[split_name]['images'] / image_path.name}')
            shutil.move(image_path, output_folders[split_name]['images'] / image_path.name)
            shutil.move(label_path, output_folders[split_name]['labels'] / label_path.name)
        except:
            continue
# Copy files to corresponding directories
copy_files(train_files, 'train')
copy_files(test_files, 'test')
copy_files(val_files, 'val')

print("Dataset split completed successfully!")
