import copy
from player import Player

class Board():
    def __init__(self):
        self.dimension = 3
        self.grid = [ [ None for y in range (self.dimension) ] for x in range (self.dimension ) ]
        self.grid_drawn = [ [ None for y in range (self.dimension) ] for x in range (self.dimension ) ]
        self.moves = []
        
        # draw_board() -> use ball to draw TicTacToe board
        
    def has_winner(self):        
        # need at least 5 moves before x hits three in a row
        if (len(self.moves) < 5):
            return None
        
        # check rows for win
        for row in range(self.dimension):
            unique_rows = set(self.grid[row])
            if (len(unique_rows) == 1):
                value = unique_rows.pop()
                if (value != None):
                    return value
                    
        # check columns for win
        for col in range(self.dimension):
            unique_cols = set()
            for row in range(self.dimension):
                unique_cols.add(self.grid[row][col])

            if (len(unique_cols) == 1):
                value = unique_cols.pop()
                if (value != None):
                    return value

        # check backwards diagonal (top left to bottom right) for win
        backwards_diag = set()
        backwards_diag.add(self.grid[0][0])
        backwards_diag.add(self.grid[1][1])
        backwards_diag.add(self.grid[2][2])

        if (len(backwards_diag) == 1):
            value = backwards_diag.pop()
            if (value != None):
                return value

        # check forwards diagonal (bottom left to top right) for win
        forwards_diag = set()
        forwards_diag.add(self.grid[2][0])
        forwards_diag.add(self.grid[1][1])
        forwards_diag.add(self.grid[0][2])

        if (len(forwards_diag) == 1):
            value = forwards_diag.pop()
            if (value != None):
                return value
        
        # found no winner, return None
        return None
    
    def make_move(self, row, col, player):
        if (self.is_space_empty(row, col)):
            self.grid[row][col] = player
            self.moves.append([row,col])
        else:
            raise Exception("Attempting to move onto already occupied space")
    
    def draw_move(self, row, col, player):
        # player = X or O
        # Send command to draw either X or O symbol in specified row / col in sand
        pass

    def last_move(self):
        return self.moves[-1]

    def is_space_empty(self, row, col):
        return self.grid[row][col] is None

    def get_legal_moves(self):
        choices = []
        for row in range(self.dimension):
            for col in range(self.dimension):
                if (self.is_space_empty(row, col)):
                    choices.append([row,col])
        return choices
                
    def __deepcopy__(self, memodict={}):
        dp = Board()
        dp.grid = copy.deepcopy(self.grid) 
        dp.moves = copy.deepcopy(self.moves)
        return dp  