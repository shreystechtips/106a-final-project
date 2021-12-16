import cv2 as cv
import numpy as np
from ball_detector import get_ball_location
from transform_receiver import get_camera_transform
from transformation_handler import invert_homogeneous_matrix
default_webcam = True
if not default_webcam:
    import pyrealsense2.pyrealsense2 as rs
# from server import app, curr_frame
from finger_tracker import get_index_finger_position

# class CustomServer(Server):
#     def __call__(self, app, *args, **kwargs):
#         #Hint: Here you could manipulate app
#         return Server.__call__(self, app, *args, **kwargs)

if __name__ == '__main__':
    ## start app, should be async
    
    # manager = Manager(app)
    # manager.add_command('runserver', CustomServer())
    # manager.run()
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
        while True:
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            output = get_index_finger_position(color_image)
            if output is not None:
                finger_x, finger_y = output[0], output[1]
                cv.circle(color_image, (output[0], output[1]), 15, (139, 0, 0), cv.FILLED)
            cv.imshow('frame',color_image)
            curr_frame = color_image
            transform = get_camera_transform(color_image)
            k = cv.waitKey(1) & 0xFF
            if k == 27:
                break

