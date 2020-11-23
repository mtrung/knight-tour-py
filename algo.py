from board import Board
import random


class Algorithm:
    def __init__(self, row=8, col=8):
        self.rowCount = row
        self.colCount = col
        self.board = None
        self.curr = None

    def __str__(self) -> str:
        return str(self.board) if self.board else ''

    def solve(self, x, y):
        self.placeAt(x, y)
        while self.move():
            pass
        return True

    def placeAt(self, x=None, y=None, index=None):
        if not x:
            x = random.randint(1, 8)
            y = random.randint(1, 8)
        self.board = Board(self.rowCount, self.colCount)
        self.curr = self.board.getMeta(x, y)
        self.curr.highlight = True
        self.curr.moveIndex = index if index else 1
        return self.curr

    def calcNextMove(self, neighbors):
        # There can be multiple neighbors with the same lowest score: up to 8
        # Breaking tie is important
        # Forward looking to next neighbor
        # get lowestNextNeighborScore possible move count array for level 1
        neighbors = self.getLowestScoreNeighbors(neighbors)
        if not neighbors:
            return
        if len(neighbors) == 1:
            return neighbors[0]

        chosenNeighbor = None
        lowestNextNeighborScore = 8
        for neighbor in neighbors:
            nextNeighborScore = self.getNeighborLowestScore(neighbor)
            if (lowestNextNeighborScore > nextNeighborScore):
                lowestNextNeighborScore = nextNeighborScore
                chosenNeighbor = neighbor
        return chosenNeighbor

    def updateNeighborScores(self, curr):
        validMoves = self.board.getValidMoves(curr)
        if not validMoves:
            return
        for move in validMoves:
            move.score -= 1
        return validMoves

    def getNeighborLowestScore(self, curr) -> int:
        # Returns the lowest accessibility value from a given position
        validMoves = self.board.getValidMoves(curr)
        if not validMoves:
            return
        return validMoves[0].score

    def getLowestScoreNeighbors(self, neighbors) -> list:
        # Return the lowest accessibility moves from a given position
        # assume neighbors list is sorted
        lowestNextNeighborScore = neighbors[0].score
        return [move for move in neighbors if move.score <= lowestNextNeighborScore]

    def move(self):
        if not self.curr:
            return
        neighbors = self.updateNeighborScores(self.curr)
        if not neighbors:
            return
        moveIndex = self.curr.moveIndex
        if moveIndex != 1:
            self.curr.highlight = False
        self.curr = self.calcNextMove(neighbors)
        self.curr.moveIndex = moveIndex + 1
        self.curr.highlight = True
        return self.curr


algo = Algorithm()
algo.solve(2, 2)
print(algo)
