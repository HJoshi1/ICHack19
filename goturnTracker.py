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
    
confThreshold = 0.1  #Confidence threshold

inpWidth = 416
inpHeight = 416
net = setup_net()
ok0, frame = video.read()

data = get_points(frame,net,confThreshold)
cents = data["boxes"]
new_cents = get_centres(cents)
simps = delete_repeats(new_cents)

trackers = {}
bboxes = {}
okays = {}

row = ["x0", "y0", "x1", "y1","x2", "y2", "x3", "y3"]


#Initialize trackers for each box gathered
for i in range(len(simps)):
    trackers[i] = cv2.TrackerGOTURN_create()
    bboxes[i] = tuple([simps[i][0] - 10, simps[i][1] - 10, 20, 20])
    okays[i] = trackers[i].init(frame,bboxes[i])

# Define a bounding box
#bbox = cv2.selectROI(frame, False) #with user input


with open('coords3_10.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

for i in range(no_frames-1):
    # Read a new frame 
    okays[0], frame = video.read()

    cur_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))
    
    if cur_frame % mod == 0:
        data = get_points(frame,net,confThreshold)
        cents = data["boxes"]
        new_cents = get_centres(cents)
        simps = delete_repeats(new_cents)
        for i in range(len(simps)):
            trackers[i] = cv2.TrackerGOTURN_create()
            bboxes[i] = tuple([simps[i][0] - 10, simps[i][1] - 10, 20, 20])
            okays[i] = trackers[i].init(frame,bboxes[i])


    # Start timer
    timer = cv2.getTickCount()

    # Update tracker
    for i in range(len(simps)):
        okays[i], bboxes[i] = trackers[i].update(frame)
    
        # Tracking success
    for i in range(len(simps)):
        p1 = (int(bboxes[i][0]), int(bboxes[i][1]))
        p2 = (int(bboxes[i][0] + bboxes[i][2]), int(bboxes[i][1] + bboxes[i][3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)  
        centre = [(p1[0] + p2[0])/2 ] + [(p1[1] + p2[1])/2]
        #print(centre)
    
    row.append(centre[0])
    row.append(centre[1])
    print(row)
    row = []

    with open('coords3_11.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
        row = []
    
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