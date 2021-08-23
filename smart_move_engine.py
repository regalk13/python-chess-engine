import random

piecesScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "K": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0



def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove():
    return


def scoreMaterial(gs, board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'W':
                score += piecesScore[square[1]]
            elif square[0] == 'b':
                score -= piecesScore[square[1]]
    
    return score


