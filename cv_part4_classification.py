# -*- coding: utf-8 -*-
"""CV_Part4_Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13rJ_OMREkkH8hDy5aMXzhcVaz6_U7KbQ
"""

!pip install mediapipe

# mount google drive
from google.colab import drive
drive.mount('/content/drive')

# import all need libraries
import cv2 as cv
import glob
import re
import mediapipe as mp
import pandas as pd
import numpy as np
import tensorflow as tf
import os
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from keras.utils import to_categorical
from google.colab.patches import cv2_imshow

np.set_printoptions(precision=3, suppress=True)

"""DEFINING FUNCTIONS"""

#@title
#Functions

def getFeatures(file):
  mp_drawing = mp.solutions.drawing_utils
  mp_hands = mp.solutions.hands
  
  with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:

    inputImage = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    # getting ladmarks using mediapipe hands
    results = hands.process(cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB))
    pixelCoordinates = []

    # save all values as zero if no landmarks could be detected
    if not results.multi_hand_landmarks:
      handFeatures = {"actualLetter": 0,
                    "WRIST_x": 0,
                    "WRIST_y": 0,
                    "WRIST_z": 0,
                    "THUMB_CMC_x": 0,
                    "THUMB_CMC_y": 0,
                    "THUMB_CMC_z": 0,
                    "THUMB_MCP_x": 0,
                    "THUMB_MCP_y": 0,
                    "THUMB_MCP_z": 0,
                    "THUMB_DIP_x": 0,
                    "THUMB_DIP_y": 0,
                    "THUMB_DIP_z": 0,
                    "THUMB_TIP_x": 0,
                    "THUMB_TIP_y": 0,
                    "THUMB_TIP_z": 0,
                    "INDEX_MCP_x": 0,
                    "INDEX_MCP_y": 0,
                    "INDEX_MCP_z": 0,
                    "INDEX_PIP_x": 0,
                    "INDEX_PIP_y": 0,
                    "INDEX_PIP_z": 0,
                    "INDEX_DIP_x": 0,
                    "INDEX_DIP_y": 0,
                    "INDEX_DIP_z": 0,
                    "INDEX_TIP_x": 0,
                    "INDEX_TIP_y": 0,
                    "INDEX_TIP_z": 0,
                    "MIDDLE_MCP_x": 0,
                    "MIDDLE_MCP_y": 0,
                    "MIDDLE_MCP_z": 0,
                    "MIDDLE_PIP_x": 0,
                    "MIDDLE_PIP_y": 0,
                    "MIDDLE_PIP_z": 0,
                    "MIDDLE_DIP_x": 0,
                    "MIDDLE_DIP_y": 0,
                    "MIDDLE_DIP_z": 0,
                    "MIDDLE_TIP_x": 0,
                    "MIDDLE_TIP_y": 0,
                    "MIDDLE_TIP_z": 0,
                    "RING_MCP_x": 0,
                    "RING_MCP_y": 0,
                    "RING_MCP_z": 0,
                    "RING_PIP_x": 0,
                    "RING_PIP_y": 0,
                    "RING_PIP_z": 0,
                    "RING_DIP_x": 0,
                    "RING_DIP_y": 0,
                    "RING_DIP_z": 0,
                    "RING_TIP_x": 0,
                    "RING_TIP_y": 0,
                    "RING_TIP_z": 0,
                    "PINKY_MCP_x": 0,
                    "PINKY_MCP_y": 0,
                    "PINKY_MCP_z": 0,
                    "PINKY_PIP_x": 0,
                    "PINKY_PIP_y": 0,
                    "PINKY_PIP_z": 0,
                    "PINKY_DIP_x": 0,
                    "PINKY_DIP_y": 0,
                    "PINKY_DIP_z": 0,
                    "PINKY_TIP_x": 0,
                    "PINKY_TIP_y": 0,
                    "PINKY_TIP_z": 0
                    }

      return(handFeatures)

    handsModule = mp.solutions.hands
    image_height, image_width, _ = inputImage.shape

    # if landmarks are detected, normalize to the size of the input image
    for handLandmarks in results.multi_hand_landmarks:
      for point in handsModule.HandLandmark:
        normalizedLandmark = handLandmarks.landmark[point]
        coordinates = (mp_drawing._normalized_to_pixel_coordinates(normalizedLandmark.x, normalizedLandmark.y, image_width, image_height))
        if not coordinates:
          coordinates = (0,0)
        coordinates = list(coordinates)
        coordinates.append(normalizedLandmark.z)
        pixelCoordinates.append(coordinates)

    # get the letter that the symbol is supposed to represent from the file name
    actualLetter = re.search(r"\bProject Images/.*/\w", file)
    actualLetter = actualLetter.group()
    actualLetter = re.sub("Project Images/.*/", "", actualLetter)
    print("actual letter: ", actualLetter)

    # save all values into handFeatures dict
    handFeatures = {"actualLetter": actualLetter,
                    "WRIST_x": pixelCoordinates[0][0],
                    "WRIST_y": pixelCoordinates[0][1],
                    "WRIST_z": pixelCoordinates[0][2],
                    "THUMB_CMC_x": pixelCoordinates[1][0],
                    "THUMB_CMC_y": pixelCoordinates[1][1],
                    "THUMB_CMC_z": pixelCoordinates[1][2],
                    "THUMB_MCP_x": pixelCoordinates[2][0],
                    "THUMB_MCP_y": pixelCoordinates[2][1],
                    "THUMB_MCP_z": pixelCoordinates[2][2],
                    "THUMB_DIP_x": pixelCoordinates[3][0],
                    "THUMB_DIP_y": pixelCoordinates[3][1],
                    "THUMB_DIP_z": pixelCoordinates[3][2],
                    "THUMB_TIP_x": pixelCoordinates[4][0],
                    "THUMB_TIP_y": pixelCoordinates[4][1],
                    "THUMB_TIP_z": pixelCoordinates[4][2],
                    "INDEX_MCP_x": pixelCoordinates[5][0],
                    "INDEX_MCP_y": pixelCoordinates[5][1],
                    "INDEX_MCP_z": pixelCoordinates[5][2],
                    "INDEX_PIP_x": pixelCoordinates[6][0],
                    "INDEX_PIP_y": pixelCoordinates[6][1],
                    "INDEX_PIP_z": pixelCoordinates[6][2],
                    "INDEX_DIP_x": pixelCoordinates[7][0],
                    "INDEX_DIP_y": pixelCoordinates[7][1],
                    "INDEX_DIP_z": pixelCoordinates[7][2],
                    "INDEX_TIP_x": pixelCoordinates[8][0],
                    "INDEX_TIP_y": pixelCoordinates[8][1],
                    "INDEX_TIP_z": pixelCoordinates[8][2],
                    "MIDDLE_MCP_x": pixelCoordinates[9][0],
                    "MIDDLE_MCP_y": pixelCoordinates[9][1],
                    "MIDDLE_MCP_z": pixelCoordinates[9][2],
                    "MIDDLE_PIP_x": pixelCoordinates[10][0],
                    "MIDDLE_PIP_y": pixelCoordinates[10][1],
                    "MIDDLE_PIP_z": pixelCoordinates[10][2],
                    "MIDDLE_DIP_x": pixelCoordinates[11][0],
                    "MIDDLE_DIP_y": pixelCoordinates[11][1],
                    "MIDDLE_DIP_z": pixelCoordinates[11][2],
                    "MIDDLE_TIP_x": pixelCoordinates[12][0],
                    "MIDDLE_TIP_y": pixelCoordinates[12][1],
                    "MIDDLE_TIP_z": pixelCoordinates[12][2],
                    "RING_MCP_x": pixelCoordinates[13][0],
                    "RING_MCP_y": pixelCoordinates[13][1],
                    "RING_MCP_z": pixelCoordinates[13][2],
                    "RING_PIP_x": pixelCoordinates[14][0],
                    "RING_PIP_y": pixelCoordinates[14][1],
                    "RING_PIP_z": pixelCoordinates[14][2],
                    "RING_DIP_x": pixelCoordinates[15][0],
                    "RING_DIP_y": pixelCoordinates[15][1],
                    "RING_DIP_z": pixelCoordinates[15][2],
                    "RING_TIP_x": pixelCoordinates[16][0],
                    "RING_TIP_y": pixelCoordinates[16][1],
                    "RING_TIP_z": pixelCoordinates[16][2],
                    "PINKY_MCP_x": pixelCoordinates[17][0],
                    "PINKY_MCP_y": pixelCoordinates[17][1],
                    "PINKY_MCP_z": pixelCoordinates[17][2],
                    "PINKY_PIP_x": pixelCoordinates[18][0],
                    "PINKY_PIP_y": pixelCoordinates[18][1],
                    "PINKY_PIP_z": pixelCoordinates[18][2],
                    "PINKY_DIP_x": pixelCoordinates[19][0],
                    "PINKY_DIP_y": pixelCoordinates[19][1],
                    "PINKY_DIP_z": pixelCoordinates[19][2],
                    "PINKY_TIP_x": pixelCoordinates[20][0],
                    "PINKY_TIP_y": pixelCoordinates[20][1],
                    "PINKY_TIP_z": pixelCoordinates[20][2]
                    }

    return(handFeatures)

def addToFeatureFile(featureFile, handFeatures):
  if os.path.isfile(featureFile):
        # if file has already been written to, just write the newly found features
        with open(featureFile, 'a+', newline='') as file:
            # Create a writer object from csv module
            writer = csv.writer(file)
            writer.writerow([handFeatures["actualLetter"],
                    handFeatures["WRIST_x"],
                    handFeatures["WRIST_y"],
                    handFeatures["WRIST_z"],
                    handFeatures["THUMB_CMC_x"],
                    handFeatures["THUMB_CMC_y"],
                    handFeatures["THUMB_CMC_z"],
                    handFeatures["THUMB_MCP_x"],
                    handFeatures["THUMB_MCP_y"],
                    handFeatures["THUMB_MCP_z"],
                    handFeatures["THUMB_DIP_x"],
                    handFeatures["THUMB_DIP_y"],
                    handFeatures["THUMB_DIP_z"],
                    handFeatures["THUMB_TIP_x"],
                    handFeatures["THUMB_TIP_y"],
                    handFeatures["THUMB_TIP_z"],
                    handFeatures["INDEX_MCP_x"],
                    handFeatures["INDEX_MCP_y"],
                    handFeatures["INDEX_MCP_z"],
                    handFeatures["INDEX_PIP_x"],
                    handFeatures["INDEX_PIP_y"],
                    handFeatures["INDEX_PIP_z"],
                    handFeatures["INDEX_DIP_x"],
                    handFeatures["INDEX_DIP_y"],
                    handFeatures["INDEX_DIP_z"],
                    handFeatures["INDEX_TIP_x"],
                    handFeatures["INDEX_TIP_y"],
                    handFeatures["INDEX_TIP_z"],
                    handFeatures["MIDDLE_MCP_x"],
                    handFeatures["MIDDLE_MCP_y"],
                    handFeatures["MIDDLE_MCP_z"],
                    handFeatures["MIDDLE_PIP_x"],
                    handFeatures["MIDDLE_PIP_y"],
                    handFeatures["MIDDLE_PIP_z"],
                    handFeatures["MIDDLE_DIP_x"],
                    handFeatures["MIDDLE_DIP_y"],
                    handFeatures["MIDDLE_DIP_z"],
                    handFeatures["MIDDLE_TIP_x"],
                    handFeatures["MIDDLE_TIP_y"],
                    handFeatures["MIDDLE_TIP_z"],
                    handFeatures["RING_MCP_x"],
                    handFeatures["RING_MCP_y"],
                    handFeatures["RING_MCP_z"],
                    handFeatures["RING_PIP_x"],
                    handFeatures["RING_PIP_y"],
                    handFeatures["RING_PIP_z"],
                    handFeatures["RING_DIP_x"],
                    handFeatures["RING_DIP_y"],
                    handFeatures["RING_DIP_z"],
                    handFeatures["RING_TIP_x"],
                    handFeatures["RING_TIP_y"],
                    handFeatures["RING_TIP_z"],
                    handFeatures["PINKY_MCP_x"],
                    handFeatures["PINKY_MCP_y"],
                    handFeatures["PINKY_MCP_z"],
                    handFeatures["PINKY_PIP_x"],
                    handFeatures["PINKY_PIP_y"],
                    handFeatures["PINKY_PIP_z"],
                    handFeatures["PINKY_DIP_x"],
                    handFeatures["PINKY_DIP_y"],
                    handFeatures["PINKY_DIP_z"],
                    handFeatures["PINKY_TIP_x"],
                    handFeatures["PINKY_TIP_y"],
                    handFeatures["PINKY_TIP_z"]
                    ])
  else:
        with open(featureFile, 'w', newline='') as file:
            # if file has not been written to, add headers
            # Create a writer object from csv module
            writer = csv.writer(file)
            writer.writerow(["actualLetter", "WRIST_x", "WRIST_y", "WRIST_z", "THUMB_CMC_x", "THUMB_CMC_y", "THUMB_CMC_z", "THUMB_MCP_x", "THUMB_MCP_y", "THUMB_MCP_z", "THUMB_DIP_x", "THUMB_DIP_y", "THUMB_DIP_z", "THUMB_TIP_x", "THUMB_TIP_y", "THUMB_TIP_z", "INDEX_MCP_x", "INDEX_MCP_y", "INDEX_MCP_z", "INDEX_PIP_x", "INDEX_PIP_y", "INDEX_PIP_z", "INDEX_DIP_x", "INDEX_DIP_y", "INDEX_DIP_z", "INDEX_TIP_x", "INDEX_TIP_y", "INDEX_TIP_z", "MIDDLE_MCP_x", "MIDDLE_MCP_y", "MIDDLE_MCP_z", "MIDDLE_PIP_x", "MIDDLE_PIP_y", "MIDDLE_PIP_z", "MIDDLE_DIP_x", "MIDDLE_DIP_y", "MIDDLE_DIP_z", "MIDDLE_TIP_x", "MIDDLE_TIP_y", "MIDDLE_TIP_z", "RING_MCP_x", "RING_MCP_y", "RING_MCP_z", "RING_PIP_x", "RING_PIP_y", "RING_PIP_z", "RING_DIP_x", "RING_DIP_y", "RING_DIP_z", "RING_TIP_x", "RING_TIP_y", "RING_TIP_z", "PINKY_MCP_x", "PINKY_MCP_y", "PINKY_MCP_z", "PINKY_PIP_x", "PINKY_PIP_y", "PINKY_PIP_z", "PINKY_DIP_x", "PINKY_DIP_y", "PINKY_DIP_z", "PINKY_TIP_x", "PINKY_TIP_y", "PINKY_TIP_z"])
            writer.writerow([handFeatures["actualLetter"],
                    handFeatures["WRIST_x"],
                    handFeatures["WRIST_y"],
                    handFeatures["WRIST_z"],
                    handFeatures["THUMB_CMC_x"],
                    handFeatures["THUMB_CMC_y"],
                    handFeatures["THUMB_CMC_z"],
                    handFeatures["THUMB_MCP_x"],
                    handFeatures["THUMB_MCP_y"],
                    handFeatures["THUMB_MCP_z"],
                    handFeatures["THUMB_DIP_x"],
                    handFeatures["THUMB_DIP_y"],
                    handFeatures["THUMB_DIP_z"],
                    handFeatures["THUMB_TIP_x"],
                    handFeatures["THUMB_TIP_y"],
                    handFeatures["THUMB_TIP_z"],
                    handFeatures["INDEX_MCP_x"],
                    handFeatures["INDEX_MCP_y"],
                    handFeatures["INDEX_MCP_z"],
                    handFeatures["INDEX_PIP_x"],
                    handFeatures["INDEX_PIP_y"],
                    handFeatures["INDEX_PIP_z"],
                    handFeatures["INDEX_DIP_x"],
                    handFeatures["INDEX_DIP_y"],
                    handFeatures["INDEX_DIP_z"],
                    handFeatures["INDEX_TIP_x"],
                    handFeatures["INDEX_TIP_y"],
                    handFeatures["INDEX_TIP_z"],
                    handFeatures["MIDDLE_MCP_x"],
                    handFeatures["MIDDLE_MCP_y"],
                    handFeatures["MIDDLE_MCP_z"],
                    handFeatures["MIDDLE_PIP_x"],
                    handFeatures["MIDDLE_PIP_y"],
                    handFeatures["MIDDLE_PIP_z"],
                    handFeatures["MIDDLE_DIP_x"],
                    handFeatures["MIDDLE_DIP_y"],
                    handFeatures["MIDDLE_DIP_z"],
                    handFeatures["MIDDLE_TIP_x"],
                    handFeatures["MIDDLE_TIP_y"],
                    handFeatures["MIDDLE_TIP_z"],
                    handFeatures["RING_MCP_x"],
                    handFeatures["RING_MCP_y"],
                    handFeatures["RING_MCP_z"],
                    handFeatures["RING_PIP_x"],
                    handFeatures["RING_PIP_y"],
                    handFeatures["RING_PIP_z"],
                    handFeatures["RING_DIP_x"],
                    handFeatures["RING_DIP_y"],
                    handFeatures["RING_DIP_z"],
                    handFeatures["RING_TIP_x"],
                    handFeatures["RING_TIP_y"],
                    handFeatures["RING_TIP_z"],
                    handFeatures["PINKY_MCP_x"],
                    handFeatures["PINKY_MCP_y"],
                    handFeatures["PINKY_MCP_z"],
                    handFeatures["PINKY_PIP_x"],
                    handFeatures["PINKY_PIP_y"],
                    handFeatures["PINKY_PIP_z"],
                    handFeatures["PINKY_DIP_x"],
                    handFeatures["PINKY_DIP_y"],
                    handFeatures["PINKY_DIP_z"],
                    handFeatures["PINKY_TIP_x"],
                    handFeatures["PINKY_TIP_y"],
                    handFeatures["PINKY_TIP_z"]
                    ])
            
  file.close()

"""GETTING TRAINING IMAGE FEATURES"""

#@title
# give name to csv file
featureFileTrain = '/content/drive/MyDrive/Computer Vision/Feature File Training.csv'

# gather all images that are needed for training
IMAGE_FILES = []
imagesPath = "/content/drive/MyDrive/Computer Vision/Project Images/TRAINING/*.*"

for imageFile in glob.glob(imagesPath):
   IMAGE_FILES.append(imageFile)

# Restart CSV file if trained before
if os.path.exists(featureFileTrain):
    os.remove(featureFileTrain)


# loop through image files
for idx, imageFile in enumerate(IMAGE_FILES):
  # get features for each image
  handFeatures = getFeatures(imageFile)

  #Check to makes sure that coordinates have been processed properly
  if ((handFeatures["WRIST_x"] != 0) and (handFeatures["WRIST_y"] != 0)):
    # add newly found features to the appropriate file
    addToFeatureFile(featureFileTrain, handFeatures)
print("===================TRAINING Features Received===================")

"""GETTING TESTING IMAGE FEATURES"""

#@title
featureFileTest = '/content/drive/MyDrive/Computer Vision/Feature File Testing.csv'

# get all images for testing
IMAGE_FILES = []
imagesPath = "/content/drive/MyDrive/Computer Vision/Project Images/TESTING/*.*"

for file in glob.glob(imagesPath):
   IMAGE_FILES.append(file)

# Restart CSV file if trained before
if os.path.exists(featureFileTest):
    os.remove(featureFileTest)


# loop through image files
for idx, file in enumerate(IMAGE_FILES):
  handFeatures = getFeatures(file)

  #Check to makes sure that coordinates have been processed properly
  if ((handFeatures["WRIST_x"] != 0) and (handFeatures["WRIST_y"] != 0)):
    addToFeatureFile(featureFileTest, handFeatures)
print("===================TESTING Features Received===================")

"""SHOW TABLE RESULTS"""

#This section will display the results of all testing features
df_test = pd.read_csv(featureFileTest, header=0)

# Sort the values of the dataset according to their assigned letter
df_test = df_test.sort_values(by=["actualLetter"])

df_test

#@title

#This section will display the results of all training features
df_train = pd.read_csv(featureFileTrain, header=0)

# Sort the values of the dataset according their assigned letter
df_train = df_train.sort_values(by=["actualLetter"])

df_train

"""TRANSFORM ARRAY FOR USE IN NEURAL NETWORK"""

df_train["actualLetter"] = pd.Categorical(df_train["actualLetter"])
df_train["actualLetter"] = df_train.actualLetter.cat.codes

df_test["actualLetter"] = pd.Categorical(df_test["actualLetter"])
df_test["actualLetter"] = df_test.actualLetter.cat.codes

y_train = df_train.pop("actualLetter")
x_train = df_train.copy()

y_test = df_test.pop("actualLetter")
x_test = df_test.copy()

# Copied Features turn to Array by using NumPy
x_train = np.array(x_train)
x_test = np.array(x_test)

# Check Array Shape before transformation
print(x_train.shape)
print(x_test.shape)

# Since the array shape is 1x1, we must turn it into 1x10x1 so we can feed it into the model
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# Check Array Shape after transformation
print(x_train.shape)
print(x_test.shape)

# Check sample train and test features
print(x_train[0])
print(x_test[7])

# Number of classes according standard American Sign Language
num_classes = 26

# Using the Keras.Utils to put the label categorically 
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

"""BUILD NEURAL NETWORK"""

# One Dimensional Convolutional Neural Network model, Train will be feed to 1 Dimension Convolutional Neural Network
model = tf.keras.models.Sequential([
    tf.keras.layers.Conv1D(filters=32, kernel_size=5, strides=1, padding="causal", activation="relu", input_shape=x_train.shape[1:3]),
    tf.keras.layers.Conv1D(filters=32, kernel_size=5, strides=1, padding="causal", activation="relu"),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Conv1D(filters=64, kernel_size=5, strides=1, padding="causal", activation="relu"),
    tf.keras.layers.Conv1D(filters=64, kernel_size=5, strides=1, padding="causal", activation="relu"),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Conv1D(filters=128, kernel_size=5, strides=1, padding="causal", activation="relu"),
    tf.keras.layers.Conv1D(filters=128, kernel_size=5, strides=1, padding="causal", activation="relu"),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Conv1D(filters=256, kernel_size=5, strides=1, padding="causal", activation="relu"),
    tf.keras.layers.Conv1D(filters=256, kernel_size=5, strides=1, padding="causal", activation="relu"),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Dropout(rate=0.2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'), 
    tf.keras.layers.Dense(num_classes, activation='softmax')])

model.compile(loss = 'categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

"""TRAIN MODEL"""

#@title
#Train the Model
model.fit(x_train, y_train, epochs=100, batch_size=32, validation_data=(x_test, y_test))

#Saving the model into H5 system file
save_model = "ASL_model.h5"
model.save(save_model)
print("Model Saved into", save_model)

"""PREDICTION VALIDATION"""

#@title
# This is the final code that will test the validation data

classes = [ 
    'A', 'B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

accuratePredictionsTESTING = 0
numberTestedTESTING = 0

IMAGE_FILES = []
# ********** REPLACE PATH HERE!!!!! **********
imagesPath = "/content/drive/MyDrive/Computer Vision/Project Images/VALIDATION/FINAL VALIDATION/*.*"

for imagePath in glob.glob(imagesPath):
  

  handFeatures = getFeatures(imagePath)
  img = cv.imread(imagePath) 
  scale_percent = 20 # percent of original size
  width = int(img.shape[1] * scale_percent / 100)
  height = int(img.shape[0] * scale_percent / 100)
  dim = (width, height)
  resized=cv2.resize(img,dim)
  cv2_imshow(resized)

  inputImage = np.array([[
      handFeatures["WRIST_x"],
      handFeatures["WRIST_y"],
      handFeatures["WRIST_z"],
      handFeatures["THUMB_CMC_x"],
      handFeatures["THUMB_CMC_y"],
      handFeatures["THUMB_CMC_z"],
      handFeatures["THUMB_MCP_x"],
      handFeatures["THUMB_MCP_y"],
      handFeatures["THUMB_MCP_z"],
      handFeatures["THUMB_DIP_x"],
      handFeatures["THUMB_DIP_y"],
      handFeatures["THUMB_DIP_z"],
      handFeatures["THUMB_TIP_x"],
      handFeatures["THUMB_TIP_y"],
      handFeatures["THUMB_TIP_z"],
      handFeatures["INDEX_MCP_x"],
      handFeatures["INDEX_MCP_y"],
      handFeatures["INDEX_MCP_z"],
      handFeatures["INDEX_PIP_x"],
      handFeatures["INDEX_PIP_y"],
      handFeatures["INDEX_PIP_z"],
      handFeatures["INDEX_DIP_x"],
      handFeatures["INDEX_DIP_y"],
      handFeatures["INDEX_DIP_z"],
      handFeatures["INDEX_TIP_x"],
      handFeatures["INDEX_TIP_y"],
      handFeatures["INDEX_TIP_z"],
      handFeatures["MIDDLE_MCP_x"],
      handFeatures["MIDDLE_MCP_y"],
      handFeatures["MIDDLE_MCP_z"],
      handFeatures["MIDDLE_PIP_x"],
      handFeatures["MIDDLE_PIP_y"],
      handFeatures["MIDDLE_PIP_z"],
      handFeatures["MIDDLE_DIP_x"],
      handFeatures["MIDDLE_DIP_y"],
      handFeatures["MIDDLE_DIP_z"],
      handFeatures["MIDDLE_TIP_x"],
      handFeatures["MIDDLE_TIP_y"],
      handFeatures["MIDDLE_TIP_z"],
      handFeatures["RING_MCP_x"],
      handFeatures["RING_MCP_y"],
      handFeatures["RING_MCP_z"],
      handFeatures["RING_PIP_x"],
      handFeatures["RING_PIP_y"],
      handFeatures["RING_PIP_z"],
      handFeatures["RING_DIP_x"],
      handFeatures["RING_DIP_y"],
      handFeatures["RING_DIP_z"],
      handFeatures["RING_TIP_x"],
      handFeatures["RING_TIP_y"],
      handFeatures["RING_TIP_z"],
      handFeatures["PINKY_MCP_x"],
      handFeatures["PINKY_MCP_y"],
      handFeatures["PINKY_MCP_z"],
      handFeatures["PINKY_PIP_x"],
      handFeatures["PINKY_PIP_y"],
      handFeatures["PINKY_PIP_z"],
      handFeatures["PINKY_DIP_x"],
      handFeatures["PINKY_DIP_y"],
      handFeatures["PINKY_DIP_z"],
      handFeatures["PINKY_TIP_x"],
      handFeatures["PINKY_TIP_y"],
      handFeatures["PINKY_TIP_z"]
      ]])


  predictions = model.predict(inputImage)

  prediction = 0
  predictionIndex = 0
  index = 0
  for value in predictions[0]:
    if value > prediction:
      prediction = value
      predictionIndex = index
    index += 1


  print("prediction letter: ", classes[predictionIndex])
  if classes[predictionIndex] == handFeatures["actualLetter"]:
    accuratePredictionsTESTING += 1

  numberTestedTESTING +=1

  print("Number Tested: ", numberTestedTESTING)
  print("Accurate Predictions: ", accuratePredictionsTESTING)
  print("Accuracy Percentge: ", accuratePredictionsTESTING/numberTestedTESTING)
