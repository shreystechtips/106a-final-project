import cv2 as cv
import numpy as np
from transform_receiver import get_camera_transform, camera_matrix, dist_coeffs, set_intrinsics
from transformation_handler import get_pixel_location_workspace_frame, invert_homogeneous_matrix, get_gcode_coords, get_pixel_location_camera_frame
default_webcam = False
if not default_webcam:
    import pyrealsense2.pyrealsense2 as rs
# from server import app, curr_frame
from finger_tracker import get_index_finger_position

import sys
sys.path.insert(0, '/home/user/106a-final-project/')
from Controls.controller_manager import ControllerManager

# class CustomServer(Server):
#     def __call__(self, app, *args, **kwargs):
#         #Hint: Here you could manipulate app
#         return Server.__call__(self, app, *args, **kwargs)

if __name__ == '__main__':
    ## start app, should be async
    
    # manager = Manager(app)
    # manager.add_command('runserver', CustomServer())
    # manager.run()
    control = ControllerManager()
    control.run_finger_tracker()
    if default_webcam:
        # cap = cv.VideoCapture('/home/shrey/106a-final-project/TestData/video-1638937380.mp4')
        cap = cv.VideoCapture(0)
        while(1):
            ret, frame = cap.read()
            # get_ball_location(frame)
            if ret:
                output = get_index_finger_position(frame)
                if output is not None:
                    cv.circle(frame, (output[0], output[1]), 15, (139, 0, 0), cv.FILLED)
                cv.imshow('frame',frame)
                curr_frame = frame
                cv.imwrite("frame.jpg", frame)
                transform = get_camera_transform(frame)
            k = cv.waitKey(1) & 0xFF
            if k == 27:
                break
        cv.destroyAllWindows()
    else:
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

        align_to = rs.stream.color
        align = rs.align(align_to)
        while True:
            frames = pipeline.wait_for_frames()
            aligned_frames = align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            depth_intrin = depth_frame.profile.as_video_stream_profile().intrinsics
            color_intrin = color_frame.profile.as_video_stream_profile().intrinsics
            fx = float(color_intrin.fx)
            fy = float(color_intrin.fy)
            ppx = float(color_intrin.ppx)
            ppy = float(color_intrin.ppy)
            axs = 0.0
            set_intrinsics(np.array([[fx, axs, ppx],
                                     [0.0, fy, ppy],
                                     [0.0, 0.0, 1.0]]))
            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            output = get_index_finger_position(color_image)
            if output is not None:
                finger_x, finger_y = output[0], output[1]
                cv.circle(color_image, (finger_x, finger_y), 15, (139, 0, 0), cv.FILLED)
                marker_to_camera_transform = get_camera_transform(color_image, debug=False)
                if marker_to_camera_transform is not None:                        
                    camera_to_marker_transform = invert_homogeneous_matrix(marker_to_camera_transform)
                    finger_in_workspace_frame = get_pixel_location_workspace_frame(finger_x, 
                                                finger_y, depth_frame, depth_intrin, camera_to_marker_transform)
                    finger_in_camera_frame = get_pixel_location_camera_frame(finger_x, 
                                                finger_y, depth_frame, depth_intrin)
                    # rvec, _ = cv.Rodrigues(np.array([[1.0, 0, 0],
                    #                               [0, 1.0 ,0],
                    #                               [0, 0.0, 1]]))
                    # print(finger_in_camera_frame)
                    # cv.aruco.drawAxis(color_image, camera_matrix, dist_coeffs, rvec, -1 * np.array(finger_in_camera_frame), 1)
                    finger_in_workspace_frame = get_pixel_location_workspace_frame(output[0], 
                                                output[1], depth_frame, depth_intrin, camera_to_marker_transform)
                    control.get_controller().finger_pos = finger_in_workspace_frame
                    print(finger_in_workspace_frame)
                    print(get_gcode_coords(finger_in_workspace_frame))
                    control.update_manager()
            cv.imshow('frame',color_image)
            k = cv.waitKey(1) & 0xFF
            if k == 27:
                break

