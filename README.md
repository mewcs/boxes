boxes
=====

The purpose of this project is to create a digital version of the pencil and
paper game known as [boxes][].

[boxes]: https://en.wikipedia.org/wiki/Dots_and_Boxes

Ideas
-----

* Network capabilities.
	- Allow players to connect to one another.

* Graphical user interface.
	- Create a window and render the lines that makes up the various boxes.
	- Derive user input from the mouse.

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
		- Which parts of the API can be separated into individual modules/classes
		  that can later be reused to create a NPC player with some basic kind of
		  artificial intelligence.
	* Implement a skeleton structure of the API which includes class, method and
	  function definitions.

4. Implement base functionality.
	* ...

Future work
-----------

* Create a simple NPC.
	- This would allow single player games in which a human is playing against
	  the computer.

Previous work
-------------

* [KSquares][] (c++)

[KSquares]: http://games.kde.org/game.php?game=ksquares
