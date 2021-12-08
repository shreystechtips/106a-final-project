import cv2 as cv
from ball_detector import get_ball_location

if __name__ == '__main__':
    cap = cv.VideoCapture('/Users/karthikdharmarajan/Documents/EECS106A/106a-final-project/TestData/video-1638937380.mp4')
    while(1):
        ret, frame = cap.read()
        get_ball_location(frame)
        cv.imshow('frame',frame)
        k = cv.waitKey(1) & 0xFF
        if k == 27:
            break
    cv.destroyAllWindows()
