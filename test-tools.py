import cv2
import numpy as np

from tools import calibrate


# Open video and get informations
video = cv2.VideoCapture("/home/nathan/misc/opencv/j1_padel.mp4")
fps = video.get(cv2.CAP_PROP_FPS)
elapsed_time = 1000/fps
elapsed_time_int = int(elapsed_time)

if not video.isOpened():
    print("Could not open video")

# test calibrate
ret, frame = video.read()
calibrate(frame)

video.release()
cv2.destroyAllWindows()