import cv2 as cv

# Run from main directory, not Perception directory

video_cap = cv.VideoCapture(0)
counter = 0

while (True):
    ret, img = video_cap.read()
    if not ret:
        break
    cv.imshow('Image', img)
    k = cv.waitKey(1)
    if k == ord('p'):
        cv.imwrite(f'calibration_image{counter}.jpg', img)
        counter += 1
cv.destroyAllWindows()
