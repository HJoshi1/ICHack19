#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 16:35:40 2019

@author: arohan
"""
import cv2 as cv
import numpy as np
from sub_detect import postprocess, getOutputsNames


# Initialize the parameters
confThreshold = 0.1  #Confidence threshold
inpWidth = 416  #608     #Width of network's input image
inpHeight = 416 #608     #Height of network's input image

#Initialize video capture/writer object
input_source = "trialvideos/drone6_4s.mp4"
outputFile = "trialvideos/drone6out.avi"
cap = cv.VideoCapture(input_source)
no_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
vid_writer = cv.VideoWriter(outputFile, cv.VideoWriter_fourcc('M','J','P','G'), 30, (round(cap.get(cv.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv.CAP_PROP_FRAME_HEIGHT))))

## Setup neural netowrk
#Load names of classes
classesFile = "model/coco.names";
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
#Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "model/yolov3.cfg";
modelWeights = "model/yolov3.weights";
#Setup net
net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)

#Process data
for i in range(no_frames):
    hasFrame, frame = cap.read()
    cur_frame = int(cap.get(cv.CAP_PROP_POS_FRAMES))
    blob = cv.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))
    data = postprocess(frame, outs, confThreshold)
    vid_writer.write(frame.astype(np.uint8))
    print("Frame ",cur_frame," in ",no_frames)
    
    
    
    
    
    
    
    
    
    