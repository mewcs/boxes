import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import grid
import gridWidget


class MainWindow(QtWidgets.QWidget):

    def __init__(self, cols, rows):
        self.app = QtWidgets.QApplication(sys.argv)
        super(MainWindow, self).__init__()
        self.grid = None
        self.scoreLabel = None
        self.gridWidget = None
        self.initUI(cols, rows)

    def initUI(self, cols, rows):
        line_pad = gridWidget.LINE_THICKNESS_DRAWN_HALF
        widget_pad = 11
        width = gridWidget.LINE_LENGTH * cols + 1 + 2 * line_pad + 2 * widget_pad
        height = gridWidget.LINE_LENGTH * rows + 1 + 2 * line_pad + 2 * widget_pad
        self.resize(width, height)
        self.center()
        self.setWindowTitle('Boxes')

        # Score board
        self.scoreLabel = QtWidgets.QLabel()
        self.scoreLabel.setAlignment(QtCore.Qt.AlignCenter)

        sizePolicy = QtWidgets.QSizePolicy()
        sizePolicy.setVerticalPolicy(QtWidgets.QSizePolicy.Fixed)
        self.scoreLabel.setSizePolicy(sizePolicy)

        font = QtGui.QFont()
        font.setPointSize(15)
        self.scoreLabel.setFont(font)

        self.setScore()

        scoreLyt = QtWidgets.QHBoxLayout()
        scoreLyt.addWidget(self.scoreLabel)

        # Grid widget
        self.grid = grid.Grid(cols, rows)
        self.gridWidget = gridWidget.GridWidget(self.grid)

        # Main layout
        mainLyt = QtWidgets.QVBoxLayout()
        mainLyt.addLayout(scoreLyt)
        mainLyt.addWidget(self.gridWidget)

        self.setLayout(mainLyt)

        self.show()

    def setLine(self, pos: int):
        self.gridWidget.setLine(pos)

    def setScore(self, score: list=[0, 0]):
        """
        Set the score in the ui. First index is the player, second is the opponents
        """
        self.scoreLabel.setText("You    %d  :  %d    Opponent" % (score[0], score[1]))

    def setBox(self, pos: int, isOpponent: bool):
        color = gridWidget.COLOR_OPPONENT if isOpponent else gridWidget.COLOR_PLAYER
        self.gridWidget.setBox(pos, color)

    def center(self):
        rect = self.frameGeometry()
        point = QtWidgets.QDesktopWidget().availableGeometry().center()
        rect.moveCenter(point)
        self.move(rect.topRight())


def createWindow():
    win = MainWindow(5, 5)
    return win
