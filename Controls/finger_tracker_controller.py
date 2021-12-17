from Controls.controller import Controller
import numpy as np
from Perception.transformation_handler import get_gcode_coords
import queue

class FingerTracker(Controller):

    # Units in mm
    epsilon = 1
    max_indices_behind = 5

    def __init__(self, ser):
        super().__init__(ser)
        self.points = queue.Queue()
        self.finger_pos = np.array([0, 0, 100])
        self.prev_finger_pos = np.array([0, 0])
        self.reset_values()

    def reset_values(self):
        self.index_finished = False
        self.index_started = False

    def add_target_point(self, point):
        self.points.put(point)
        self.set_tracking()
    
    def check_for_new_point(self):
        if self.finger_pos[2] < 0.15:
            gcode_coords = get_gcode_coords(self.finger_pos)
            if np.linalg.norm(self.prev_finger_pos - np.array(gcode_coords)) > 50:
                self.add_target_point(gcode_coords)
                self.prev_finger_pos = np.array(gcode_coords)

    def update_idle(self):
        self.check_for_new_point()
    
    def update_tracking(self):
        self.check_for_new_point()
        if self.points.empty():
            return
        self.send_to_coords(self.points.get())

    def update_backtracking(self):
        # Uses straight line tracking to get back to ball (will change if bad)
        self.curr_index = max(0, self.completed_index)
        self.set_tracking()

    def send_to_coords(self, coords):
        ''' Moves magnet mechanism to specify coordinates in "coords"
            Input coords in a np.array of size (2,) representing x, y in millimeters in workspace frame 
        '''
        self.send_command(f'G01 X{coords[0]} Y{coords[1]} F5000')

    def get_progress(self):
        return self.curr_index / len(self.points)
