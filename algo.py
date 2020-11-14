from board import LogicsBoard, BoardPosition


class Algorithm:
    def __init__(self, row=8, col=8):
        self.rowCount = row
        self.colCount = col
        self.m_logicsBoard = LogicsBoard(row, col)

    def SetIndex(self, c, index):
        self.m_logicsBoard.GetPos(c).MoveIndex = index

    def GetIndex(self, c):
        return self.m_logicsBoard.GetPos(c).MoveIndex

    # def Init(self):
        #    for (i=1 i <= rowCount i++):
        #        for (j=1 j <= colCount j++):
        #            m_logicsBoard.GetPos(i, j).SetUnoccupied()

        # initialize the m_possibleMovesMatrix array
        # for (i=1 i <= rowCount i++):
        #     for (j=1 j <= colCount j++):
        #         PointI p = new PointI(i, j)
        #             m_logicsBoard.GetPos(
        #                 i, j).PossibleMovesCount = GetPossibleMovesCount(p)

    # def GetPossibleMovesCount(self, curr):
    #    return m_logicsBoard.GetPossibleMoves(curr).Count

    def DetermineNextMove(self, curr):
        # There can be multiple cells with the same lowest move count: up to 8
        # get smallest possible move count array for level 1
        L1Candidates = self.GetSmallestAccessArray(curr)
        if not L1Candidates:
            return -1

        if len(L1Candidates) == 1:
            return L1Candidates[0]

        # level 2 forward check
        smallestAccessValIndex_Level1 = 0
        candidatePos = L1Candidates[smallestAccessValIndex_Level1]
        smallestAccessVal_Level1 = candidatePos.PossibleMovesCount

        # designate 1st one is the smallest
        smallestAccessVal_Level2 = self.GetSmallestAccessVal(candidatePos)

        candidate_smallestAccessVal_Level2 = -1
        # for (level1_i=1 level1_i < L1Candidates.Count level1_i++):
        for i, item in enumerate(L1Candidates):
            candidate_smallestAccessVal_Level2 = self.GetSmallestAccessVal(
                L1Candidates[i])
            # if the level 2
            if (smallestAccessVal_Level2 > candidate_smallestAccessVal_Level2):
                smallestAccessValIndex_Level1 = i
                smallestAccessVal_Level2 = candidate_smallestAccessVal_Level2

        return L1Candidates[smallestAccessValIndex_Level1]

    def UpdateAccessibility(self, curr):
        PossiblePos = self.GetPossibleMovePositions(curr)
        for p in PossiblePos:
            p.PossibleMovesCount += -1

    def GetPossibleMovePositions(self, curr) -> list:
        PossiblePoints = self.m_logicsBoard.GetPossibleMoves(curr)
        # PossiblePos = []
        # for p in PossiblePoints:
        #    PossiblePos.Add(m_logicsBoard.GetPos(p))
        return PossiblePoints

    def GetSmallestAccess(self, Positions: list):
        if not Positions:
            return -1
        # smallestIndex = 0
        sortedList = sorted(Positions, key=lambda pos: pos.PossibleMovesCount)
        # for i, pos in enumerate(Positions):
        #     if (pos.PossibleMovesCount < Positions[smallestIndex].PossibleMovesCount):
        #         smallestIndex = i
        # smallestValue = Positions[smallestIndex].PossibleMovesCount
        return sortedList[0].PossibleMovesCount

    def GetSmallestAccessVal(self, curr):
        # Get all possible moves from a given position
        Positions = self.GetPossibleMovePositions(curr)
        return self.GetSmallestAccess(Positions)

    def GetSmallestAccessArray(self, curr) -> list:
        # Get all possible moves from a given position
        Positions = self.GetPossibleMovePositions(curr)
        if not Positions:
            return
        # Get the smallest value
        smallest = self.GetSmallestAccess(Positions)
        # Remove non-smallest positions
        # for (i=0 i < Positions.Count i++):
        # if (Positions[i].PossibleMovesCount > smallestValue):
        #         Positions.RemoveAt(i)
        #         i--
        # return Positions
        return [p for p in Positions if p.PossibleMovesCount <= smallest]

    def moveNext(self, curr):
        possibleMoves = self.m_logicsBoard.GetPossibleMoves(curr)
        if len(possibleMoves) == 0:
            return
        boardindex = self.GetIndex(curr)
        self.UpdateAccessibility(curr)
        curr = self.DetermineNextMove(curr)
        self.SetIndex(curr, boardindex + 1)
        return curr

    def solve(self, x, y):
        curr = BoardPosition(x, y)
        self.SetIndex(curr, 1)
        while True:
            curr = self.moveNext(curr)
            if not curr:
                return


algo = Algorithm()
algo.solve(1, 1)
print(algo.m_logicsBoard.toMdStr())
