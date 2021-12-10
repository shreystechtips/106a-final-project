from Controls.controller import Controller
import serial
from time import sleep
from Controls.point_tracker_controller import PointTracker

class ControllerManager:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.2)
        # Wake up the serial connection!
        self.ser.write(str.encode("\r\n\r\n"))
        sleep(2)
        self.ser.flushInput()
        print('Starting Serial Connection!')
        self.controller = PointTracker(self.ser)
        self.controller.send_command("\n")
#        self.controller = PointTracker(self.ser)
        input("hit enter once 12v in")
        print('Attempting to home')
        self.controller.send_command('$H')
        it = self.ser.readline()
        print(it)
        iter = 0
        person = ""
        while person != "x" and ">G1X10F2000:ok" not in str(it):
            sleep(0.1)
            #person = input("ree")
            it = self.ser.readline()
            print(it)
            if iter % 30 == 0:
                person = input("enter")
            iter +=1 
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
        return not(self.controller.state == Controller.states['TRACKING'] or self.controller.state == Controller.states['BACKTRACKING'])

    def get_progress(self):
        return self.controller.get_progress()
