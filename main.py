import game
import PyQt5.QtGui
import sys
global QApp


def main():
    """Main function for Boxes"""
    app = PyQt5.QtGui.QGuiApplication(sys.argv)

    g1 = game.Game()
    g2 = game.Game()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
