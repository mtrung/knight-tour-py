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
            # debug
            return f'{self.moveIndex},{self.score}'
        if self.moveIndex == 0:
            return '![0](https://upload.wikimedia.org/wikipedia/commons/f/f9/Reversi_OOt45.svg)'
        elif self.moveIndex == 1:
            return f'![{self.moveIndex}](https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg)'
        hl = f'![{self.moveIndex}](https://upload.wikimedia.org/wikipedia/commons/c/c8/Chess_ndl45.svg)'
        return hl if self.hightlight else str(self.moveIndex)
