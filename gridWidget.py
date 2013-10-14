from PyQt5 import QtCore, QtGui, QtWidgets
import grid

LINE_LENGTH = 20
LINE_THICKNESS = 1
LINE_THICKNESS_DRAWN = 3
LINE_THICKNESS_DRAWN_HALF = int(LINE_THICKNESS_DRAWN/2)
LINE_UNDRAWN = QtCore.Qt.gray
LINE_DRAWN = QtCore.Qt.black
LINE_LASTDRAWN = QtCore.Qt.red

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

	def initGridLines( self ):
		maxPos = self._grid.maxPos()
		for cell in range( maxPos+1 ):
			column, row, dir = self._grid.getCoord( cell )
			self.lines.append( GridLine( column, row, dir ) )
			
	def setLine( self, cell:int ):
		self.highlite( cell )
		self.repaint()
		
	def highlite( self, cell:int ):
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

		painter.end()

	@staticmethod
	def drawLine(line:GridLine, painter:QtGui.QPainter):
		pen = QtGui.QPen()
		pen.setColor(line.color)
		pen.setWidth(line.width)
		painter.setPen(pen)
		painter.drawLine(line.start, line.end)
