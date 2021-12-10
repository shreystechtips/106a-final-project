import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os
import pyrealsense2.pyrealsense2 as rs

def get_ball_location(frame):
    # if not filename == 'PXL_20211208_184659297.jpg':
    #     continue
    # frame = cv.resize(frame, (0,0), fx = 0.2, fy = 0.2)
    # cv.imshow("frame", frame)
    blurred_frame = cv.GaussianBlur(frame, (5, 5), 0)
    # cv.imshow("blur", blurred_frame)
    # edges = cv.Canny(blurred_frame,100,200)
    # plt.subplot(121),plt.imshow(blurred_frame,cmap = 'gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    # plt.show()
    # k = cv.waitKey(1) & 0xFF
    # hsv_frame = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)
    # brown_lower = np.array([10, 100, 20])
    # brown_upper = np.array([20, 255, 200])
    # mask_brown = cv.inRange(hsv_frame, brown_lower, brown_upper)

    # brown_output = cv.bitwise_and(frame, frame, mask=mask_brown)

    # cv.imshow("brown", brown_output)
    
    # cv.imshow("mask", mask_brown)
    
    # blurred_frame = cv.GaussianBlur(frame, (5, 5), 0)
    # hsv_frame = cv.cvtColor(blurred_frame, cv.COLOR_BGR2HSV)
    # thresholded = cv.inRange(hsv_frame, np.array([0, 0, 150]), np.array([255, 100, 200]))
    # # thresholded = cv.inRange(hsv_frame, np.array([0, 0, 0]), np.array([90, 20, 360]))
    # cv.imshow("Threshold", thresholded)
    
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    minRadius = 26
    counter = 100
    while counter > 0:
        circles = cv.HoughCircles(frame_gray, cv.HOUGH_GRADIENT, 1, 20, param1=200, param2=70, minRadius=minRadius, maxRadius=70)
        print("done applying circles")
        if circles is not None and len(circles[0]) == 1:
            print("circles are")
            print(circles)
            for x, y, r in circles[0]:
                c = plt.Circle((x, y), r, fill=False, lw=3, ec='C1')
                plt.gca().add_patch(c)
            plt.imshow(frame)
            plt.gcf().set_size_inches((12, 8))
            plt.show()
            break
        else:
            print(circles)
            print(minRadius)
            if circles is None or len(circles[0]) == 1:
                minRadius -= 1
            else:
                minRadius += 1
        counter -= 1

if __name__ == '__main__':
    pipeline = rs.pipeline()
    config = rs.config()

    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    pipeline.start(config)
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        cv.imshow('frame',color_image)
        get_ball_location(color_image)

        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break
