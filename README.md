boxes
=====

The purpose of this project is to create a digital version of the pencil and
paper game known as [boxes][].

The following image demonstrates a game of boxes on a 2x2 board.

![Boxes Screenshot](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Dots-and-boxes.svg/300px-Dots-and-boxes.svg.png)

[boxes]: https://en.wikipedia.org/wiki/Dots_and_Boxes

Ideas
-----

* Networking capabilities.
	- Allow players to connect to one another.
	- Standard modules socket and asyncore could be useful/sufficient for the networking functionality.

* Graphical user interface.
	- Create a window and render the lines that makes up the various boxes.
	- Derive user input from the mouse.
	- The pygame module has among other things a simple 2d-renderer.
	- Qt could also be used for rendering.

* Pause and continue (if time allows).
	- It should be possible to save the game state.
	- Transfer old game state from server to client at the beginning of the game.

* Use the latest stable version of all libraries:
	- Python 3.3.x
	- Qt 5.1.x

Timeframe
---------

Approximately four weeks.

Milestones
----------

1. Research
	* Search for rendering libraries that can be used from Python.
		- Create a small proof of concept that uses a library to draw a single
		  line between two given coordinates (x, y).
	* Learn more about the networking capabilities available in Python.

2. Proof of concept.
	* Complete a quick demo which demonstrates the feasibility of the project.
		- The user input could be hardcoded and the output could be in ASCII. The
		  goal is to make sure that the game logic can be implemented in time.

3. Discuss the API and design.
	* How should the project be implemented?
		- Which parts of the API can be separated into individual modules/classes?
		  Would it be possbile to use these modules to create a NPC player with
		  some basic kind of artificial intelligence.
	* Implement a skeleton structure of the API which includes class, method and
	  function definitions.

4. Implement base functionality.

5. Test functionality and try to locate bugs.

6. Fix bugs and clean up the implementation.

Design
------

* Isolate logic so that it can be used by a variety of front-ends.
* Isolate networking functionality.
* Implement two front-ends to verify the isolation of logic and networking.
	- A command line interface.
	- A graphical user interface (Qt).

Future work
-----------

* Create a simple NPC.
	- This would allow single player games in which a human is playing against
	  the computer.

* Use the grid from a finished game of boxes to construct a cubescape. The
  cubescape will be divided into blue and red areas based on the players color.
  This devision of areas could be used as a starting point for a game of RISK
  or Heroes of Might and Magic.

Previous work
-------------

* [KSquares][] (c++)

[KSquares]: http://games.kde.org/game.php?game=ksquares
