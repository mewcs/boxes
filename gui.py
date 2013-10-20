import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import grid
import gridWidget


class BoxesWindow(QtWidgets.QWidget):

    """
    The main ui for the gmae
    """

    def __init__(self, cols: int, rows: int):
        """
        Parameters:
            cols: Numer of columns
            rows: Numbers of rows
        """
        super(BoxesWindow, self).__init__()

        line_pad = gridWidget.LINE_THICKNESS_DRAWN_HALF
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

        # Status line
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.setSizeGripEnabled(False)
        self.statusBar.setFixedHeight(50)
        self.permanentStatus = QtWidgets.QStatusBar()
        self.permanentStatus.setSizeGripEnabled(False)
        self.permanentStatus.setMinimumWidth(200)
        self.statusBar.addWidget(self.permanentStatus)

        # Grid widget
        self.grid = grid.Grid(cols, rows)
        self.gridWidget = gridWidget.GridWidget(self.grid)

        # Main layout
        mainLyt = QtWidgets.QVBoxLayout()
        mainLyt.setAlignment(QtCore.Qt.AlignHCenter)
        mainLyt.addLayout(scoreLyt)
        mainLyt.addWidget(self.statusBar)
        mainLyt.addWidget(self.gridWidget)

        self.setLayout(mainLyt)

        self.show()

    def setLine(self, pos: int):
        """ Draw a line """
        self.gridWidget.setLine(pos)

    def setScore(self, score: list=[0, 0]):
        """
        Set the score in the ui. First index is the player, second is the opponents
        """
        self.scoreLabel.setText("You    %d  :  %d    Opponent" % (score[0], score[1]))

    def setBox(self, pos: int, isOpponent: bool):
        """
        Draw a box
        """
        color = gridWidget.COLOR_OPPONENT if isOpponent else gridWidget.COLOR_PLAYER
        self.gridWidget.setBox(pos, color)

    def center(self):
        """ Centers this window on the screen """
        rect = self.frameGeometry()
        point = QtWidgets.QDesktopWidget().availableGeometry().center()
        rect.moveCenter(point)
        self.move(rect.topRight())

    def setStatus(self, text: str, msecs: int=1000):
        """ Show a message in the status bar for msecs milliseconds """
        self.statusBar.showMessage(text, msecs)

    def setPermanentStatus(self, text: str):
        """
        Show a permanent message in the status bar.
        Overrides any previous permanent message
        """
        self.permanentStatus.showMessage(text)
