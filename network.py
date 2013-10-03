import socket

DEFAULT_PORT = 50009
BUFFER_SIZE = 1024

class communicator(object):
    def __init__( self ):
        self._socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self._connection = self._socket
        self._connectedto = None
    
    def connectedTo( self ):
        return self._connectedto

    def receiveMessage( self ):
        """Will wait until message is recieved and return it"""
        data = self._connection.recv( BUFFER_SIZE )
        if not data: 
            raise StandardError()
        return data.decode()

    def sendMessage( self, message ):
        self._connection.send( message.encode() )
    
    def close( self ):
        self._connection.close()

class server(communicator):
    def waitForConnection( self, port=DEFAULT_PORT ):
        self._socket.bind( ('', port ) )
        self._socket.listen( 1 )
        self._connection, self._addr = self._socket.accept()


class client(communicator):
    def connectToServer( self, host, port=DEFAULT_PORT ):
        self._connection.connect((host, port))