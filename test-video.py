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
    global paused
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img,(x,y),10,(0,0,255),-1)






paused = False
previous_frames = [] # could be faster with a linked list
next_frames = []
max_num_frames = 64

def read_frame():
    if len(next_frames) == 0:
        ret, frame = video.read()
    else:
        ret, frame = True, next_frames.pop()
    if not ret:
        return False
    
    if len(previous_frames) >= max_num_frames:
        previous_frames.pop(0)
    previous_frames.append(frame)
    cv2.imshow("Video", frame)
    return True

def rewind_frame():
    if len(previous_frames) > 1:
        next_frames.append(previous_frames.pop())
        cv2.imshow("Video", previous_frames[-1])
    
    


while video.isOpened():
    if not paused:
        if not read_frame():
            break

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
    if key == ord('p'):
        if paused:
            if not read_frame():
                break
    if key == ord('o'):
        if paused:
            rewind_frame()


video.release()
cv2.destroyAllWindows()