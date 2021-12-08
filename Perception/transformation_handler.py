import numpy as np

marker_to_workspace_transformation = np.array([[1, 0, 0, 0],
                                               [0, 1, 0, 0],
                                               [0, 0, 1, 0],
                                               [0, 0, 0, 1]])

def invert_homogeneous_matrix(matrix: np.ndarray):
    ''' Inverts a homogeneous matrix given as matrix
    '''
    R = matrix[0:3, 0:3]
    T = matrix[0:3, 3:]
    R_t = R.T
    return np.block([[R_t, np.dot(R_t, -1 * T)],
                     [np.zeros((1,3)), 1]])


def convert_camera_vector_to_workspace(vector: np.array, camera_to_marker_transform: np.ndarray):
    ''' vector: (3,) numpy array in the camera frame
        output: (3,) numpy array in the workspace frame
    '''
    vector.append(1)
    marker_vector = np.dot(camera_to_marker_transform, vector)
    workspace_vector = np.dot(marker_to_workspace_transformation, marker_vector)
    return workspace_vector[0:3]