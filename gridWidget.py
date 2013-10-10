from PyQt5 import QtCore, QtGui, QtWidgets
import grid

LINE_LENGTH = 20
LINE_THICKNESS = 1
LINE_THICKNESS_DRAWN = 3
LINE_UNDRAWN = QtCore.Qt.gray
LINE_DRAWN = QtCore.Qt.black
LINE_LASTDRAWN = QtCore.Qt.red

class GridLine( object ):
	def __init__( self, column:int, row:int, dir:int ):
		self.start = QtCore.QPoint()
		self.start.setX( column*LINE_LENGTH )
		self.start.setY( row*LINE_LENGTH )
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

	def initGridLines( self ):
		maxPos = self._grid.maxPos()
		for cell in range( maxPos+1 ):
			column, row, dir = self._grid.getCoord( cell )
			self.lines.append( GridLine( column, row, dir ) )
			
	def addLine( self, cell:int ):
		self._grid.setLine( cell )
		self.highlite( cell )
		
	def highlite( self, cell:int ):
		try:
			self.lines[ self._lastLineId ].color = LINE_DRAWN
		except:
			pass
		self._lastLineId = cell
		self.lines[ cell ].color = LINE_LASTDRAWN		
		self.lines[ cell ].width = LINE_THICKNESS_DRAWN	
		
	def paintEvent(self, event):
		painter = QtGui.QPainter()
		painter.begin(self)
		for line in self.lines:
			pen = QtGui.QPen()
			pen.color = line.color
			pen.setWidth( line.width )
			painter.setPen(	 pen )
			painter.drawLine( line.start, line.end )
		painter.end()
