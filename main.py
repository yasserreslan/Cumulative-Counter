import cv2
import imutils
import time
from classes import Box
from pytube import YouTube

import os


#Ensure video does not download every time we run
if (os.path.isfile("carvid.mp4")):
  pass

#Download video for the first time for usage
else:
    print("Downloading video from Youtube...")
    yt = YouTube('https://www.youtube.com/watch?v=R3BKDet7am8')

    ys = yt.streams.get_highest_resolution()
    
    ys.download(filename="carvid.mp4")



#Get vid from file dir
cap = cv2.VideoCapture("carvid.mp4")

#Last frame to compare with
last_frame = None

# Car video header 
text = ""

# Visualize the line from which the cars pass
boxes = []
boxes.append(Box((337, 300), (175, 1)))



#Start video
print("\n Running current frames...")
while cap.isOpened():
    #Read video frames
    _, frame = cap.read()

    

    #Slow down the frame (this can be adjusted)
    time.sleep(0.01)
    
    

    # Processing of frames are done in gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)


    # Need to check if we have last frame, if not get it
    if last_frame is None or last_frame.shape != gray.shape:
        last_frame = gray
        continue


    # Compare last frame
    delta_frame = cv2.absdiff(last_frame, gray)
    last_frame = gray

    # Scan for movemnent
    thresh = cv2.threshold(delta_frame, 10, 1000, cv2.THRESH_BINARY)[1]
    # Number of iterations to scan (If the iterations is too low we might now catch all movement, 
    # if too high we might get unwanted boxes ex:car tops details)

    thresh = cv2.dilate(thresh, None, iterations=2)
    # Returns a list of objects
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Converts it
    contours = imutils.grab_contours(contours)



    # Loops over all objects found
    for contour in contours:
        # Skip if contour is small (312 is ideal for this video)
        if cv2.contourArea(contour) < 312:
            continue


        # Get a bounding box arround vehicles 
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Frame Counter header
        text = "Cars:"
        # Check for overlap
        for box in boxes:
            box.frame_countdown -= 1
            if box.overlap((x, y), (x + w, y + h)):
                if box.frame_countdown <= 0:
                    box.counter += 1
                box.frame_countdown = 15
            text += " (" + str(box.counter) + ")"

    # Set the header
    cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    #insert boxes on frame
    for box in boxes:
        cv2.rectangle(frame, box.start_point, box.end_point, (255, 255, 255), 2)


    # Let's show the frame in our window
    cv2.imshow("Car counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()