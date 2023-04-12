import cv2
import numpy as np


def calibrate(frame, output_dim):
    """Show the frame to the user, so he can click on the 4 corners of the field.
    It the creates the transformation matrix from thoses corners to a rectangular field
    of the specified dimensions.

    arguments:
    frame      -- the frame containing the image for the callibration
    output_dim -- the dimensions of the wanted field

    Usage:
    When the image appears, the user must click on the 4 corners of the field,
    and then press 'Enter'.
    The user can undo a mark if he wants by pressing the 'z' key.
    """
    positions = [] # list of the positions clicked
    
    def callback(event, x, y, flags, param):
        nonlocal positions
        if event == cv2.EVENT_LBUTTONDOWN:
            if len(positions) < 4:
                positions.append([x,y])
    
    cv2.namedWindow("Callibration")
    cv2.setMouseCallback("Callibration",callback)

    # Loop to get the 4 corners
    key = 0
    while (key != ord('\n') and key != ord('\r')) or len(positions) < 4:
        # Show the current frame
        current_frame = np.copy(frame)
        for p in positions:
            cv2.circle(current_frame, p, 8, (0,0,255), -1)
        cv2.imshow("Callibration", current_frame)

        # get new key and act accordingly
        key = cv2.waitKey(30)

        if key == ord('z'):
            if len(positions) > 0:
                positions.pop()
    
    # organisation of the corners
    positions.sort(key=lambda p: p[0])
    left = positions[:2]
    right = positions[2:]
    left.sort(key=lambda p: p[1])
    right.sort(key=lambda p: p[1])
    upleft = left[0]
    downleft = left[1]
    upright = right[0]
    downright = right[1]

    # Compute the transform matrix
    input_points = np.float32([upleft, upright, downright, downleft])
    width, height = output_dim
    output_points = np.float32([[0, 0],
                                [width - 1, 0],
                                [width - 1, height - 1],
                                [0, height - 1]])
    M = cv2.getPerspectiveTransform(input_points,output_points)

    return M
            

def apply_transform_to_point(mat, point):
    """Apply the perspective transformation matrix to the given 2D vector."""
    in_vect = np.array([point[0], point[1], 1]).T
    out_vect = np.dot(mat, in_vect)
    return [int(out_vect[0]/out_vect[2]), int(out_vect[1]/out_vect[2])]