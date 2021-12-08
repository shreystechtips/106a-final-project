import cv2 as cv
import numpy as np

def get_ball_location(frame):
    blurred_frame = cv.GaussianBlur(frame, (5, 5), 0)
    hsv_frame = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)
    thresholded = cv.inRange(hsv_frame, np.array([0, 0, 150]), np.array([255, 255, 255]))
    cv.imshow("Threshold", thresholded)
