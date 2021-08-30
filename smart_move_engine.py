import random

piecesScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0



def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1 
    opponentMinmaxScore = CHECKMATE
    bestplayerMove = None
    random.shuffle(validMoves)
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponentsMoves = gs.getValidMoves()
        opponentMaxScore = -CHECKMATE
        for opponentsMove in opponentsMoves:
            gs.makeMove(opponentsMove)
            if gs.checkmate:
                score = -turnMultiplier * CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if(score > opponentMaxScore):
                opponentMaxScore = score
            gs.undoMove()
        
        if opponentMaxScore < opponentMinmaxScore:
            opponentMinmaxScore = opponentMaxScore
            bestplayerMove = playerMove
        gs.undoMove()

    return bestplayerMove

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'W':
                score += piecesScore[square[1]]
            elif square[0] == 'b':
                score -= piecesScore[square[1]]
    
    return score


