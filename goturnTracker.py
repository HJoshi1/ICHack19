# Copyright 2018 Satya Mallick (LearnOpenCV.com)

# Import modules
import cv2, sys, os, csv

if  not (os.path.isfile('goturn.caffemodel') and os.path.isfile('goturn.prototxt')):
    errorMsg = '''
    Could not find GOTURN model in current directory.
    Please ensure goturn.caffemodel and goturn.prototxt are in the current directory
    '''

    print(errorMsg)
    sys.exit()

# Create tracker
tracker = cv2.TrackerGOTURN_create()   
tracker1 = cv2.TrackerGOTURN_create()   

# Read video
video = cv2.VideoCapture("drone1.mp4")

# Exit if video not opened
if not video.isOpened():
    print("Could not open video")
    sys.exit()

# Read first frame
ok,frame = video.read()
if not ok:
    print("Cannot read video file")
    sys.exit()
    



# Define a bounding box
bbox = cv2.selectROI(frame, False)

# Uncomment the line below to select a different bounding box
bbox1 = cv2.selectROI(frame, False)

# Initialize tracker with first frame and bounding box
ok = tracker.init(frame,bbox)
ok1 = tracker1.init(frame,bbox1)

row = ["x1", "y1", "x2", "y2"]

with open('coords.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

while True:
    # Read a new frame
    ok, frame = video.read()
    ok1, frame = video.read()
    if not ok or not ok1:
        break

    # Start timer
    timer = cv2.getTickCount()

    # Update tracker
    ok, bbox = tracker.update(frame)
    ok1, bbox1 = tracker1.update(frame)

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    

    # Draw bounding box
    if ok:
        # Tracking success
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        
        p11 = (int(bbox1[0]), int(bbox1[1]))
        p21 = (int(bbox1[0] + bbox1[2]), int(bbox1[1] + bbox1[3]))
        cv2.rectangle(frame, p11, p21, (255,0,0), 2, 1)
        
        #check difference between two boxes if below threshold 
        #recheck all boxes if they're overlapping
        centre = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)
        centre1 = ((p11[0] + p21[0])/2, (p11[1] + p21[1])/2)

        #cornerdiff1 = p1 - p11
        #cornerdiff2 = p2 - p21
        closeness_value = 10
        
        row = [centre[0], centre[1], centre1[0], centre1[1]]

        with open('coords.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        
        csvFile.close()
        
       # if cornerdiff1*closeness_value < p1 or cornerdiff2*closeness_value < p2:
        #    #recalculate 
        #    bbox1 = cv2.selectROI(frame, False)
        #    bbox = cv2.selectROI(frame, False)
        
    else :
        # Tracking failure
        cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Display tracker type on frame
    cv2.putText(frame, "GOTURN Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    # Display result
    cv2.imshow("Tracking", frame)
 
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break