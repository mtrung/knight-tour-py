import pandas
from tabulate import tabulate

from position import Position, MaxPossMoves


class Board:
    def __init__(self, row=8, col=8):
        self.rowCount = row
        self.colCount = col
        columns = [i for i in range(1, col+1)]
        rows = [i for i in range(1, row+1)]
        self.board = pandas.DataFrame(columns=columns, index=rows)
        self.initBoard()

    def getMeta(self, x, y) -> Position:
        pos = self.board[x][y]
        if not pos or pandas.isnull(pos):
            pos = Position(x, y)
            self.board[x][y] = pos
        return pos

    # check if this position is valid or not
    def isValid(self, x, y) -> bool:
        return not (x < 1 or y < 1 or (x > self.colCount) or (y > self.rowCount))

    def getValidMoves(self, curr) -> list:
        # return a list of legal & unoccupied moves
        moves = []
        for moveNumber in range(MaxPossMoves):
            x, y = curr.getNextMove(moveNumber)
            if self.isValid(x, y):
                pos = self.getMeta(x, y)
                if pos.isUnoccupied():
                    moves.append(pos)
        if not moves:
            return moves

        moves = sorted(moves, key=lambda pos: pos.score)
        return moves

    def initBoard(self):
        # init board with position data
        for y in range(1, self.rowCount + 1):
            for x in range(1, self.colCount + 1):
                curr = self.getMeta(x, y)
                possibleMoves = self.getValidMoves(curr)
                curr.score = len(possibleMoves)

    def __str__(self):
        return tabulate(self.board, headers='keys', tablefmt='pipe', showindex=True)
