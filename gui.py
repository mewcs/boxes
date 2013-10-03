import random
import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

class MainWindow(QtWidgets.QWidget):
	def __init__(self, width, height):
		self.app = QtWidgets.QApplication(sys.argv)
		super(MainWindow, self).__init__()
		self.initUI(width, height)
		self.rows = [False]*5
		self.cols = [False]*6
		self.rows[0] = True
		self.rows[1] = True
		self.rows[3] = True
		self.cols[0] = True

	def initUI(self, width, height):
		self.resize(width, height)
		self.center()

		self.setWindowTitle('Boxes')

		self.show()

	def center(self):
		rect = self.frameGeometry()
		point = QtWidgets.QDesktopWidget().availableGeometry().center()
		rect.moveCenter(point)
		self.move(rect.topLeft())

	def paintEvent(self, event):
		painter = QtGui.QPainter()
		painter.begin(self)
		self.drawLines(painter)
		painter.end()

	def drawLines(self, painter):
		red = QtCore.Qt.red
		gray = QtCore.Qt.gray

		for i in range(len(self.rows)):
			x = 10 + i * 12
			y = 10
			if self.rows[i]:
				painter.setPen(red)
			else:
				painter.setPen(gray)
			painter.drawLine(x, y, x + 10, y)

		for i in range(len(self.cols)):
			x = 10
			y = 10 + i * 12
			if self.cols[i]:
				painter.setPen(red)
			else:
				painter.setPen(gray)
			painter.drawLine(x, y, x, y + 10)

	def closeWindow(self):
		sys.exit(self.app.exec_())

def createWindow():
	win = MainWindow(320, 240)
	return win

if __name__ == '__main__':
	win = createWindow()
	win.closeWindow()
