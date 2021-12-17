import numpy as np
import pyrealsense2.pyrealsense2 as rs
import cv2 as cv 

def invert_homogeneous_matrix(matrix: np.ndarray):
    ''' Inverts a homogeneous matrix given as matrix
    '''
    # R = matrix[0:3, 0:3]
    # T = matrix[0:3, 3:]
    # R_t = R.T
    # return np.block([[R_t, np.dot(R_t, -1 * T)],
    #                  [np.zeros((1,3)), 1]])
    return np.linalg.inv(matrix)

workspace_to_marker_transformation = np.array([[0.0, -1.0, 0.0, 0.18],
                                               [1.0, 0.0, 0.0, -0.267],
                                               [0.0, 0.0, 1.0, 0.1],
                                               [0.0, 0.0, 0.0, 1.0]])

marker_to_workspace_transformation = invert_homogeneous_matrix(workspace_to_marker_transformation)

def convert_camera_vector_to_workspace(vector: np.array, camera_to_marker_transform: np.ndarray):
    ''' vector: (3,) numpy array in the camera frame
        output: (3,) numpy array in the workspace frame
    '''
    vector = np.append(vector, 1)
    marker_vector = np.dot(camera_to_marker_transform, vector)
    workspace_vector = np.dot(marker_to_workspace_transformation, marker_vector)
    return workspace_vector[0:3]

def draw_static_transform(frame, camera_intrinsic_matrix, dist_coeffs, marker_to_camera_transform):    
    workspace_to_camera_transformation = np.matmul(marker_to_camera_transform, workspace_to_marker_transformation)
    rvec, _ = cv.Rodrigues(workspace_to_camera_transformation[0:3, 0:3])
    # print(rvec.T)
    # print(workspace_to_camera_transformation[0:3, 3:])
    cv.aruco.drawAxis(frame, camera_intrinsic_matrix, dist_coeffs, rvec, workspace_to_camera_transformation[0:3, 3:], 0.1)

def get_pixel_location_camera_frame(x: int, y: int, depth, depth_intrinsics):
    depth_value = depth.get_distance(x, y)
    depth_point = rs.rs2_deproject_pixel_to_point(
            depth_intrinsics, [x, y], depth_value)
    return depth_point

def get_pixel_location_workspace_frame(x: int, y: int, depth, depth_intrinsics, camera_to_marker_transform):
    camera_frame_coord = np.array(get_pixel_location_camera_frame(x, y, depth, depth_intrinsics))
    return convert_camera_vector_to_workspace(camera_frame_coord, camera_to_marker_transform)

def get_gcode_coords(workspace_coords):
    tentative_coords = [workspace_coords[0] * 1000, workspace_coords[1] * 1000]
    if tentative_coords[0] < 0:
        tentative_coords[0] = 0
    elif tentative_coords[0] > 290:
        tentative_coords[0] = 290
    if tentative_coords[1] < 0:
        tentative_coords[1] = 0
    elif tentative_coords[1] > 290:
        tentative_coords[1] = 290
    return [int(tentative_coords[0]), int(tentative_coords[1])]