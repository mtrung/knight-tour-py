import pandas
from tabulate import tabulate

horizontal = [2, 1, -1, -2, -2, -1, 1, 2]
vertical = [-1, -2, -2, -1, 1, 2, 2, 1]
MaxPossMoves = len(horizontal)
move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                (2, 1), (2, -1), (-2, 1), (-2, -1)]


class BoardPosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.MoveIndex = 0
        self.PossibleMovesCount = 0

    def GetNextMove(self, xoffset, yoffset):
        return BoardPosition(self.x + xoffset, self.y + yoffset)

    def nextMove(self, index):
        xoffset, yoffset = move_offsets[index]
        return BoardPosition(self.x + xoffset, self.y + yoffset)

    def isInvalid(self):
        return self.x < 1 or self.y < 1

    def IsUnoccupied(self) -> bool:
        return self.MoveIndex == 0

    def SetUnoccupied(self):
        self.MoveIndex = 0

    def __str__(self):
        return f'{self.MoveIndex}'


class LogicsBoard:
    def __init__(self, row=8, col=8):
        self.rowCount = row
        self.colCount = col
        columns = [i for i in range(1, col+1)]
        rows = [i for i in range(1, row+1)]
        self.m_board = pandas.DataFrame(columns=columns, index=rows)
        # self.m_board = BoardPosition[colCount + 1, rowCount + 1]
        self.initBoard()

    def GetPos2(self, x, y) -> BoardPosition:
        pos = self.m_board[x][y]
        if not pos or pandas.isnull(pos):
            self.m_board[x][y] = BoardPosition(x, y)
            # self.m_board[x][y].x = x
            # self.m_board[x][y].y = y
        return self.m_board[x][y]

    def GetPos(self, c) -> BoardPosition:
        return self.GetPos2(c.x, c.y)

    # check if this position is valid or not
    def IsPosValid(self, pos1) -> bool:
        return not (pos1.isInvalid() or (pos1.x > self.colCount) or (pos1.y > self.rowCount))

    # check if the next position is valid and if it is occupied
    def IsNextPosValid(self, next) -> bool:
        return (self.IsPosValid(next) and self.GetPos(next).IsUnoccupied())

    def GetPossibleMoves(self, curr) -> list:
        # PossibleMoves = []
        # for moveNumber in range(MaxPossMoves):
        #     # next = curr.GetNextMove(horizontal[moveNumber], vertical[moveNumber])
        #     next = curr.nextMove(moveNumber)
        #     if (self.IsNextPosValid(next)):
        #         PossibleMoves.append(next)
        # return PossibleMoves
        possibleMoveList = [curr.nextMove(moveNumber)
                            for moveNumber in range(MaxPossMoves)]
        return [self.m_board[next.x][next.y] for next in possibleMoveList if self.IsNextPosValid(next)]

    def initBoard(self):
        # self.m_board.fillna(0, inplace=True)
        for y in range(1, self.rowCount + 1):
            for x in range(1, self.colCount + 1):
                possibleMoves = self.GetPossibleMoves(BoardPosition(x, y))
                self.GetPos2(x, y).PossibleMovesCount = len(possibleMoves)

    def toMdStr(self):
        return tabulate(self.m_board, headers='keys', tablefmt='pipe', showindex=True)
