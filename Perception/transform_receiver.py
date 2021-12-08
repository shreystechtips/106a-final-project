import cv2 as cv

aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_50)
marker_id = 0

def get_camera_transform(frame):
    aruco_params = cv.aruco.DetectorParameters_create()
    (corners, ids, rejected) = cv.aruco.detectMarkers(frame, aruco_dict, parameters=aruco_params)
    new_frame = frame.copy()
    if len(corners) > 0:
        cv.aruco.drawDetectedMarkers(new_frame, corners, ids=ids)
        cv.imshow("ArUco Marker", new_frame)
    return None