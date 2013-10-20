import game
from PyQt5 import QtWidgets
import sys


def main():
    """Main function for Boxes game"""

    app = QtWidgets.QApplication(sys.argv)  # Qt needs an app context for its widgets

    # Ask: Play head to head on the same computer or over network
    localOrNetwork = QtWidgets.QMessageBox()
    localOrNetwork.setWindowTitle("Boxes")
    localOrNetwork.setText("How do you want to play?")
    localOrNetwork.addButton("Local", QtWidgets.QMessageBox.NoRole)
    localOrNetwork.addButton("Host", QtWidgets.QMessageBox.NoRole)
    localOrNetwork.addButton("Client", QtWidgets.QMessageBox.NoRole)
    localOrNetwork.exec()
    result = localOrNetwork.result()

    # Create game objects depending on above choice
    if result == 0:  # Create two games on the local machine
        g1 = game.Game()
        g2 = game.Game("localhost")

    # Act as server
    elif result == 1:
        g = game.Game()

    # Act as client
    elif result == 2:
        askServerClient = QtWidgets.QInputDialog()
        askServerClient.setLabelText("Enter ip to connect to")
        askServerClient.exec()
        host = askServerClient.textValue()
        g = game.Game(host)

    # Exit when app exists
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
