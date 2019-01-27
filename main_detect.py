#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 16:35:40 2019

@author: arohan
"""
import cv2
import pandas as pd
import numpy as np

def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def postprocess(frame, outs, confThreshold):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    confidences = []
    boxes = []
    
    for out in outs:
        for detection in out:
            scores = detection[5:]
            #classId = np.argmax(scores)
            confidence = scores[np.argmax(scores)]
            if detection[4]>confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])
    
    mapping = {'confidences':confidences,'boxes':boxes}
    data = pd.DataFrame(mapping)
    data = data.sort_values(by=['confidences'],ascending=False)

    return data
    #for i in range(len(data)):
    #    cv2.rectangle(frame,(data["boxes"].iloc[i][0],data["boxes"].iloc[i][1]),(data["boxes"].iloc[i][0]+data["boxes"].iloc[i][2],data["boxes"].iloc[i][1]+data["boxes"].iloc[i][3]),(0,255,0),3)
    
        

def setup_net():
    
    ## Setup neural netowrk
    #Give the configuration and weight files for the model and load the network using them.
    modelConfiguration = "yolov3.cfg";
    modelWeights = "yolov3.weights";
    #Setup net
    net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return net

def get_points(frame,net,confThreshold):
    #Process data
    blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), [0,0,0], 1, crop=False)
    net.setInput(blob)
    outs = net.forward(getOutputsNames(net))
    data = postprocess(frame, outs, confThreshold)
    
    return data

 
    
def euclidean(a,b):
    if len(a) != len(b):
        return "Lengths are unequal"
    else:
        tot = 0  
    for i in range(len(a)):
        tot += (b[i] - a[i])**2
    ans = np.sqrt(tot)
    return ans

def get_centres(boxes):
    centres = []
    for box in boxes:
        xCoord = box[0] + box[2]/2
        yCoord = box[1] + box[3]/2
        centres.append([int(xCoord), int(yCoord)])
    return centres 


def KNN_search(N, centres,frame,iterations):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    randy = []
    randx = []
    
    #N is number of classes
    for i in range(N):
        randx.append(np.random.rand()*frameWidth)
        randy.append(np.random.rand()*frameHeight)
        
    min_indices = [] #should be same length as centres
    
    #len(centers) is the number of centres
    for i in range(iterations):
        for j in range(len(centres)):
            classes = []
            for k in range(N):
                classes.append(euclidean(centres[j],[randx[k],randy[k]]))
        minIndex = classes.index(min(classes))
        min_indices.append(minIndex)
    
        mapping = {'centres':centres,'min_index':min_indices}
        
        for i in range(N):
            xsum = 0
            ysum = 0
            count = 0
            if mapping['min_index'] == i:
                xsum += mapping[centres][0]
                ysum += mapping[centres][1]
                count += 1
            if count > 0:
                randx[i] = xsum/count
                randy[i] = ysum/count
    
    new_centres = []
    for i in range(N):
        new_centres.append([randx[i],randy[i]])
    
    return new_centres
    

def delete_repeats(centres):
    simplified_values = centres[:][:]
    
    for point1 in simplified_values:
        for point2 in simplified_values:
            if point1 != point2:
                #print(centres)
                euc = euclidean(point1,point2)
                if  euc < 200:
                    simplified_values.remove(point2)
                    
    return simplified_values
    
def reduce_confident_boxes(centres):
    simp_vals = []
    for i, centre in enumerate(centres):
        for j, spot in enumerate(centres):
            if not i == j:
                if euclidean(centre, spot) > 30:
                    if centre not in simp_vals:
                        simp_vals.append(centre)
                    if spot not in simp_vals:
                        simp_vals.append(spot)
                else:
                    xCoord = (centre[0] + spot[0])/2
                    yCoord = (centre[1] + spot[1])/2
                    simp_vals.append([xCoord, yCoord])
    return simp_vals
                    

        
        
    


    
    
    
    
    
    
    
    
    