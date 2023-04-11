import cv2
import numpy as np


def calibrate(frame):
    positions = [] # list of the positions clicked
    
    def callback(event, x, y, flags, param):
        nonlocal positions
        if event == cv2.EVENT_LBUTTONDOWN:
            positions.append((x,y))
            cv2.circle(frame, (x,y), 8, (0,0,255), -1)
            cv2.imshow("Callibration", frame)
    
    cv2.imshow("Callibration", frame)
    cv2.setMouseCallback('Callibration',callback)

    key = 0
    while key != ord('\n') and key != ord('\r'):
        key = cv2.waitKey(50)
    print(positions)
            
