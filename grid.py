class Grid(object):
    # HLINE corresponds to a horizontal line.
    HLINE = 0
    # VLINE corresponds to a vertical line.
    VLINE = 1

    def __init__(self, cols: int, rows: int):
        # _grid is a bitfield holding the draw state of each line. The boolean
        # state indicates if the line is drawn (1) or not drawn (0).
        #
        # Each line is associated with a bit position in the following way:
        # - First all horizontal lines are given a bit position, starting at the
        #   upper left and ending at the lower right portion of the grid. Their
        #   respective bit positions are within the range [0, self._horiz).
        # - Secondly all vertical lines are given a bit position, starting at the
        #   upper left and ending at the lower right portion of the grid. Their
        #   respective bit positions are within the range
        #   [self._horiz, self._horiz+self._vert).
        self._grid = 0
        # Number of columns in the grid.
        self._cols = cols
        # Number of rows in the grid.
        self._rows = rows
        # Number of horizontal lines.
        self._horiz = cols * (rows + 1)
        # Number of vertical lines.
        self._vert = (cols + 1) * rows

    def cols(self):
        """
        cols returns the number of columns on the grid.
        """
        return self._cols

    def rows(self):
        """
        rows returns the number of rows on the grid.
        """
        return self._rows

    def horiz(self):
        """
        horiz returns the number of horizontal lines on the grid.
        """
        return self._horiz

    def vert(self):
        """
        vert returns the number of vertical lines on the grid.
        """
        return self._vert

    def _validate(self, pos: int):
        """
        _validate validates the provided position. It raises an exception if the
        provided position falls outside of the grid.
        """
        if pos < 0 or pos > self.maxPos():
            raise Exception('position %d falls outside of the grid.' % (pos))

    def _hasLine(self, pos: int) -> bool:
        """
        _hasLine returns True if the line at the provided position is already
        marked as drawn.
        """
        self._validate(pos)
        # Check if the bit at the provided position is already set in the grid.
        if self._grid & 1 << pos != 0:
            return True
        else:
            return False

    def setLine(self, pos: int) -> bool:
        """
        setLine tries to mark the line at the provided position as drawn. It
        returns number of boxes completed by line drawn of -1 if the line was
        already marked as drawn.
        """
        # Check if the line has already been marked as drawn. Note that _hasLine
        # also validates the provided position.
        if self._hasLine(pos):
            return -1
        self._grid |= 1 << pos

        return len(self.completesBoxes(pos))

    def getCoord(self, pos: int) -> (int, int, bool):
        """
        getCoord returns the column and row numbers associated with a given
        position. The boolean return argument indicates the orientation of the
        line, which is either horizontal (HLINE) or vertical (VLINE).
        """
        self._validate(pos)
        if pos < self._horiz:
            row, col = divmod(pos, self._cols)
            return col, row, self.HLINE
        else:
            pos -= self._horiz
            row, col = divmod(pos, (self._cols + 1))
            return col, row, self.VLINE

    def getPos(self, col: int, row: int, orientation: bool) -> int:
        """
        Returns: the position associated with the provided column, row and
        orientation.
        """
        if orientation == self.HLINE:
            return (row * self._cols) + col
        else:
            return (self._horiz) + (row * (self._cols + 1)) + col

    def getBoxCoord(self, pos: int) -> (int, int):
        row, column = divmod(pos, self._rows)
        return column, row

    def getBoxPos(self, col: int, row: int) -> int:
        return (row * self._cols) + col

    def maxBox(self) -> int:
        return self._cols * self._rows

    def completesBoxes(self, pos: int) -> bool:
        """
        Returns: A list of zero to two indices of the boxes the argument pos
        completes.
        """
        col, row, orient = self.getCoord(pos)

        drawnLines = self.drawnLines()

        completedBoxes = list()

        # Check adjecent lines
        if orient == self.HLINE:
            # Above and below
            for i, i2 in zip([-1, 1], [-1, 0]):
                if row + i < 0 or row + i > self._rows:
                    continue
                x1 = self.getPos(col, row + i, orient) in drawnLines
                x2 = self.getPos(col, row + i2, not orient) in drawnLines
                x3 = self.getPos(col + 1, row + i2, not orient) in drawnLines

                if x1 and x2 and x3:
                    box_row = row + i2
                    box_col = col
                    completedBoxes.append(self.getBoxPos(box_col, box_row))

        else:
            for i, i2 in zip([-1, 1], [-1, 0]):
                if col + i < 0 or col + i > self._cols:
                    continue
                x1 = self.getPos(col + i, row, orient) in drawnLines
                x2 = self.getPos(col + i2, row, not orient) in drawnLines
                x3 = self.getPos(col + i2, row + 1, not orient) in drawnLines

                if x1 and x2 and x3:
                    box_row = row
                    box_col = col + i2
                    completedBoxes.append(self.getBoxPos(box_col, box_row))

        return completedBoxes

    def maxPos(self) -> int:
        """
        maxPos returns the maximum valid position in the grid, which always
        corresponds to the vertical line in the lower right corner.
        """
        return self._horiz + self._vert - 1

    def drawnLines(self) -> [int]:
        """
        Returns a list containing the positions of all lines that are marked as
        drawn.
        """
        return [pos for pos in range(self.maxPos() + 1) if self._hasLine(pos)]
