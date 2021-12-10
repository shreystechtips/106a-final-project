import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import os

PATHNAME = '/Users/ryankoh/Desktop/106a-final-project/TestData/steel_ball_test_imgs/'
def get_ball_location(frame):
    for filename in os.listdir(PATHNAME):
        # if not filename == 'PXL_20211208_184659297.jpg':
        #     continue
        frame = cv.imread(PATHNAME + filename, 0)
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
        
        # frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        print("Got this far")
        minRadius = 26
        counter = 100
        while counter > 0:
            circles = cv.HoughCircles(frame, cv.HOUGH_GRADIENT, 1, 20, param1=200, param2=70, minRadius=minRadius, maxRadius=70)
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
    get_ball_location(None)