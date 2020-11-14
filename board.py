import pandas
from tabulate import tabulate

move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                (2, 1), (2, -1), (-2, 1), (-2, -1)]
MaxPossMoves = len(move_offsets)

class BoardPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # 0: unoccupied
        # >0: occupied, indicates order of the move
        self.moveIndex = 0
        # accessibility score
        self.score = 0

    def getNextMove(self, index):
        xoffset, yoffset = move_offsets[index]
        return (self.x + xoffset, self.y + yoffset)

    def isUnoccupied(self) -> bool:
        return self.moveIndex == 0

    def __str__(self):
        return f'{self.moveIndex}' if True else f'{self.moveIndex},{self.score}'


class Board:
    def __init__(self, row=8, col=8):
        self.rowCount = row
        self.colCount = col
        columns = [i for i in range(1, col+1)]
        rows = [i for i in range(1, row+1)]
        self.board = pandas.DataFrame(columns=columns, index=rows)
        self.initBoard()

    def getMeta(self, x, y) -> BoardPosition:
        pos = self.board[x][y]
        if not pos or pandas.isnull(pos):
            self.board[x][y] = BoardPosition(x, y)
        return self.board[x][y]

    # check if this position is valid or not
    def isValid(self, x, y) -> bool:
        return not (x < 1 or y < 1 or (x > self.colCount) or (y > self.rowCount))

    def getValidMoves(self, curr) -> list:
        # return a list of legal & unoccupied moves
        PossibleMoves = []
        for moveNumber in range(MaxPossMoves):
            x, y = curr.getNextMove(moveNumber)
            if self.isValid(x, y):
                pos = self.getMeta(x, y)
                if pos.isUnoccupied():
                    PossibleMoves.append(pos)
        return PossibleMoves

    def initBoard(self):
        # self.board.fillna(0, inplace=True)
        for y in range(1, self.rowCount + 1):
            for x in range(1, self.colCount + 1):
                possibleMoves = self.getValidMoves(BoardPosition(x, y))
                self.getMeta(x, y).score = len(possibleMoves)

    def toMdStr(self):
        return tabulate(self.board, headers='keys', tablefmt='pipe', showindex=True)
