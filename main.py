import network
import gui

def main():
	"""Main function for Boxes"""
	
	SCORE = [0,0]

	# Create window
	win = gui.createWindow()

	type = int( input("Start server(0) or client(1)") )

	c = None
	myturn = False
	if type == 0:
		c = network.server()
		print("Waiting for opponent")
		c.waitForConnection()
		print( "Connected to: ", c.connectedTo() )
		myturn = True

	elif type == 1:
		c = network.client()
		host = input("Host:")
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
					print("Score is now %d:%d, draw again" % ( SCORE[0], SCORE[1] ) )
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
					print("Score is now %d:%d, draw again" % ( SCORE[0], SCORE[1] ) )

	c.close()
	win.closeWindow()



if __name__ == "__main__":
	main()


