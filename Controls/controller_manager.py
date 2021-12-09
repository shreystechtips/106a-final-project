from Controls.controller import Controller
import serial
from time import sleep
from point_tracker_controller import PointTracker

class ControllerManager:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.2)
        # Wake up the serial connection!
        self.ser.write(str.encode("\r\n\r\n"))
        sleep(2)
        self.ser.flushInput()
        print('Starting Serial Connection!')
        self.controller = PointTracker(self.ser)
        print('Attempting to home')
        self.controller.set_home()

    def update_manager(self):
        self.controller.update()

    def draw_points(self, points):
        self.controller.load_new_points(points)

    def pause_drawing(self):
        self.controller.set_idle()

    def update_ball_location(self, ball_position):
        self.controller.ball_position = ball_position

    def is_done(self):
        return self.controller.state == Controller.states['TRACKING'] or self.controller.state == Controller.states['BACKTRACKING']

    def get_progress(self):
        return self.controller.get_progress()