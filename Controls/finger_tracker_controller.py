from Controls.controller import Controller
import numpy as np
from Perception.transformation_handler import get_gcode_coords

class FingerTracker(Controller):

    # Units in mm
    epsilon = 1
    max_indices_behind = 5

    def __init__(self, ser):
        super().__init__(ser)
        self.points = []
        self.finger_pos = np.array([0, 0, 100])
        self.prev_finger_pos = np.array([0, 0])
        self.reset_values()

    def reset_values(self):
        self.curr_index = 0
        self.index_finished = False
        self.index_started = False

    def add_target_point(self, point):
        self.points.append(point)
        self.set_tracking()
    
    def check_for_new_point(self):
        if self.finger_pos[2] < 0.4:
            gcode_coords = get_gcode_coords(self.finger_pos)
            if np.linalg.norm(self.prev_finger_pos - np.array(gcode_coords)) > 50:
                self.add_target_point(gcode_coords)
                self.prev_finger_pos = np.array(gcode_coords)
                print(gcode_coords)

    def update_idle(self):
        self.check_for_new_point()
    
    def update_tracking(self):
        self.check_for_new_point()
        if self.curr_index >= len(self.points):
            self.set_idle()
            return
#        if self.curr_index - self.completed_index > PointTracker.max_indices_behind:
#           self.set_backtracking()
#            return
        if self.index_finished:
            self.curr_index += 1
            self.index_finished = False
            self.index_started = False
            return
        if not self.index_started:
            self.send_to_coords(self.points[self.curr_index])
            self.index_started = True
        else:
            if self.check_acknowledgement():
                self.index_finished = True

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
