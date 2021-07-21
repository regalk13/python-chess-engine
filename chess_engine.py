

class GameState():
    def __init__(self):
        # 8x8 Board on a 2d list, each element has 2 characters.
        # First character represents the color of the piece.
        # Second represents the type of the pice.
        # "--" empty space.
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--","--"],
            ["--", "--", "--", "--", "--", "--", "--","--"],
            ["--", "--", "--", "--", "--", "--", "--","--"],
            ["--", "--", "--", "--", "--", "--", "--","--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.whiteToMove = True
        self.moveLog = []