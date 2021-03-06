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

        self.moveFunctions = {'p':self.getPawnMoves, 'R': self.getRockMoves, 'N': self.getKnightMoves,
                            'B':self.getBishopMoves, 'Q':self.getQueenMoves, 'K':self.getKingMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.inCheck = False
        self.pins = []
        self.checkmate = False
        self.stalemate = False
        self.chescks = []
        self.enpassantPossible = ()
        self.currentClastingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentClastingRight.wks,self.currentClastingRight.bks,
                                            self.currentClastingRight.wqs, self.currentClastingRight.bqs)]

   def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentClastingRight.wks = False
            self.currentClastingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentClastingRight.bks = False
            self.currentClastingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentClastingRight.wqs = False
                elif move.startCol == 7:
                    self.currentClastingRight.wks = False

        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentClastingRight.bqs = False
                elif move.startCol == 7:
                    self.currentClastingRight.bks = False

   def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove


        if move.pieceMoved == 'wk':
            self.whiteKingLocation = (move.startRow, move.startCol)
        elif move.pieceMoved == 'bk':
            self.whiteKingLocation = (move.startRow, move.startCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'

        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)

        else:
            self.enpassantPossible = ()
       

        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #King Side Case
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = '--'
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = '--'

        # Castling
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentClastingRight.wks,self.currentClastingRight.bks, self.currentClastingRight.wqs, self.currentClastingRight.bqs ))

   def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove


            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)

            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()


            # undo castle rights
            self.castleRightsLog.pop()  # get rid of the new castle rights from the move we are undoing
            self.currentClastingRight = self.castleRightsLog[-1]
            # undo the castle move
            if move.isCastleMove:
                if move.endCol- move.startCol == 2:  # king-side
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:  # queen-side
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'


            self.checkmate = False
            self.stalemate = False

   def getValidMoves(self):  
        tempCastleRights = CastleRights(self.currentClastingRight.wks, self.currentClastingRight.bks, self.currentClastingRight.wqs, self.currentClastingRight.bqs)

        moves = []
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]

        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]

        if self.inCheck:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]

                else:
                    for i in range(1,8):
                        validSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[1] == checkCol:
                            break

                for i in range(len(moves) - 1, -1, -1):
                    if moves[i].pieceMoved[1] != 'K':
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])

            else:
                self.getKnightMoves(kingRow, kingCol, moves)

        else:
            moves = self.getAllPossibleMoves()
            if self.whiteToMove:
                self.getCastleMoves(self.whiteKingLocation[0],  self.whiteKingLocation[1], moves)
            else:
                self.getCastleMoves(self.blackKingLocation[0],  self.blackKingLocation[1], moves)
        if len(moves) == 0:
            if self.squareUnderAttack(kingRow, kingCol):
                self.checkmate = True

            else:
                self.stalemate = True

        else:
            self.checkmate = False
            self.stalemate = False

        self.currentClastingRight = tempCastleRights
        return moves

   def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.whiteToMove:
            enemyColor = "b"
            allyColor = "w"
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = "w"
            allyColor = "b"
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]

        directions = ((-1,0), (0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                    (i == 1 and type == 'p' and ((enemyColor == "w" and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                        (type == 'Q') or (i == 1 and type == 'K'):
                                            if possiblePin == ():
                                                inCheck = True
                                                checks.append((endRow, endCol, d[0], d[1]))
                                                break
                                            else:
                                                pins.append(possiblePin)
                                                break

                        else:
                            break

                else:
                    break

        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks

   def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])

        else:
             return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

   def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True

        return False

   def getQueenMoves(self, r, c, moves):
        self.getRockMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

   def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break

        knightMoves = ((-2,-1), (-2,1),(-1,-2), (-1,2), (1,-2),(1, 2), (2,-1),(2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c),(endRow, endCol), self.board))

   def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c+ d[1]* i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break
    
   def getKingMoves(self, r, c, moves):
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)        
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    
                    if allyColor == "w":
                        self.whiteKingLocation = (endRow, endCol)

                    else:
                        self.blackKingLocation = (endRow, endCol)

                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r,c), (endRow, endCol), self.board))
                    
                    if allyColor == 'w':
                        self.whiteKingLocation = (r,c)

                    else:
                        self.blackKingLocation = (r,c)


    
   def getCastleMoves(self, row, col, moves):
        """
        Generate all valid castle moves for the king at (row, col) and add them to the list of moves.
        """
        if self.squareUnderAttack(row, col):
            return  # can't castle while in check
        if (self.whiteToMove  and self.currentClastingRight) or (
                not self.whiteToMove and self.currentClastingRight.bks):
            self.getKingsideCastleMoves(row, col, moves)
        if (self.whiteToMove and self.currentClastingRight.wqs) or (
                not self.whiteToMove and self.currentClastingRight.bqs):
            self.getQueensideCastleMoves(row, col, moves)

   def getKingsideCastleMoves(self, row, col, moves):
        if self.board[row][col + 1] == '--' and self.board[row][col + 2] == '--':
            if not self.squareUnderAttack(row, col + 1) and not self.squareUnderAttack(row, col + 2):
                moves.append(Move((row, col), (row, col + 2), self.board, isCastleMove=True))

   def getQueensideCastleMoves(self, row, col, moves):
        if self.board[row][col - 1] == '--' and self.board[row][col - 2] == '--' and self.board[row][col - 3] == '--':
            if not self.squareUnderAttack(row, col - 1) and not self.squareUnderAttack(row, col - 2):
                moves.append(Move((row, col), (row, col - 2), self.board, isCastleMove=True))

   def getRockMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:
                            break
                else:
                    break
                    

   def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)

        return moves
                    
   def getPawnMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        
        if self.whiteToMove:
            move_amount = -1
            startRow = 6
            enemyColor = "b"
            kingRow, kingCol = self.whiteKingLocation

        else:
            move_amount = 1
            startRow = 1
            enemyColor = "w"
            kingRow, kingCol = self.blackKingLocation

        if self.board[r + move_amount][c] == "--":
            if not piecePinned or pinDirection == (move_amount, 0):
                    moves.append(Move((r, c), (r+move_amount, c), self.board))
                    if r == startRow and self.board[r+move_amount][c] == "--":
                        moves.append(Move((r,c), (r + 2* move_amount, c), self.board))
        if c-1 >= 0:
                if not piecePinned or pinDirection == (move_amount, -1):
                    if self.board[r + move_amount][c - 1][0] == enemyColor:
                        moves.append(Move((r,c), (r+move_amount,c-1),self.board))

                elif (r+move_amount, c-1) == self.enpassantPossible:
                        attaking_piece = blocking_piece = False
                        if kingRow == r:
                            if kingCol < c:
                                inside_range = range(kingCol + 1, c -1)
                                outside_range = range(c + 1, 8)

                            else:
                                inside_range = range(kingCol -1, c, -1)
                                outside_range = range(c -2, -1,-1)

                            for i in inside_range:
                                if self.board[r][i] != '--':
                                    blocking_piece = True

                            for i in outside_range:
                                square = self.board[r][i]
                                if square[0] == enemyColor and (square[1] == 'R' or square[1] == 'Q'):
                                    attaking_piece = True
                                elif square != "--":
                                    blocking_piece = True
                        if not attaking_piece or blocking_piece:
                            moves.append(Move(r,c), (r+move_amount, c-1), self.board, enpassantPossible=True)
        if c + 1 <= 7:
                if not piecePinned or pinDirection == (move_amount, -1):
                    if self.board[r + move_amount][c + 1][0] == (move_amount, +1):    
                        moves.append(Move((r,c), (r+move_amount,c+1),self.board))

                elif (r+move_amount, c+1) == self.enpassantPossible:
                    attaking_piece = blocking_piece = False
                    if kingRow == r:
                        if kingCol < c:
                            inside_range = range(kingCol + 1, c)
                            outside_range = range(c +2, 8)
                        else:
                            inside_range = range(kingCol -1, c +1, -1)
                            outside_range = range(c - 1, -1, -1)

                        for i in inside_range:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attaking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    
                    if not attaking_piece or blocking_piece:
                        moves.append(Move((r, c), (r+move_amount, c+1), self.board, enpassantPossible=True))
        
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
        ranksToRows = {"1": 7, "2": 6, "3": 5, "4":4,
                    "5": 3, "6": 2, "7": 1, "8": 0}

        rowsToRanks = {v:k for k, v in ranksToRows.items()}
        filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                        "e": 4, "f":5, "g":6, "h":7}

        colsToFiles = {v: k for k,v in filesToCols.items()}


        def __init__(self, startSq, endSq, board, enpassantPossible=False, isCastleMove=False):
            self.startRow = startSq[0]
            self.startCol = startSq[1]
            self.endRow = endSq[0]
            self.endCol = endSq[1]
            self.pieceMoved = board[self.startRow][self.startCol]
            self.pieceCaptured = board[self.endRow][self.endCol]
            self.isPawnPromotion = False
            self.isPawnPromotion = (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7)

            self.isEnpassantMove = enpassantPossible
            if self.isEnpassantMove:
                self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
            
            self.isCastleMove = isCastleMove

            self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        
        
        #Overriding the Method

        def __eq__(self, other):
            if isinstance(other, Move):
                return self.moveID == other.moveID

            return False


        def getChessNotation(self):
            return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

        def getRankFile(self, r, c):
           return self.colsToFiles[c] + self.rowsToRanks[r]
