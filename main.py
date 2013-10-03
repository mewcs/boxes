import network
import gui


def main():
    """Main function for Boxes"""
    
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
                myturn = False
            
            c.sendMessage( outmessage )
        else:
            print( "Waiting for response" )
            inmessage = c.receiveMessage()
            print( "Recieved: ", inmessage )
            myturn = True

    c.close()
    win.closeWindow()



if __name__ == "__main__":
    main()


