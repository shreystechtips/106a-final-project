from abc import ABC, abstractmethod
from time import sleep
import numpy as np

class Controller(ABC):
    ''' IDLE means that the robot is not moving and is just waiting
        HOMING means that the $H command is being executed 
        TRACKING means that it is following a given trajectory
        BACKTRACKING means that the magnet is going back to the location of the ball
    '''
    states = {
        'IDLE': 0,
        'HOMING': 1,
        'TRACKING': 2,
        'BACKTRACKING': 3
    }

    def __init__(self, ser):
        self.set_idle()
        self.started_homing = False
        self.ball_position = np.array([0, 0])
        self.ser = ser

    def set_idle(self):
        self.state = Controller.states['IDLE']
    
    def set_home(self):
        self.state = Controller.states['HOMING']

    def set_tracking(self):
        self.state = Controller.states['TRACKING']

    def set_backtracking(self):
        self.state = Controller.states['BACKTRACKING']

    def update(self):
        if self.state == Controller.states['IDLE']:
            self.update_idle()
        elif self.state == Controller.states['HOMING']:
            if not self.started_homing:
                self.started_homing = True
                self.send_command('$H')
            else:
                sleep(0.05)
        elif self.state == Controller.states['TRACKING']:
            self.update_tracking()
        elif self.state == Controller.states['BACKTRACKING']:
            self.update_backtracking()

    def update_idle(self):
        sleep(0.05)

    @abstractmethod
    def update_tracking(self):
        pass

    @abstractmethod
    def update_backtracking(self):
        pass

    def send_command(self, command_string):
        self.ser.write(command_string.encode() + str.encode('\n'))

    def check_acknowledgement(self) -> bool:
        for c in self.ser.read():
            print(chr(c))
            if chr(c) == '\n':
                return True
        return False
    
    @abstractmethod
    def get_progress(self):
        pass
