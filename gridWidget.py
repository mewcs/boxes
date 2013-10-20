from PyQt5 import QtCore, QtGui, QtWidgets
from grid import Grid

# Pre-defines
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

    """
    Holds data about a line such as start-point, end-point and color
    """

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

    def copy(self):
        """
        Return a copy of self
        Note: Is there a safer way to do this.
        What if we add variables to self and forget to copy them in this function?
        """
        newLine = GridLine(0, 0, 0)
        newLine.start = self.start
        newLine.end = self.end
        newLine.color = self.color
        newLine.width = self.width
        return newLine


class GridBox(object):

    """
    Holds data about a box in the grid
    """

    def __init__(self, column: int, row: int):
        self.start = QtCore.QPoint()
        self.start.setX(column * LINE_LENGTH)
        self.start.setY(row * LINE_LENGTH)
        self.end = QtCore.QPoint()
        self.end.setX(self.start.x() + LINE_LENGTH)
        self.end.setY(self.start.y() + LINE_LENGTH)

        self.color = None


class GridWidget(QtWidgets.QWidget):

    """
    A widget for displaying a grid for the game Boxes
    """

    lineClicked = QtCore.pyqtSignal(object)  # Signal emitted when clicking on a line

    def __init__(self, grid: Grid):
        super(GridWidget, self).__init__()
        self._grid = grid
        self.lines = list()  # List of GridLine to draw
        self.boxes = list()  # List of GridBox to draw
        self.mouseOverLine = None  # GridLine to draw on mouseover

        self.initGrid()
        self.scale = 1.0  # The scale of the widget
        self._lastLineId = None
        self._prevMousePos = None
        self.setMouseTracking(True)

    def initGrid(self):
        """
        Create the visual grid. Lines and boxes.
        """
        maxPos = self._grid.maxPos()
        for cell in range(maxPos + 1):
            column, row, orientation = self._grid.getCoord(cell)
            self.lines.append(GridLine(column, row, orientation))

        for box in range(self._grid.maxBox()):
            column, row = self._grid.getBoxCoord(box)
            self.boxes.append(GridBox(column, row))

    def setLine(self, cell: int):
        self.highlight(cell)
        self.repaint()

    def setBox(self, cell: int, color):
        self.boxes[cell].color = color
        self.repaint()

    def highlight(self, cell: int):
        """
        Show a line as just drawn
        """
        if self._lastLineId is not None:
            self.lines[self._lastLineId].color = LINE_DRAWN
        self._lastLineId = cell
        self.lines[cell].color = LINE_LASTDRAWN
        self.lines[cell].width = LINE_THICKNESS_DRAWN

    def resizeEvent(self, event):
        """
        Scale the grid according to the size of the widget
        """
        pixmapWidth = self._grid.cols() * LINE_LENGTH + 2
        pixmapHeight = self._grid.rows() * LINE_LENGTH + 2

        self.scale = min(float(self.width()) / pixmapWidth, float(self.height()) / pixmapHeight)

    def paintEvent(self, event):
        """
        Main paint function. Called whenever recieving focus, resized etc. by QWidget
        """
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

        # draw mouse line.
        if self.mouseOverLine:
                self.drawLine(self.mouseOverLine, painter)

        painter.end()

    @staticmethod
    def drawLine(line: GridLine, painter: QtGui.QPainter):
        """ Draw line in QPainter """
        pen = QtGui.QPen()
        pen.setColor(line.color)
        pen.setWidth(line.width)
        painter.setPen(pen)
        painter.drawLine(line.start, line.end)

    @staticmethod
    def drawBox(box: GridBox, painter: QtGui.QPainter):
        """ Draw box in QPainter """
        rect = QtCore.QRect(box.start, box.end)
        painter.fillRect(rect, box.color)

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        pos = self.locateLine(x, y)

        # Ignore the mouse event if the position hasn't changed since last time.
        if self._prevMousePos == pos:
            return
        self._prevMousePos = pos

        # Return if no line was located at the mouse cursor coordinates.
        if pos is None:
            self.mouseOverLine = None
            # Repaint to remove prev mouse line.
            self.repaint()
            return

        self.mouseOverLine = self.lines[pos].copy()
        self.mouseOverLine.color = LINE_MOUSE
        self.mouseOverLine.width = LINE_THICKNESS_DRAWN
        self.repaint()

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        pos = self.locateLine(x, y)

        # Return if no line was located at the mouse cursor coordinates.
        if pos is None:
            return

        self.lineClicked.emit(pos)

    def locateLine(self, x: int, y: int) -> int:
        """
        Given the local x and y pixels, return the line id that that point
        """
        # Accomodate for scale of grid
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

    def leaveEvent(self, event):
        # Restore the line color at the previous mouse position.
        self.mouseOverLine = None
        self._prevMousePos = None
        self.repaint()

    def sizeHint(self) -> QtCore.QSize:
        """ Returns the ideal size of the widget """
        x = LINE_LENGTH * self._grid.cols() + 1 + 2 * LINE_THICKNESS_DRAWN_HALF
        y = LINE_LENGTH * self._grid.rows() + 1 + 2 * LINE_THICKNESS_DRAWN_HALF
        return QtCore.QSize(x, y)
