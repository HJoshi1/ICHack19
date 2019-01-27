# Copyright 2018 Satya Mallick (LearnOpenCV.com)

# Import modules
import cv2, sys, os, csv
from main_detect import setup_net, get_points, get_centres, delete_repeats
import numpy as np


if  not (os.path.isfile('goturn.caffemodel') and os.path.isfile('goturn.prototxt')):
    errorMsg = '''
    Could not find GOTURN model in current directory.
    Please ensure goturn.caffemodel and goturn.prototxt are in the current directory
    '''

    print(errorMsg)
    sys.exit()

# Read video
input_file = "drone3.mp4"
video = cv2.VideoCapture(input_file)
no_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(video.get(cv2.CAP_PROP_FPS))
mod = 70
outputFile = input_file[:-4] + str(mod)+ "_out.avi"

vid_writer = cv2.VideoWriter(outputFile,cv2.VideoWriter_fourcc('M','J','P','G'), fps, (round(video.get(cv2.CAP_PROP_FRAME_WIDTH)),round(video.get(cv2.CAP_PROP_FRAME_HEIGHT))))

# Exit if video not opened
if not video.isOpened():
    print("Could not open video")
    sys.exit()
    
tracker1 = cv2.TrackerGOTURN_create()
tracker2 = cv2.TrackerGOTURN_create()
okays1, frame = video.read()

    
confThreshold = 0.1  #Confidence threshold

inpWidth = 416
inpHeight = 416
net = setup_net()

data = get_points(frame,net,confThreshold)
cents = data["boxes"]
new_cents = get_centres(cents)
simps = delete_repeats(new_cents)


row0 = ["x0", "y0"]
row1 = ["x1", "y1"]

with open('coords_player1.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row0)
    row0 = []

csvFile.close()


with open('coords_player2.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row1)
    row1 = []

csvFile.close()

#Initialize trackers for each box gathered
bboxes1 = tuple([simps[0][0] - 10, simps[0][1] - 10, 20, 20])
okays1 = tracker1.init(frame,bboxes1)

bboxes2 = tuple([simps[1][0] - 10, simps[1][1] - 10, 20, 20])
okays2 = tracker2.init(frame,bboxes2)

# Define a bounding box
#bbox = cv2.selectROI(frame, False) #with user input


while True:
    # Read a new frame 
    okays1, frame = video.read()
    okays2, frame = video.read()
    
    if not okays1 or not okays2:
        break

    cur_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
    
    if cur_frame % mod == 0:
        data = get_points(frame,net,confThreshold)
        cents = data["boxes"]
        new_cents = get_centres(cents)
        simps = delete_repeats(new_cents)
        
        ''' p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        centre1 = '''
        
        
        tracker1 = cv2.TrackerGOTURN_create()
        bboxes1 = tuple([simps[0][0] - 10, simps[0][1] - 10, 20, 20])
        okays1 = tracker1.init(frame,bboxes1)
        
        tracker2 = cv2.TrackerGOTURN_create()
        bboxes2 = tuple([simps[1][0] - 10, simps[1][1] - 10, 20, 20])
        okays2 = tracker2.init(frame,bboxes2)
    
    
    # Start timer
    timer = cv2.getTickCount()

    # Update tracker
    okays1, bboxes1 = tracker1.update(frame)
    okays2, bboxes2 = tracker2.update(frame)

    
    # Tracking success
    p1 = (int(bboxes1[0]), int(bboxes1[1]))
    p2 = (int(bboxes1[0] + bboxes1[2]), int(bboxes1[1] + bboxes1[3]))
    cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)  
    centre1 = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)
    
    p12 = (int(bboxes2[0]), int(bboxes2[1]))
    p22 = (int(bboxes2[0] + bboxes2[2]), int(bboxes2[1] + bboxes2[3]))
    cv2.rectangle(frame, p12, p22, (255,0,0), 2, 1)  
    centre2 = ((p12[0] + p22[0])/2, (p12[1] + p22[1])/2)
    
    row0.append(centre1[0])
    row0.append(centre1[1])
    
    row1.append(centre2[0])
    row1.append(centre2[1])

    with open('coords_player1.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row0)
    row0 = []

    csvFile.close()

    with open('coords_player2.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row1)
    row1 = []
    
    csvFile.close()
        
    # Display tracker type on frame
    cv2.putText(frame, "Current Frame:" + str(cur_frame), (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

    # Display result
    #cv2.imshow("Tracking", frame)
    vid_writer.write(frame.astype(np.uint8))
    print("Frame ",cur_frame," in ",no_frames)
    
    
    
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break