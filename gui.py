import random
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import grid
import gridWidget

class MainWindow(QtWidgets.QWidget):
	def __init__(self, cols, rows):
		self.app = QtWidgets.QApplication(sys.argv)
		super(MainWindow, self).__init__()
		self.initUI(cols, rows)

	def initUI(self, cols, rows):
		line_pad = gridWidget.LINE_THICKNESS_DRAWN_HALF
		widget_pad = 11
		width  = gridWidget.LINE_LENGTH*cols + 1 + 2*line_pad + 2*widget_pad
		height = gridWidget.LINE_LENGTH*rows + 1 + 2*line_pad + 2*widget_pad
		self.resize(width, height)
		self.center()
		self.setWindowTitle('Boxes')

		# Button row
		quitButton = QtWidgets.QPushButton()
		quitButton.setText('QUIT')

		bLyt = QtWidgets.QHBoxLayout()
		bLyt.addWidget( quitButton )


		# Grid widget
		self.grid = grid.Grid( cols, rows )
		self.gridWidget = gridWidget.GridWidget( self.grid )

		# Main layout
		mainLyt = QtWidgets.QVBoxLayout()
		#mainLyt.addLayout( bLyt, 20 )
		mainLyt.addWidget( self.gridWidget )

		self.setLayout( mainLyt )


		self.show()

	def setLine( self, pos:int ):
		self.gridWidget.setLine( pos )

	def center(self):
		rect = self.frameGeometry()
		point = QtWidgets.QDesktopWidget().availableGeometry().center()
		rect.moveCenter(point)
		#self.move(rect.topLeft())
		self.move(rect.topRight())

	def closeWindow(self):
		sys.exit(self.app.exec_())

def createWindow():
	win = MainWindow(5, 5)
	return win

if __name__ == '__main__':
	win = createWindow()
	win.closeWindow()
