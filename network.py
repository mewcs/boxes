import socket
from PyQt5 import QtCore, QtWidgets

DEFAULT_PORT = 50015
BUFFER_SIZE = 1024

class communicator(QtCore.QThread):
	data_recv = QtCore.pyqtSignal(object)
	data_send = QtCore.pyqtSignal(object)

	def __init__(self):
		QtCore.QThread.__init__(self)
		self.data_send.connect(self.on_send)

		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._connection = self._socket
		self._connectedto = None

	def run(self):
		while True:
			data = self.recv()
			self.data_recv.emit(data)

	def connectedTo( self ):
		return self._connectedto

	def recv(self):
		"""Will wait until message is recieved and return it"""
		data = self._connection.recv(BUFFER_SIZE)
		if not data:
			raise Exception()
		return data.decode()

	def on_send(self, data):
		self._connection.send(data.encode())

	def close(self):
		self._connection.close()


class server(communicator):
	def __init__(self, port=DEFAULT_PORT):
		print("server.__init__()")
		super(server, self).__init__()
		self._port = port

	def run(self):
		print("server.run()")
		self.waitForConnection()
		super(server, self).run()

	def waitForConnection(self):
		print("server.waitForConnection()")
		self._socket.bind(('', self._port))
		self._socket.listen(1)
		self._connection, self._addr = self._socket.accept()


class client(communicator):
	def __init__(self, host, port=DEFAULT_PORT):
		print("client.__init__()")
		super(client, self).__init__()
		self._host = host
		self._port = port

	def run(self):
		print("client.run()")
		self.connectToServer()
		super(client, self).run()

	def connectToServer(self):
		print("client.connectToServer()")
		self._connection.connect((self._host, self._port))
