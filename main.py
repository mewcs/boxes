import network
import gui
from PyQt5 import QtCore, QtGui, QtWidgets

def main():
	"""Main function for Boxes"""
	
	SCORE = [0,0]

	# Create window
	win = gui.createWindow()

	askServerClient = QtWidgets.QInputDialog( win )
	askServerClient.setLabelText( "Enter ip to connect to or empty to be host" ) 
	askServerClient.exec()

	connectTo = askServerClient.textValue()

	host = connectTo if connectTo.strip() else None

	c = None
	myturn = False
	if not host:
		c = network.server()
		print("Waiting for opponent")
		c.waitForConnection()
		print( "Connected to: ", c.connectedTo() )
		myturn = True

	else:
		c = network.client()
		c.connectToServer( host )

	if not c:
		return
	
	# Main loop
	while 1:
		if myturn:
			outmessage = input("Send int: ")

			if( outmessage == "QUIT" ):
				break
			else:
				try:
					int( outmessage )
				except:
					print("Invalid input")
					continue
			
			result = win.grid.setLine( int(outmessage) )
			if result >= 0:
				win.setLine( int(outmessage) )
				c.sendMessage( outmessage )
				if result == 0:
					myturn = False
				elif result > 0:
					SCORE[ 0 ] += result
					win.setScore( SCORE )
					for box in win.grid.completesBoxes( int(outmessage) ):	
						win.setBox( box, 0 )
			else:
				print("Can't draw here, try again")
					
		else:
			print( "Waiting for response" )
			inmessage = int( c.receiveMessage() )
			result = win.grid.setLine( inmessage )
			print( "Recieved: ", inmessage )
			if result >= 0:
				win.setLine( inmessage )
				if result == 0:
					myturn = True
				else:
					SCORE[ 1 ] += result
					win.setScore( SCORE )
					for box in win.grid.completesBoxes( int(outmessage) ):	
						win.setBox( box, 1 )

	c.close()
	win.closeWindow()



if __name__ == "__main__":
	main()


