import cv2 as cv
import yaml
from yaml.error import YAMLError
import numpy as np

aruco_dict = cv.aruco.Dictionary_get(cv.aruco.DICT_5X5_50)
marker_id = 0

def get_camera_matrices():
    with open("Perception/calibration_matrix.yaml", "r") as stream:
        try:
            read_data = yaml.safe_load(stream)
            return read_data['camera_matrix'], read_data['dist_coeff']
        except YAMLError as err:
            print(err)
    return None

camera_matrix, dist_coeffs = get_camera_matrices()
camera_matrix = np.array(camera_matrix)
dist_coeffs = np.array(dist_coeffs)

def get_camera_transform(frame, debug=True):
    ''' Returns an np.ndarray of size (4, 4) as a homogeneous transformation matrix from camera frame to marker frame
        Input: frame - the frame containing the ArUco Marker
    '''
    aruco_params = cv.aruco.DetectorParameters_create()
    corners, ids, _ = cv.aruco.detectMarkers(frame, aruco_dict, parameters=aruco_params)
    if len(corners) > 0:
        rvecs, tvecs, _ = cv.aruco.estimatePoseSingleMarkers(corners, 0.038, camera_matrix, dist_coeffs)
        rotation_matrix, _ = cv.Rodrigues(rvecs[0])
        translation_vector = tvecs[0].T
        if debug:
            new_frame = frame.copy()
            cv.aruco.drawDetectedMarkers(new_frame, corners, ids=ids)
            cv.aruco.drawAxis(new_frame, camera_matrix, dist_coeffs, rvecs[0], tvecs[0], 0.1)
            cv.imshow("ArUco Marker", new_frame)
        return np.block([[rotation_matrix, translation_vector],
                        [np.zeros((1, 3)), 1]])
    return None