#### LOAD PACKAGES ####
import os 
import numpy as np
import cv2
import mrcnn.config
import mrcnn.utils
from mrcnn.model import MaskRCNN
import tensorflow as tf 
import matplotlib.pyplot as plt
import pandas as pd
import xml.etree.ElementTree as ET
from keras.preprocessing.image import img_to_array
from mrcnn import visualize
from keras.preprocessing.image import load_img
from os.path import isfile, join
from video.py import pics_to_vid
#########################

# Set dir 
os.chdir('/Path/to/dir')

# Path to COCO
Coco_path = '/Path/to/Coco'

# Config 
class Config(mrcnn.config.Config):
    NAME = "coco_pretrained_model_config"
    IMAGES_PER_GPU = 1
    GPU_COUNT = 1
    NUM_CLASSES = 81
    DETECTION_MIN_CONFIDENCE = 0.25

config = Config()
config.display()

# Model
model = MaskRCNN(mode="inference", model_dir='/Path/to/Model', config=Config())
model.load_weights(Coco_path, by_name=True)

# Video
Video_path = "/Path/to/video/vidoe.mp4"
VIDEO = cv2.VideoCapture(Video_path)

# Function for later use 
def get_car_boxes(boxes, class_ids):
    car_boxes = []

    for i, box in enumerate(boxes):
        # If the detected object isn't a car / truck, skip it
        if class_ids[i] in [3, 8, 6]:
            car_boxes.append(box)

    return np.array(car_boxes)


# Capture the first frame #
while(VIDEO.isOpened()):
    ret, frame = VIDEO.read()
    i = 1
    cv2.imwrite('test_pic.jpg',frame)
    break

test_image = load_img('/Path/to/pic/test_pic.jpg')
plt.imshow(test_image)


# Load the coordinates created by the YOLO tool 
tree = ET.parse('Path/to/coordinates.xml')
root = tree.getroot()
coord = pd.DataFrame(columns = ['xmin','ymin','xmax','ymax'], data = np.zeros((len(root.findall('object/bndbox/xmin')),4)))
step = 0
for j,z in enumerate(['xmin','ymin','xmax','ymax']):
    strin = "object/bndbox/" + z
    for x in root.findall(strin):
        if step % len(root.findall('object/bndbox/xmin')) == 0:
            step = 0
        coord.iloc[step,j] = int(x.text)
        step = step + 1

park_coordinates = np.array(coord)
park_coordinates = park_coordinates.astype(int)


# Load class names to visualize model prediction
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

# Predict the first frame
img = img_to_array(test_image)
results = model.detect([img], verbose=0)
r = results[0]
visualize.display_instances(img, r['rois'], r['masks'], r['class_ids'],class_names, scores = r['scores'])

# Main function: Open video - get frame - predict - paint pic - save
VIDEO.release()
cv2.destroyAllWindows()
VIDEO = cv2.VideoCapture(Video_path)
# Open
while VIDEO.isOpened():
    success, frame = VIDEO.read()
    if not success:
        break
    # Frame
    frameId = int(round(VIDEO.get(1)))
    name = "pic" + str(frameId) + ".jpg"
    cv2.imwrite(name, frame)
    path = 'Path/to/store/pics' + name
    
    # Reload frame. This is due to the model predicting better when keras is reading the pic
    frame_n = load_img(path, target_size = [2160,3840])
    
    rgb_image = img_to_array(frame_n)
    
    results = model.detect([rgb_image], verbose=0)
    r = results[0]
    detected_cars = get_car_boxes(r['rois'], r['class_ids'])
    
    # Change the column places 
    permutation = [1, 0, 3, 2]
    idx = np.empty_like(permutation)
    idx[permutation] = np.arange(len(permutation))
    detected_cars = detected_cars[:, idx]
    
    # Calculate overlap
    overlaps = mrcnn.utils.compute_overlaps(detected_cars,park_coordinates)
    overlaps = overlaps.transpose()
    
    free_space = False
    for parking_area, overlap_areas in zip(park_coordinates, overlaps):
        max_IoU_overlap = np.max(overlap_areas)
        x1, y1 ,x2, y2 = parking_area
        
        if max_IoU_overlap < 0.1:
            # Parking space not occupied = green box 
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            free_space = True
        else:
            # Parking space is still occupied - red box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, f"{max_IoU_overlap:0.2}", (x1 + 6, y2 - 6), font, 0.3, (255, 255, 255))
        
        # Save pic
        cv2.imwrite('Path/to/store/pics'+ str(frameId)+'.jpg', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
VIDEO.release()
cv2.destroyAllWindows()


pathIn= '/Path/to/pics'
pathOut = '/Path/to/save/video/video.mp4'

pics_to_vid(pathIn,pathOut)









