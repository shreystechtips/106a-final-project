import random

class HumanBot():
    def __init__(self, player):
        self.player = player
        self.is_human = True

    def select_move(self, board):
        candidates = board.get_legal_moves()
        # Wait for CV to detect move
        move = None # Initiate finger detection HERE
        # move = random.choice(candidates)
        
        # Validates move by comparing to candidates
        if move in candidates:
            # Returns move (row, col)
            return move
        else:
            # Invalid move
            return None