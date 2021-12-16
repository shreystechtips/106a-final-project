import numpy as np
import pyrealsense2.pyrealsense2 as rs
import cv2 as cv 

def invert_homogeneous_matrix(matrix: np.ndarray):
    ''' Inverts a homogeneous matrix given as matrix
    '''
    R = matrix[0:3, 0:3]
    T = matrix[0:3, 3:]
    R_t = R.T
    return np.block([[R_t, np.dot(R_t, -1 * T)],
                     [np.zeros((1,3)), 1]])

workspace_to_marker_transformation = np.array([[0, -1, 0, 0.36195],
                                               [1, 0, 0, -0.46355],
                                               [0, 0, 1, -0.03],
                                               [0, 0, 0, 1]])

marker_to_workspace_transformation = invert_homogeneous_matrix(workspace_to_marker_transformation)

def convert_camera_vector_to_workspace(vector: np.array, camera_to_marker_transform: np.ndarray):
    ''' vector: (3,) numpy array in the camera frame
        output: (3,) numpy array in the workspace frame
    '''
    vector.append(1)
    marker_vector = np.dot(camera_to_marker_transform, vector)
    workspace_vector = np.dot(marker_to_workspace_transformation, marker_vector)
    return workspace_vector[0:3]

def draw_static_transform(frame, camera_intrinsic_matrix, dist_coeffs, marker_to_camera_transform):    
    workspace_to_camera_transformation = np.matmul(marker_to_camera_transform, workspace_to_marker_transformation)
    rvec, _ = cv.Rodrigues(workspace_to_camera_transformation[0:3, 0:3])
    print(rvec.T)
    print(workspace_to_camera_transformation[0:3, 3:])
    cv.aruco.drawAxis(frame, camera_intrinsic_matrix, dist_coeffs, rvec, workspace_to_camera_transformation[0:3, 3:], 0.1)

def get_pixel_location_camera_frame(x: int, y: int, depth, depth_intrinsics):
    depth_value = depth.get_distance(x, y)
    depth_point = rs.rs2_deproject_pixel_to_point(
            depth_intrinsics, [x, y], depth_value)
    return depth_point