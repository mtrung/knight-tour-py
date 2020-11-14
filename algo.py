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

    def calcNextMove(self, neighbors):
        # There can be multiple neighbors with the same lowest accessibility: up to 8
        # get smallest_l2 possible move count array for level 1
        neighbors = self.getLowestScoreNeighbors(neighbors)
        if not neighbors:
            return
        if len(neighbors) == 1:
            return neighbors[0]

        chosenNeighbor = None
        smallest_l2 = 8
        for neighbor in neighbors:
            neighbor_l2 = self.getNeighborLowestScore(neighbor)
            if (smallest_l2 > neighbor_l2):
                smallest_l2 = neighbor_l2
                chosenNeighbor = neighbor
        return chosenNeighbor

    def updateNeighborScores(self, curr):
        moves = self.getValidMoves(curr)
        if not moves:
            return
        for move in moves:
            move.score -= 1
        return moves

    def getValidMoves(self, curr, toSort=True) -> list:
        l = self.board.getValidMoves(curr)
        return l if not toSort or not l else sorted(l, key=lambda pos: pos.score)

    def getNeighborLowestScore(self, curr) -> int:
        # Returns the lowest accessibility value from a given position
        validMoves = self.getValidMoves(curr)
        if not validMoves:
            return
        return validMoves[0].score

    def getLowestScoreNeighbors(self, neighbors) -> list:
        # Return the lowest accessibility moves from a given position
        # assume neighbors list is sorted
        smallest_l2 = neighbors[0].score
        return [move for move in neighbors if move.score <= smallest_l2]

    def move(self, curr):
        neighbors = self.updateNeighborScores(curr)
        if not neighbors:
            return
        moveIndex = curr.moveIndex
        curr = self.calcNextMove(neighbors)
        curr.moveIndex = moveIndex+1
        return curr


algo = Algorithm()
algo.solve(2, 2)
print(algo.board.toMdStr())
