#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 01:47:21 2019

@author: arohan
"""

import numpy as np
import cv2 as cv
import pandas as pd

# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def postprocess(frame, outs, confThreshold):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    classIds = []
    confidences = []
    boxes = []
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if detection[4]>confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
    
    mapping = {'confidences':confidences,'classIds':classIds,'boxes':boxes}
    data = pd.DataFrame(mapping)
    data.sort_values(by=['confidences'],ascending=False)
    print("len(data): ",len(data))
    
    for i in range(len(data)):
        cv.rectangle(frame,(data["boxes"].iloc[i][0],data["boxes"].iloc[i][1]),(data["boxes"].iloc[i][0]+data["boxes"].iloc[i][2],data["boxes"].iloc[i][1]+data["boxes"].iloc[i][3]),(0,255,0),3)
    
        