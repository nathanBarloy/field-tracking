import numpy as np
import cv2
import matplotlib.pyplot as plt


def apply_transform_to_point(mat, point):
    in_vect = np.array([point[0], point[1], 1]).T
    out_vect = np.dot(mat, in_vect)
    return (int(out_vect[0]/out_vect[2]), int(out_vect[1]/out_vect[2]))


img = cv2.imread("/home/nathan/Images/camera_padel.jpg")
height = img.shape[0]
width = img.shape[1]


A = [390, 1870]
B = [1182, 645]
C = [2612, 680]
D = [3265, 1870]
E = [1893, 1080]
for x in [A,B,C,D,E]:
    cv2.circle(img, x, 10, (0,0,255), -1)

"""
downsize = 0.40
img = cv2.resize(img,(int(downsize*width), int(downsize*height)), interpolation = cv2.INTER_AREA)
cv2.imshow("test", img)
"""


maxHeight = 1000
maxWidth = 500
input_pts = np.float32([A, B, C, D])
output_pts = np.float32([[0, maxHeight - 1],
                        [0, 0],
                        [maxWidth - 1, 0],
                        [maxWidth - 1, maxHeight - 1]])


M = cv2.getPerspectiveTransform(input_pts,output_pts)
out = cv2.warpPerspective(img,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)

E2 = apply_transform_to_point(M, E)
print(E2)
cv2.circle(out, E2, 10, (0,255,0), -1)


cv2.imshow("terrain", out)


cv2.waitKey(0)
cv2.destroyAllWindows()

