from board import Board, BoardPosition


class Algorithm:
    def __init__(self, row=8, col=8):
        self.board = Board(row, col)

    def solve(self, x, y):
        curr = self.placeAt(x, y)
        while True:
            curr = self.move(curr)
            if not curr:
                return
        return True

    def placeAt(self, x, y, index=None):
        pos = self.board.getMeta(x, y)
        pos.moveIndex = index if index else pos.moveIndex+1
        return pos

    def calcNextMove(self, curr):
        # There can be multiple neighbors with the same lowest accessibility: up to 8
        # get smallest_l2 possible move count array for level 1
        neighbors = self.getSmallestAccessibilityList(curr)
        if not neighbors:
            return
        if len(neighbors) == 1:
            return neighbors[0]

        chosenNeighbor = None
        smallest_l2 = 8
        for neighbor in neighbors:
            neighbor_l2 = self.getSmallestAccessibility(neighbor)
            if (smallest_l2 > neighbor_l2):
                smallest_l2 = neighbor_l2
                chosenNeighbor = neighbor
        return chosenNeighbor

    def updateAccessibility(self, curr):
        moves = self.getValidMoves(curr)
        for move in moves:
            move.PossibleMovesCount -= 1

    def getValidMoves(self, curr, toSort=False) -> list:
        l = self.board.getValidMoves(curr)
        return l if not toSort or not l else sorted(l, key=lambda pos: pos.PossibleMovesCount)

    def getSmallestAccessibility(self, curr) -> int:
        # Returns the lowest accessibility value from a given position
        validMoves = self.getValidMoves(curr, toSort=True)
        if not validMoves:
            return
        return validMoves[0].PossibleMovesCount

    def getSmallestAccessibilityList(self, curr) -> list:
        # Return the lowest accessibility moves from a given position
        validMoves = self.getValidMoves(curr, toSort=True)
        if not validMoves:
            return
        smallest_l2 = validMoves[0].PossibleMovesCount
        return [move for move in validMoves if move.PossibleMovesCount <= smallest_l2]

    def move(self, curr):
        possibleMoves = self.board.getValidMoves(curr)
        if len(possibleMoves) == 0:
            return
        boardindex = curr.moveIndex
        self.updateAccessibility(curr)
        curr = self.calcNextMove(curr)
        curr.moveIndex = boardindex+1
        return curr


algo = Algorithm()
algo.solve(2, 2)
print(algo.board.toMdStr())
