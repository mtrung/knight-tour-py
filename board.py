import pandas
from tabulate import tabulate

move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                (2, 1), (2, -1), (-2, 1), (-2, -1)]
MaxPossMoves = len(move_offsets)

class BoardPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.moveIndex = 0
        self.PossibleMovesCount = 0

    def getNextMove(self, index):
        xoffset, yoffset = move_offsets[index]
        return (self.x + xoffset, self.y + yoffset)

    def isUnoccupied(self) -> bool:
        return self.moveIndex == 0

    def __str__(self):
        return f'{self.moveIndex},{self.PossibleMovesCount}'


class Board:
    def __init__(self, row=8, col=8):
        self.rowCount = row
        self.colCount = col
        columns = [i for i in range(1, col+1)]
        rows = [i for i in range(1, row+1)]
        self.board = pandas.DataFrame(columns=columns, index=rows)
        # self.board = BoardPosition[colCount + 1, rowCount + 1]
        self.initBoard()

    def getMeta(self, x, y) -> BoardPosition:
        pos = self.board[x][y]
        if not pos or pandas.isnull(pos):
            self.board[x][y] = BoardPosition(x, y)
            # self.board[x][y].x = x
            # self.board[x][y].y = y
        return self.board[x][y]

    # def GetPos(self, c) -> BoardPosition:
    #     return self.getMeta(c.x, c.y)

    # check if this position is valid or not
    def IsPosValid(self, x, y) -> bool:
        return not (x < 1 or y < 1 or (x > self.colCount) or (y > self.rowCount))

    # check if the next position is valid and if it is occupied
    # def IsNextPosValid(self, x, y) -> bool:
    #     return (self.IsPosValid(x, y) and self.getMeta(x, y).isUnoccupied())

    def getValidMoves(self, curr) -> list:
        # return a list of legal & unoccupied moves
        PossibleMoves = []
        for moveNumber in range(MaxPossMoves):
            # next = curr.GetNextMove(horizontal[moveNumber], vertical[moveNumber])
            x, y = curr.getNextMove(moveNumber)
            if self.IsPosValid(x, y):
                pos = self.getMeta(x, y)
                if pos.isUnoccupied():
                    PossibleMoves.append(pos)
        return PossibleMoves
        # possibleMoveList = [curr.getNextMove(moveNumber)
        #                     for moveNumber in range(MaxPossMoves)]
        # validList = [self.board[x][y] for (x, y) in possibleMoveList if self.IsPosValid(x, y)]
        # for move in validList

    def initBoard(self):
        # self.board.fillna(0, inplace=True)
        for y in range(1, self.rowCount + 1):
            for x in range(1, self.colCount + 1):
                possibleMoves = self.getValidMoves(BoardPosition(x, y))
                self.getMeta(x, y).PossibleMovesCount = len(possibleMoves)

    def toMdStr(self):
        return tabulate(self.board, headers='keys', tablefmt='pipe', showindex=True)
