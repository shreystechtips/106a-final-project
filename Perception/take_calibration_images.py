import cv2 as cv
import numpy as np
# Run from main directory, not Perception directory

counter = 0
default_webcam = False
if not default_webcam:
    import pyrealsense2.pyrealsense2 as rs 

if default_webcam:
    video_cap = cv.VideoCapture(0)
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

        image = np.asanyarray(color_frame.get_data())

        cv.imshow('Image', image)
        k = cv.waitKey(1)
        if k == ord('p'):
            cv.imwrite(f'calibration_image{counter}.jpg', image)
            counter += 1