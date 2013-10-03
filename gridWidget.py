from PyQt5 import QtCore, QtGui, QtWidgets
import grid

LINE_LENGTH = 10

class GridWidget( QtWidgets.QWidget ):
	def __init__( self, grid : grid.Grid ):
		super(GridWidget, self).__init__()
		self._grid = grid
		self.show()

	def addLine( self, cell:int ):
		self._grid.setLine( cell )
		
	def paintEvent(self, event):
		painter = QtGui.QPainter()
		painter.begin(self)
		self.drawLines(painter)
		painter.end()

	def drawLines(self, painter):
		filled = self._grid.drawnLines()
		maxPos = self._grid.maxPos()

		for cell in range( maxPos+1 ):
			color = QtCore.Qt.red if cell in filled else QtCore.Qt.gray
			painter.setPen( color )
			column, row, dir = self._grid.getCoord( cell )

			s1 = QtCore.QPoint() #Draw from
			s2 = QtCore.QPoint() #Draw to
		
			s1.setX( column*LINE_LENGTH )
			s1.setY( row*LINE_LENGTH)

			if( dir == self._grid.VLINE ):
				s2.setX( s1.x() )
				s2.setY( s1.y()+LINE_LENGTH )

			elif( dir == self._grid.HLINE ):
				s2.setX( s1.x()+LINE_LENGTH )
				s2.setY( s1.y() )

			painter.drawLine( s1, s2 )