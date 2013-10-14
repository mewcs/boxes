from PyQt5 import QtCore, QtGui, QtWidgets
import grid

LINE_LENGTH = 20
LINE_THICKNESS = 1
LINE_THICKNESS_DRAWN = 3
LINE_THICKNESS_DRAWN_HALF = int(LINE_THICKNESS_DRAWN/2)
LINE_UNDRAWN = QtCore.Qt.gray
LINE_DRAWN = QtCore.Qt.black
LINE_LASTDRAWN = QtCore.Qt.red
LINE_MOUSE = QtCore.Qt.yellow

class GridLine( object ):
	def __init__( self, column:int, row:int, dir:int ):
		pad = LINE_THICKNESS_DRAWN_HALF
		self.start = QtCore.QPoint()
		self.start.setX( pad + column*LINE_LENGTH )
		self.start.setY( pad + row*LINE_LENGTH )
		self.end = QtCore.QPoint()
		if( dir == grid.Grid.VLINE ):
			self.end.setX( self.start.x() )
			self.end.setY( self.start.y()+LINE_LENGTH )

		elif( dir == grid.Grid.HLINE ):
			self.end.setX( self.start.x()+LINE_LENGTH )
			self.end.setY( self.start.y() )

		self.color = LINE_UNDRAWN
		self.width = LINE_THICKNESS

class GridWidget( QtWidgets.QWidget ):
	def __init__( self, grid : grid.Grid ):
		super(GridWidget, self).__init__()
		self._grid = grid
		self.lines = list()
		self.initGridLines()
		self.show()
		self._lastLineId = None
		self._prevMousePos = None
		self.setMouseTracking(True)

	def initGridLines( self ):
		maxPos = self._grid.maxPos()
		for cell in range( maxPos+1 ):
			column, row, dir = self._grid.getCoord( cell )
			self.lines.append( GridLine( column, row, dir ) )

	def addLine( self, cell:int ):
		self._grid.setLine( cell )
		self.highlight( cell )
		self.repaint()

	def highlight( self, cell:int ):
		if self._lastLineId is not None:
			self.lines[ self._lastLineId ].color = LINE_DRAWN
		self._lastLineId = cell
		self.lines[ cell ].color = LINE_LASTDRAWN
		self.lines[ cell ].width = LINE_THICKNESS_DRAWN

	def paintEvent(self, event):
		painter = QtGui.QPainter()
		painter.begin(self)

		# draw background grid.
		for line in self.lines:
			if line.color == LINE_UNDRAWN:
				self.drawLine(line, painter)

		# draw previous lines.
		for line in self.lines:
			if line.color == LINE_DRAWN:
				self.drawLine(line, painter)

		# draw last line.
		if self._lastLineId is not None:
			line = self.lines[self._lastLineId]
			self.drawLine(line, painter)

		# draw mouse lines.
		for line in self.lines:
			if line.color == LINE_MOUSE:
				self.drawLine(line, painter)

		painter.end()

	@staticmethod
	def drawLine(line:GridLine, painter:QtGui.QPainter):
		pen = QtGui.QPen()
		pen.setColor(line.color)
		pen.setWidth(line.width)
		painter.setPen(pen)
		painter.drawLine(line.start, line.end)

	def mouseMoveEvent(self, event):
		x = event.x()
		y = event.y()
		pos = self.locateLine(x, y)

		# Ignore the mouse event if the position hasn't changed since last time.
		if self._prevMousePos == pos:
			return

		# Restore the line color at the previous mouse position.
		if self._prevMousePos is not None:
			self.lines[self._prevMousePos].color = LINE_UNDRAWN
			self.lines[self._prevMousePos].width = LINE_THICKNESS

		# Return if no line was located at the mouse cursor coordinates.
		if pos is None:
			self._prevMousePos = None
			self.repaint()
			return

		print("hover at pos:", pos)
		line = self.lines[pos]
		if line.color == LINE_UNDRAWN:
			self._prevMousePos = pos
			self.lines[pos].color = LINE_MOUSE
			self.lines[pos].width = LINE_THICKNESS_DRAWN
			self.repaint()

	def mousePressEvent(self, event):
		x = event.x()
		y = event.y()
		pos = self.locateLine(x, y)

		# Return if no line was located at the mouse cursor coordinates.
		if pos is None:
			return

		print("click at pos:", pos)

	def locateLine(self, x:int, y:int) -> int:
		pad = LINE_THICKNESS_DRAWN_HALF + 1
		for pos in range(len(self.lines)):
			line = self.lines[pos]
			if pos < self._grid._horiz:
				# Horizontal line.
				xpad = 0
				ypad = pad
			else:
				# Vertical line.
				xpad = pad
				ypad = 0
			if line.start.x()-xpad <= x <= line.end.x()+xpad and line.start.y()-ypad <= y <= line.end.y()+ypad:
				return pos
		return None
