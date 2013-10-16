from PyQt5 import QtCore, QtGui, QtWidgets
from grid import Grid

LINE_LENGTH = 20
LINE_THICKNESS = 1
LINE_THICKNESS_DRAWN = 3
LINE_THICKNESS_DRAWN_HALF = int(LINE_THICKNESS_DRAWN / 2)
LINE_UNDRAWN = QtCore.Qt.gray
LINE_DRAWN = QtCore.Qt.black
LINE_LASTDRAWN = QtCore.Qt.red
LINE_MOUSE = QtCore.Qt.yellow

COLOR_PLAYER = QtCore.Qt.blue
COLOR_OPPONENT = QtCore.Qt.green


class GridLine(object):

    def __init__(self, column: int, row: int, orientation: int):
        pad = LINE_THICKNESS_DRAWN_HALF
        self.start = QtCore.QPoint()
        self.start.setX(pad + column * LINE_LENGTH)
        self.start.setY(pad + row * LINE_LENGTH)
        self.end = QtCore.QPoint()
        if(orientation == Grid.VLINE):
            self.end.setX(self.start.x())
            self.end.setY(self.start.y() + LINE_LENGTH)

        elif(orientation == Grid.HLINE):
            self.end.setX(self.start.x() + LINE_LENGTH)
            self.end.setY(self.start.y())

        self.color = LINE_UNDRAWN
        self.width = LINE_THICKNESS


class GridBox(object):

    def __init__(self, column: int, row: int):
        self.start = QtCore.QPoint()
        self.start.setX(column * LINE_LENGTH)
        self.start.setY(row * LINE_LENGTH)
        self.end = QtCore.QPoint()
        self.end.setX(self.start.x() + LINE_LENGTH)
        self.end.setY(self.start.y() + LINE_LENGTH)

        self.color = None


class GridWidget(QtWidgets.QWidget):
    lineClicked = QtCore.pyqtSignal(object)

    def __init__(self, grid: Grid):
        super(GridWidget, self).__init__()
        self._grid = grid
        self.lines = list()
        self.boxes = list()
        self.initGrid()
        self.scale = 1.0
        self.show()
        self._lastLineId = None
        self._prevMousePos = None
        self.setMouseTracking(True)

    def initGrid(self):
        maxPos = self._grid.maxPos()
        for cell in range(maxPos + 1):
            column, row, orientation = self._grid.getCoord(cell)
            self.lines.append(GridLine(column, row, orientation))

        for box in range(self._grid.maxBox()):
            column, row = self._grid.getBoxCoord(box)
            self.boxes.append(GridBox(column, row))

    def setLine(self, cell: int):
        self.highlite(cell)
        self.repaint()

    def setBox(self, cell: int, color):
        self.boxes[cell].color = color
        self.repaint()

    def highlite(self, cell: int):
        if self._lastLineId is not None:
            self.lines[self._lastLineId].color = LINE_DRAWN
        self._lastLineId = cell
        self.lines[cell].color = LINE_LASTDRAWN
        self.lines[cell].width = LINE_THICKNESS_DRAWN

    def resizeEvent(self, event):
        pixmapWidth = self._grid.cols() * LINE_LENGTH + 2
        pixmapHeight = self._grid.rows() * LINE_LENGTH + 2

        self.scale = min(float(self.width()) / pixmapWidth, float(self.height()) / pixmapHeight)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.scale(self.scale, self.scale)

        # draw boxes
        for box in self.boxes:
            if box.color:
                self.drawBox(box, painter)

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
    def drawLine(line: GridLine, painter: QtGui.QPainter):
        pen = QtGui.QPen()
        pen.setColor(line.color)
        pen.setWidth(line.width)
        painter.setPen(pen)
        painter.drawLine(line.start, line.end)

    @staticmethod
    def drawBox(box: GridBox, painter: QtGui.QPainter):
        rect = QtCore.QRect(box.start, box.end)
        painter.fillRect(rect, box.color)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        pos = self.locateLine(x, y)

        # Ignore the mouse event if the position hasn't changed since last time.
        if self._prevMousePos == pos:
            return

        # Restore the line color at the previous mouse position.
        self.restorePrevMouseLine()

        # Return if no line was located at the mouse cursor coordinates.
        if pos is None:
            # Repaint to remove prev mouse line.
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
        self.lineClicked.emit(pos)

    def locateLine(self, x: int, y: int) -> int:
        x /= self.scale
        y /= self.scale
        pad = LINE_THICKNESS_DRAWN_HALF + 1
        for pos in range(len(self.lines)):
            line = self.lines[pos]
            if pos < self._grid.horiz():
                # Horizontal line.
                xpad = 0
                ypad = pad
            else:
                # Vertical line.
                xpad = pad
                ypad = 0
            if line.start.x() - xpad <= x <= line.end.x() + xpad and line.start.y() - ypad <= y <= line.end.y() + ypad:
                return pos
        return None

    def restorePrevMouseLine(self):
        """ Restore the line color at the previous mouse position. """
        if self._prevMousePos is not None:
            self.lines[self._prevMousePos].color = LINE_UNDRAWN
            self.lines[self._prevMousePos].width = LINE_THICKNESS
            self._prevMousePos = None

    def leaveEvent(self, event):
        # Restore the line color at the previous mouse position.
        self.restorePrevMouseLine()
        self.repaint()
