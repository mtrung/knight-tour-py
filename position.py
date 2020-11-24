move_offsets = [(1, 2), (1, -2), (-1, 2), (-1, -2),
                (2, 1), (2, -1), (-2, 1), (-2, -1)]
MaxPossMoves = len(move_offsets)

positionValues = {
    'empty': None,
    'highlight':  None,
    '1st': None,
    'visited': None
}

def setPieceStyle(useIndex):
    global positionValues
    if useIndex:
        positionValues = {
            # https://en.wikipedia.org/wiki/Chess_symbols_in_Unicode
            'empty': '',
            'highlight': '♞',
            '1st': '△',
            'visited': '♘',
        }
    else:
        positionValues = {
            'empty': '![](https://upload.wikimedia.org/wikipedia/commons/f/f9/Reversi_OOt45.svg)',
            'highlight': '![](https://upload.wikimedia.org/wikipedia/commons/c/c8/Chess_ndl45.svg)',
            '1st': '![](https://upload.wikimedia.org/wikipedia/commons/c/c8/Chess_ndl45.svg)',
            'visited': '![](https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg)'
        }

setPieceStyle(True)

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # 0: unoccupied
        # >0: occupied, indicates order of the move
        self.moveIndex = 0
        # accessibility score = # possible moves from a position
        self.score = 0
        self.highlight = False

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
            return positionValues['empty'] if positionValues['empty'] else ''
        elif self.moveIndex == 1:
            return positionValues['1st'] if positionValues['1st'] else str(self.moveIndex)
        elif self.highlight:
            return positionValues['highlight'] if positionValues['highlight'] else str(self.moveIndex)
        return positionValues['visited'] if positionValues['visited'] else str(self.moveIndex)

