# Copyright 2018 Satya Mallick (LearnOpenCV.com)

# Import modules
import cv2, sys, os, csv
from main_detect import setup_net, get_points, get_centres, delete_repeats



if  not (os.path.isfile('goturn.caffemodel') and os.path.isfile('goturn.prototxt')):
    errorMsg = '''
    Could not find GOTURN model in current directory.
    Please ensure goturn.caffemodel and goturn.prototxt are in the current directory
    '''

    print(errorMsg)
    sys.exit()



# Create tracker
'''tracker0 = cv2.TrackerGOTURN_create()   
tracker1 = cv2.TrackerGOTURN_create()   
tracker2 = cv2.TrackerGOTURN_create()   
tracker3 = cv2.TrackerGOTURN_create()  ''' 

# Read video
video = cv2.VideoCapture("drone6_4s.mp4")
no_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Exit if video not opened
if not video.isOpened():
    print("Could not open video")
    sys.exit()

# Read first frame
'''ok0,frame = video.read()
if not ok0:
    print("Cannot read video file")
    sys.exit()'''
  
    
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



for i in range(len(simps)):
    trackers[i] = cv2.TrackerGOTURN_create()
    bboxes[i] = tuple([simps[i][0] - 10, simps[i][1] - 10, 20, 20])
    okays[i] = trackers[i].init(frame,bboxes[i])

# Define a bounding box
#bbox = cv2.selectROI(frame, False)



'''bbox0 = tuple(data["boxes"].iloc[0])
bbox1 = tuple(data["boxes"].iloc[1])
bbox2 = tuple(data["boxes"].iloc[2])
bbox3 = tuple(data["boxes"].iloc[3])'''
# Initialize tracker with first frame and bounding box
'''ok0 = tracker0.init(frame,bbox0)
ok1 = tracker1.init(frame,bbox1)
ok2 = tracker2.init(frame,bbox2)
ok3 = tracker3.init(frame,bbox3)'''

row = ["x0", "y0", "x1", "y1","x2", "y2", "x3", "y3"]


with open('coords.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

for i in range(no_frames):
    # Read a new frame
    
    okays[0], frame = video.read()

    cur_frame = int(video.get(cv2.CAP_PROP_POS_FRAMES))


    # Start timer
    timer = cv2.getTickCount()

    # Update tracker
    for i in range(len(simps)):
        okays[i], bboxes[i] = trackers[i].update(frame)
    '''ok0, bbox0 = tracker0.update(frame)
    ok1, bbox1 = tracker1.update(frame)
    ok2, bbox2 = tracker2.update(frame)
    ok3, bbox3 = tracker3.update(frame)'''
    
    # Calculate Frames per second (FPS)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    row = []

    # Draw bounding box
    
        # Tracking success
    for i in range(len(simps)):
        p1 = (int(bboxes[i][0]), int(bboxes[i][1]))
        p2 = (int(bboxes[i][0] + bboxes[i][2]), int(bboxes[i][1] + bboxes[i][3]))
        cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)  
        centre = ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)
        row.append(centre)


        
        '''pA0 = (int(bbox0[0]), int(bbox0[1]))
        pB0 = (int(bbox0[0] + bbox0[2]), int(bbox0[1] + bbox0[3]))
        cv2.rectangle(frame, pA0, pB0, (255,0,0), 2, 1)
        
        pA1 = (int(bbox1[0]), int(bbox1[1]))
        pB1 = (int(bbox1[0] + bbox1[2]), int(bbox1[1] + bbox1[3]))
        cv2.rectangle(frame, pA1, pB1, (255,0,0), 2, 1)
        
        pA2 = (int(bbox2[0]), int(bbox2[1]))
        pB2 = (int(bbox2[0] + bbox2[2]), int(bbox2[1] + bbox2[3]))
        cv2.rectangle(frame, pA2, pB2, (255,0,0), 2, 1)
        
        pA3 = (int(bbox3[0]), int(bbox3[1]))
        pB3 = (int(bbox3[0] + bbox3[2]), int(bbox3[1] + bbox3[3]))
        cv2.rectangle(frame, pA3, pB3, (255,0,0), 2, 1)'''
        
        #check difference between two boxes if below threshold 
        #recheck all boxes if they're overlapping
        '''centre1 = ((pA1[0] + pB1[0])/2, (pA1[1] + pB1[1])/2)
        centre2 = ((pA2[0] + pB2[0])/2, (pA2[1] + pB2[1])/2)
        centre3 = ((pA3[0] + pB3[0])/2, (pA3[1] + pB3[1])/2)'''

        #cornerdiff1 = p1 - p11
        #cornerdiff2 = p2 - p21
        #closeness_value = 10
        

    with open('coords.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    
    csvFile.close()
        
       # if cornerdiff1*closeness_value < p1 or cornerdiff2*closeness_value < p2:
        #    #recalculate 
        #    bbox1 = cv2.selectROI(frame, False)
        #    bbox = cv2.selectROI(frame, False)
        
    
    # Tracking failure
    #cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

    # Display tracker type on frame
    cv2.putText(frame, "Current Frame:" + str(cur_frame), (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

    # Display FPS on frame
    cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

    # Display result
    cv2.imshow("Tracking", frame)
 
    # Exit if ESC pressed
    k = cv2.waitKey(1) & 0xff
    if k == 27:
        break