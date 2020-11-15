move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                (2, 1), (2, -1), (-2, 1), (-2, -1)]
MaxPossMoves = len(move_offsets)


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # 0: unoccupied
        # >0: occupied, indicates order of the move
        self.moveIndex = 0
        # accessibility score = # possible moves from a position
        self.score = 0
        self.hightlight = False

    def getNextMove(self, index):
        xoffset, yoffset = move_offsets[index]
        return (self.x + xoffset, self.y + yoffset)

    def isUnoccupied(self) -> bool:
        return self.moveIndex == 0

    def __str__(self):
        if False:
            return f'{self.moveIndex},{self.score}'
        if self.moveIndex == 0:
            return ''
        return f'**{self.moveIndex}**' if self.hightlight else str(self.moveIndex)
