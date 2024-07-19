## Comprehensive Image Preprocessing App 🚀

This app tries to solve multiple problems occuring during the preparation of the Object Detection datasets to train.
It includes a list of tool which can help. (At least the help me every time)

## List of tools (detailed descriptions provided down below)

- Cleaner
- Slicer
- COCO Extractor
- COCO Merger
- Voc2Coco Converter
- Paths Writer
- File Counter

⚠️Still under coding:
- COCO2YOLO (JSON2YOLO)
- Images Merger
 
## Detailed Description
### Cleaner
This tool just tries to clean the dataset folder from duplicates. Roboflow datasets can have a lot of duplicates inside. So this instrument just parses the train/valid/test folders and deletes augumentations.
**Important**. Unfortunately, it is impossible to differ between augumented and original. So the script randomly selects one.

### Slicer
Performs Sahi slicing.
**Important** At the moment the slicing is done without any settings and the final result includes even null class slices. The custom settings will be added later.

### COCO Extractor
If you have lot of datasets to combine together, that is a ready-to-go tool to extract all the `annotations.coco.json` together in one folder.

### COCO Merger
Manually rewritten `coco_merger` from pypi to merge all the Extracted annotations together in one file.
**Important** Don't forget to look at the result and delete bugged class if there are any.

### Voc2Coco Converter
Just converts VOC XML files to COCO JSON

### Paths writer
In order to train YOLO based models, you have to convert it to YOLO-format. One way to prepare the data is using JSON2YOLO. But it requires the path to all image files. This tool takes image folder as an input and writes down all the image paths to one folder.

### File counter
Basic tool which counts the files. Can be used if you need to know how much Images in total you have. (Better than using Windows Explorer calc)

### COCO2YOLO (STILL UNDER WORK)
To train Large dataset which could not be stored in Roboflow you have to convert everything by hand. This tool does everything for you easily.

### Images Merger (STILL UNDER WORK)
  Finally, after you've done everything above you may need to merge all the image from datasets together. This one is for you. 

  
