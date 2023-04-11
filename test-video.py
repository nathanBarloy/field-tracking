import numpy as np
import cv2
import pynput


# Open video and get informations
video = cv2.VideoCapture("/home/nathan/misc/opencv/j1_padel.mp4")
fps = video.get(cv2.CAP_PROP_FPS)
elapsed_time = 1000/fps
elapsed_time_int = int(elapsed_time)

if not video.isOpened():
    print("Could not open video")


# callback functions for mouse click
def left_click(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),10,(0,0,255),-1)






paused = False
while video.isOpened():
    if not paused:
        ret, frame = video.read()
        if not ret:
            break
        
        cv2.imshow("Video", frame)

    key = cv2.waitKey(elapsed_time_int)
    if key == ord('q'):
        break
    if key == ord(' '):
        paused = not paused
    if key == ord('a'):
        elapsed_time /=0.75
        elapsed_time_int = int(elapsed_time)
    if key == ord('z'):
        elapsed_time *=0.75
        elapsed_time_int = int(elapsed_time)


video.release()
cv2.destroyAllWindows()