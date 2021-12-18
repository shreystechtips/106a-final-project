## EECS 106A Team 36 Sandbox Project Code

This README will outline the Code Structure for our work

```bash
Sandbox
├── Arduino (Open Source GRBL Software)
├── calibration_images (Data to Calibrate the RealSense)
├── Controls
│   ├── controller_manager.py (Interface between controller and server)
│   ├── controller.py (Generic Controller)
│   ├── finger_tracker_controller.py (Finger Tracking Drawing)
│   ├── point_tracker_controller.py (Normal Point drawing)
│   ├── presets.py (Preset Drawing Paths)
├── frontend (React Webapp)
│   ├── package.json (settings and all packages)
│   ├── src
│   │   ├── App.js (Main UI and interface code)
├── LED-Arduino (LED Control Script for LaunchPad)
│   └── LED-Control
│       └── LED-Control.ino
├── Perception
│   ├── ArUco Marker *.pdf (AR Tags)
│   ├── ball_detector.py (Ball detection Algorithm)
│   ├── calibration_matrix.yaml
│   ├── chessboard.pdf (Account for camera lens curvature)
│   ├── finger_tracker.py (Talks to the finger controller)
│   ├── gcode_points.py (Convert GCode to x,y points)
│   ├── hsv_range_detector.py (Naive Ball Tracking)
│   ├── main.py (The main file for finger tracking)
│   ├── server.py (Flask Server to interface with webapp)
│   ├── take_calibration_images.py (take images)
│   ├── camera_calibration.py (Calibrate the Camera from images)
│   ├── transform_receiver.py (Get camera transform)
│   ├── transformation_handler.py (Transform images)
│   └── trench_detector.py (stretch, detect 3d ridges)
├── requirements.txt (Installed python packages)
├── run.py
├── sandify.gcode
├── TestData (Data for steel ball testing and more system calibration)
├── TicTacToe (Framework/code for our interactive game, WIP)
```