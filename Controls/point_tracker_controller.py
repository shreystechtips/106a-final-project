from controller import Controller
import numpy as np

class PointTracker(Controller):

    # Units in mm
    epsilon = 1
    max_indices_behind = 5

    def __init__(self, ser):
        super().__init__(ser)
        self.points = []
        self.reset_values()

    def reset_values(self):
        self.curr_index = 0
        self.index_finished = False
        self.index_started = False
        self.completed_index = -1

    def load_new_points(self, points):
        self.set_idle()
        self.reset_values()        
        self.points = points
        self.set_tracking()

    def update_tracking(self):
        if self.curr_index >= len(self.points):
            self.set_idle()
            return
        if np.linalg.norm(self.ball_position - np.array(self.points[self.completed_index+1])) <= PointTracker.epsilon:
            self.completed_index += 1
        if self.curr_index - self.completed_index > PointTracker.max_indices_behind:
            self.set_backtracking()
            return
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
        self.send_command(f'G01 X{coords[0]} Y{coords[1]}')

    def get_progress(self):
        return self.curr_index / len(self.points)