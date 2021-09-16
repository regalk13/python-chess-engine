import random

from pygame.constants import NUMEVENTS

piecesScore = {"K": 0, "Q": 10, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3



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
        if gs.stalemate:
            opponentMaxScore = STALEMATE

        elif gs.checkmate:
            opponentMinmaxScore = -CHECKMATE

        else:
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves:
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE
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

def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)
    findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove

    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            
            gs.undoMove()

        return maxScore


    else:   
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth -1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move

            gs.undoMove()

        return minScore


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move   
        gs.undoMove()
    return maxScore    


def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE

        else:
            return CHECKMATE

    elif gs.stalemate:
        return STALEMATE


    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'W':
                score += piecesScore[square[1]]
            elif square[0] == 'b':
                score -= piecesScore[square[1]]
    
    return score


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'W':
                score += piecesScore[square[1]]
            elif square[0] == 'b':
                score -= piecesScore[square[1]]
    
    return score


