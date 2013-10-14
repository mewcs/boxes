class Grid(object):
	# HLINE corresponds to a horizontal line.
	HLINE = 0
	# VLINE corresponds to a vertical line.
	VLINE = 1

	def __init__(self, cols:int, rows:int):
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
		self._horiz = cols * (rows+1)
		# Number of vertical lines.
		self._vert = (cols+1) * rows

	# _validate validates the provided position. It raises an exception if the
	# provided position falls outside of the grid.
	def _validate(self, pos:int):
		if pos < 0 or pos > self.maxPos():
			raise Exception('position %d falls outside of the grid.' % (pos))

	# _hasLine returns True if the line at the provided position is already
	# marked as drawn.
	def _hasLine(self, pos:int) -> bool:
		self._validate(pos)
		# Check if the bit at the provided position is already set in the grid.
		if self._grid & 1<<pos != 0:
			return True
		else:
			return False

	# setLine tries to mark the line at the provided position as drawn. It
	# returns True on success and False if the line was already marked as drawn.
	def setLine(self, pos:int) -> bool:
		# Check if the line has already been marked as drawn. Note that _hasLine
		# also validates the provided position.
		if self._hasLine(pos):
			return False
		self._grid |= 1<<pos
		return True

	# getCoord returns the column and row numbers associated with a given
	# position. The boolean return argument indicates the orientation of the
	# line, which is either horizontal (HLINE) or vertical (VLINE).
	def getCoord(self, pos:int) -> (int, int, bool):
		self._validate(pos)
		if pos < self._horiz:
			row, col = divmod(pos, self._cols)
			return col, row, self.HLINE
		else:
			pos -= self._horiz
			row, col = divmod(pos, (self._cols+1))
			return col, row, self.VLINE

	# getPos returns the position associated with the provided column, row and
	# orientation.
	def getPos(self, col:int, row:int, orientation:bool) -> int:
		pass

	# completeBox returns true if the line at pos is part of a complete box.
	def completeBox(self, pos:int) -> bool:
		pass

	# maxPos returns the maximum valid position in the grid, which always
	# corresponds to the vertical line in the lower right corner.
	def maxPos(self) -> int:
		return self._horiz + self._vert - 1

	# drawnLines returns a list containing the positions of all lines that are
	# marked as drawn.
	def drawnLines(self) -> [int]:
		return [pos for pos in range(self.maxPos()+1) if self._hasLine(pos)]

def testGrid():
	grid = Grid(4, 2)
	if grid.setLine(0):
		print("was able to set line 0")
	if grid.setLine(12):
		print("was able to set line 12")
	if grid.setLine(21):
		print("was able to set line 21")
	print(grid.drawnLines())
	col, row, orientation = grid.getCoord(12)
	print("col:", col, "row:", row, "orientation:", orientation)

if __name__ == '__main__':
	testGrid()
