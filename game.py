import network
import gui
from PyQt5 import QtWidgets


class Game(object):

    def __init__(self):
        self._score = [0, 0]

        self.win = gui.createWindow()

        # Server or client
        askServerClient = QtWidgets.QInputDialog(self.win)
        askServerClient.setLabelText("Enter ip to connect to or empty to be host")
        askServerClient.exec()
        host = askServerClient.textValue()

        self.host = host if host.strip() else None

        # Init connection
        if self.isServer():
            self._connection = network.server()
        else:
            self._connection = network.client(self.host)

        self.myturn = self.isServer()
        self._connection.data_recv.connect(self.on_recv)
        self._connection.start()

        # TODO: check that connection succeeded

        self.win.gridWidget.lineClicked.connect(self.line_clicked)

    def line_clicked(self, pos):
        if self.myturn:
            result = self.win.grid.setLine(pos)
            if result >= 0:
                self.win.setLine(pos)
                if result == 0:
                    self.myturn = False
                elif result > 0:
                    self._score[0] += result
                    self.win.setScore(self._score)
                    for box in self.win.grid.completesBoxes(pos):
                        self.win.setBox(box, 0)
                self._connection.data_send.emit(str(pos))
            else:
                print("Can't draw here, try again")

    def on_recv(self, data):
        if not self.myturn:
            pos = int(data)
            result = self.win.grid.setLine(pos)
            if result >= 0:
                self.win.setLine(pos)
                if result == 0:
                    self.myturn = True
                else:
                    self._score[1] += result
                    self.win.setScore(self._score)
                    for box in self.win.grid.completesBoxes(pos):
                        self.win.setBox(box, 1)
        else:
            raise BaseException("Got line but it's my turn!")

    def isServer(self):
        return not self.isClient()

    def isClient(self):
        return bool(self.host)
