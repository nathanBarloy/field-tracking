import cv2
import numpy as np
import time


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
    
    cv2.destroyWindow("Callibration")

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
    return [out_vect[0]/out_vect[2], out_vect[1]/out_vect[2]]


class VideoPlayer:
    """
    This class can be used to manipulate a video stream.

    Attributes:
    video : cv2.VideoCapture
        The video OpenCV object.
    paused : bool
        True if the video is paused.
    elapsed_time : float
        Time to wait between two frames (in ms).
    previous_frames : List[cv2.Image]
        List of the previous frames. The last frame in the list is the current one.
    next_frames : List[cv2.Image]
        List of the next frames to play before getting new ones.
    buffer_size : int
        Max size of the previous_frame attribute.
    field_dim : Tuple(float, float)
        Dimensions of the watched field. Should be (width, height).
    transform_matrix : numpy.array
        The transformation matrix for the field.
    
    Methodes:
    read_frame() -> bool
        Read and show the next frame. Return False if it is the end of the video.
    rewind_frame() -> None
        Show the previous frame.
    play() -> None
        Start the video player.
    """

    def __init__(self, path, buffer_size, field_dim):
        self.video = cv2.VideoCapture(path)
        if not self.video.isOpened():
            raise ValueError(f"Could not open video at path '{path}'.")
        self.paused = True
        fps = self.video.get(cv2.CAP_PROP_FPS)
        self.elapsed_time = 1000/fps
        self.previous_frames = [] # could be faster with a linked list
        self.next_frames = []
        self.buffer_size = buffer_size
        self.field_dim = field_dim
    
    def read_frame(self):
        if len(self.next_frames) == 0:
            ret, frame = self.video.read()
        else:
            ret, frame = True, self.next_frames.pop()
        if not ret:
            return False
        
        if len(self.previous_frames) >= self.buffer_size:
            self.previous_frames.pop(0)
        self.previous_frames.append(frame)
        cv2.imshow("Video", frame)
        return True

    def rewind_frame(self):
        if len(self.previous_frames) > 1:
            self.next_frames.append(self.previous_frames.pop())
            cv2.imshow("Video", self.previous_frames[-1])

    def start(self):
        self.read_frame()
        self.transform_matrix = calibrate(self.previous_frames[-1], self.field_dim)

        old_time = time.time()
        while self.video.isOpened():
            if not self.paused:
                if not self.read_frame():
                    break

            new_time = time.time()
            to_wait = int(self.elapsed_time - 1000*(new_time-old_time))
            key = cv2.waitKey(max(to_wait, 1))
            old_time = new_time
            if key == ord('q'):
                break
            if key == ord(' '):
                self.paused = not self.paused
            if key == ord('a'):
                self.elapsed_time /=0.75
            if key == ord('z'):
                self.elapsed_time *=0.75
            if key == ord('p'):
                if self.paused:
                    if not self.read_frame():
                        break
            if key == ord('o'):
                if self.paused:
                    self.rewind_frame()

        self.video.release()
        cv2.destroyAllWindows()
