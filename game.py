import network
import gui
from PyQt5 import QtWidgets
import time

GRID_SIZE = (5,5)

class Game(object):
    """
    A game of boxes head to head over network or on the same computer.
    """
    def __init__(self, host:str=None):
        '''
        Parameters:
            host : str with ip to connect to or None if server

        Example:
        game = Game() # Creates a new game instance which will be server
        game2 = Game("localhost") # New instance that will connect to host on local machine
        '''

        self._score = [0, 0] # he current score. First index is current player, second is the opponent
        
        self.host = host    # None if server, ip string if client

        self.win = gui.BoxesWindow( GRID_SIZE[0], GRID_SIZE[1] )

        # Init connection
        if self.isServer():
            self._connection = network.server()
        else:
            self._connection = network.client(self.host)

        self.myturn = self.isServer() # Server starts

        # Connect data recieved signal to our function and start network thread
        self._connection.data_recv.connect(self.on_recv)
        self._connection.start()

        # TODO: check that connection succeeded

        # Connect signal when a line is clicked in the ui to game logic
        self.win.gridWidget.lineClicked.connect(self.line_clicked)

    def line_clicked(self, pos):
        """
        When line is clicked in UI
        Parameters:
            pos : The index of the line. See grid module for info about this index
        """
        # Only do something if it is our turn
        if self.myturn:
            self.drawLine( pos )
        else:
            self.win.setStatus("Not your turn")


    def drawLine( self, pos ):
        """
        Draw a line and act on the result of that
        """
        wasMe = self.myturn # Was the line drawn by this game or opponent

        # Set the line in our grid object
        result = self.win.grid.setLine(pos)

        # If setLine was successful
        if result >= 0:
            # Draw the line in the UI
            self.win.setLine(pos)
                
            # If no boxes where completed
            if result == 0:
                self.myturn = not self.myturn

            # If one or more boxes were completed, increment score and draw again
            elif result > 0:
                self._score[not wasMe] += result
                self.win.setScore(self._score)
                # Draw completed boxes
                for box in self.win.grid.completesBoxes(pos):
                    self.win.setBox(box, not wasMe)
            if wasMe:
                self._connection.data_send.emit(str(pos))
            
        # Cant set line at this pos
        else:
            self.win.setStatus("Can't draw here, try again", 2000 )

    def on_recv(self, data):
        """
        Opponent drew a line
        """
        if not self.myturn:
            pos = int(data)
            self.drawLine( pos )
        else:
            raise BaseException("Got line but it's my turn!")

    def isServer(self):
        return not self.isClient()

    def isClient(self):
        return bool(self.host)

    def getMyTurn( self ):
        return self._myturn

    def setMyTurn( self, value ):
        self._myturn = value
        if value:
            self.win.setPermanentStatus( "Your turn" )
        else:
            self.win.setPermanentStatus( "Waiting for opponent" )

    myturn = property( getMyTurn, setMyTurn )
